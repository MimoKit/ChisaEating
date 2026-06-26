from gsuid_core.data_store import get_res_path
from gsuid_core.utils.plugins_config.gs_config import StringConfig
from .config_default import CONFIG_DEFAULT

CONFIG_PATH = get_res_path() / "ChisaEating" / "config.json"
CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
CHISA_CONFIG = StringConfig("ChisaEating", CONFIG_PATH, CONFIG_DEFAULT)
