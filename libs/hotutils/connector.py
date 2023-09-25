from dataclasses import dataclass
import json
import logging
import os
import pickle
from time import sleep
from typing import Any
from playwright.sync_api import sync_playwright, Request
import requests
from libs.logger import Logger
from libs.mod.mod import Mod
from libs.mod.stat import ModStat
from libs.mod.types import ModSet, ModSlot, StatType


@dataclass
class HotUtilsConnectorConfigs:
    cookie_json_filepath: str | None = None
    out_data_filepath: str | None = None
    mods_dump_filepath: str | None = None
    log_level: int = logging.INFO


class HotUtilsConnector:
    __LOGIN_URL = "https://hotutils.com/login"
    __ACCOUNT_SELECT_URL = "https://hotutils.com/accountselect"
    __FETCH_ALL_URL = "https://api.hotutils.com/Production/account/data/all"

    def __init__(self, configs: HotUtilsConnectorConfigs = HotUtilsConnectorConfigs()) -> None:
        self.__configs = configs
        self.__logger = Logger(f"{self.__class__.__name__}", level=self.__configs.log_level)
        self.__logger.debug("Initializing connector")
        self.__playwright = sync_playwright().start()
        self.__browser = self.__playwright.chromium.launch(headless=False, args=["--start-maximized"])
        self.__context = self.__browser.new_context(no_viewport=True)
        self.__page = self.__context.new_page()
        self.__refresh_request: Request | None = None
        self.__all_data: Any | None = None
        self.__mods: list[Mod] = []

    @property
    def is_running(self) -> bool:
        try:
            _ = self.__page.content()
        except:
            pass
        return not self.__page.is_closed()

    def __load_cookie(self) -> None:
        filepath = self.__configs.cookie_json_filepath
        if filepath is None:
            raise
        with open(filepath, "r") as f:
            cookies = json.load(f)
            self.__context.add_cookies(cookies)
            self.__logger.debug("Cookie loaded")

    def __save_cookie(self) -> None:
        filepath = self.__configs.cookie_json_filepath
        if filepath is None:
            raise
        with open(filepath, "w") as f:
            json.dump(self.__context.cookies(), f)
            self.__logger.debug("Cookie file saved")

    def __on_refresh_request(self, request: Request) -> None:
        self.__refresh_request = request
        self.__logger.debug("Refresh request sent")
        self.__page.remove_listener("request", self.__on_refresh_request)

    def __refresh(self) -> None:
        self.__logger.info("Logging in ...")
        refresh_button = None
        while refresh_button is None:
            try:
                _ = self.__page.content()
            except:
                pass
            refresh_button = self.__page.locator('css=div[class*="BasicLayout_refresh"]')
            if refresh_button.count() == 0:
                refresh_button = None
            self.__logger.debug("Wait ...")
            sleep(1)

        self.__save_cookie()

        self.__logger.info("Syncing HotUtils with game ...")
        self.__page.on("request", self.__on_refresh_request)
        refresh_button.click()

    def login(self) -> None:
        self.__page.goto(self.__LOGIN_URL)
        self.__page.evaluate("() => localStorage.setItem('rememberMe', 1)")
        if self.__configs.cookie_json_filepath and os.path.isfile(self.__configs.cookie_json_filepath):
            self.__logger.info("Found cookie file")
            self.__load_cookie()
            self.__page.goto(self.__ACCOUNT_SELECT_URL)
        else:
            self.__logger.info("No cookie file found, need to login")
            self.__page.reload()

    def get_all_data(self) -> None:
        self.__refresh()
        while self.__refresh_request is None or self.__refresh_request.response() is None:
            self.__logger.debug("Wait ...")
            sleep(1)
        self.__logger.debug("Refresh request done")
        payload = self.__refresh_request.post_data
        headers = self.__refresh_request.headers
        self.__logger.info("Requesting all data from HotUtils ...")
        response = requests.request("POST", self.__FETCH_ALL_URL, headers=headers, data=payload)
        self.__all_data = response.json()["data"]
        if self.__configs.out_data_filepath is not None:
            with open(self.__configs.out_data_filepath, "wb") as f:
                pickle.dump(self.__all_data, f)
            self.__logger.info("All data saved")

    def get_mods(self) -> list[Mod]:
        if self.__all_data is None:
            return []

        mods_data = self.__all_data["mods"]["mods"]
        mods: list[Mod] = []
        for data in mods_data:
            id = data["id"]
            set = ModSet(int(data["setId"]))
            slot = ModSlot(data["slot"] - 1)
            rarity = data["rarity"]
            level = data["level"]
            tier = data["tier"]

            primary_data = data["primaryStat"]
            primary = ModStat(StatType(primary_data["stat"]["unitStatId"]), primary_data["stat"]["statValueDecimal"])

            secondary_data_list = data["secondaryStat"]
            secondaries: list[ModStat] = []
            for secondary_data in secondary_data_list:
                stat_type = StatType(secondary_data["stat"]["unitStatId"])
                stat_decimal_value = secondary_data["stat"]["statValueDecimal"]
                stat_rolls = secondary_data["statRolls"]
                stat = ModStat(stat_type, stat_decimal_value, stat_rolls, rarity)
                secondaries.append(stat)

            mod = Mod(id, set, slot, rarity, level, tier, primary, secondaries)
            mods.append(mod)

        self.__mods = mods
        self.__logger.info(f"Found {len(mods)} mods")

        if self.__configs.mods_dump_filepath is not None:
            with open(self.__configs.mods_dump_filepath, "wb") as f:
                pickle.dump(self.__mods, f)
            self.__logger.info("Mods dump saved")

        return mods

    def close(self) -> None:
        self.__page.close()
