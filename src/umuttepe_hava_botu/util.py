import os


class MissingEnvironmentVariable(Exception):
    pass


def get_env_var(var_name: str) -> str:
    try:
        return os.environ[var_name]
    except KeyError:
        raise MissingEnvironmentVariable(f"{var_name} does not exist")
