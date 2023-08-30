import os

if os.environ.get("running_environment", "local").lower() == "local":
    from .config_local import *

    _ = environment
