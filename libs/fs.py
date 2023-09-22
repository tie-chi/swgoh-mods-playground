import os


def check_dir_exists(dir_path: str, should_create: bool = False) -> bool:
    is_exist = os.path.exists(dir_path)
    if not should_create:
        return is_exist
    if not is_exist:
        os.makedirs(dir_path)
    return check_dir_exists(dir_path, False)
