from pathlib import Path

from PIL import Image

from gsuid_core.bot import Bot
from gsuid_core.help.utils import register_help
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.sv import SV

sv = SV("千小妹还在吃", pm=6, area="ALL")

_plugin_dir = Path(__file__).parent.parent.parent
_ICON_PATH = _plugin_dir / "ICON.png"

_HELP_TEXT = (
    "🍱 【千小妹还在吃】干饭指南\n\n"
    "🍔 基础点餐：\n"
    "· 吃什么 / 喝什么（全宇宙随机）\n"
    "· 来点现实的食物 / 来点现实的饮品\n\n"
    "✨ 异界特产：\n"
    "· 鸣潮特产 / 原神特产（指定世界）\n"
    "· 来点黑暗料理\n\n"
    "🤖 MOD干饭人：\n"
    "· 在 data/ChisaEating/ganfanren/ 下新建文件夹\n"
    "  放入表情包即可自动加载"
)


@sv.on_fullmatch(
    ("千小妹还在吃帮助", "千咲吃什么帮助", "干饭帮助", "美食帮助"),
    prefix=False,
    block=True,
)
async def chisa_help(bot: Bot, ev: Event) -> None:
    logger.info(f"[ChisaEating] 帮助指令 | uid={ev.user_id} gid={ev.group_id}")
    await bot.send(_HELP_TEXT)


if _ICON_PATH.is_file():
    try:
        with Image.open(_ICON_PATH) as _icon:
            register_help("ChisaEating", "千小妹还在吃帮助", _icon.convert("RGBA"))
    except Exception as _exc:
        logger.warning(f"[ChisaEating] 注册插件帮助失败: {_exc}")
