import logging
import os
from typing import Optional


class Logger:
    def __init__(
        self,
        name: str,
        level: int = logging.INFO,
        formatter_str: str = "%(asctime)s - %(name)s:%(levelname)s - %(message)s",
        console: bool = True,
        file: Optional[str] = None,
        file_level: Optional[int] = None,
        file_formatter_str: Optional[str] = None,
        date_formatter_str: str = "%Y-%m-%d %H:%M:%S %Z",
    ) -> None:
        # create logger
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(level)

        self.debug = self.__logger.debug
        self.info = self.__logger.info
        self.warning = self.__logger.warning
        self.error = self.__logger.error
        self.critical = self.__logger.critical

        # create file handler
        if file is not None and os.path.isfile(file):
            fh = logging.FileHandler(file)
            flevel = level if file_level is None else file_level
            fh.setLevel(flevel)
            fformater_str = formatter_str if file_formatter_str is None else file_formatter_str
            fh.setFormatter(logging.Formatter(fformater_str, date_formatter_str))
            self.__logger.addHandler(fh)

        # create console handle
        if console:
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(logging.Formatter(formatter_str, date_formatter_str))
            self.__logger.addHandler(ch)
