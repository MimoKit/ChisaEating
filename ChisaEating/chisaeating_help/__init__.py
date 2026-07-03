from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from gsuid_core.bot import Bot
from gsuid_core.help.draw_new_plugin_help import get_new_help
from gsuid_core.help.utils import register_help
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.segment import MessageSegment
from gsuid_core.sv import SV

from ..chisaeating_config import CHISA_APPEARANCE_CONFIG
from ..version import ChisaEating_version

sv = SV("千小妹还在吃", pm=6, area="ALL")

_plugin_dir = Path(__file__).parent.parent.parent
_HELP_DIR = Path(__file__).parent
_HELP_JSON_PATH = _HELP_DIR / "help.json"
_ICON_PATH = _plugin_dir / "ICON.png"
_ICON_DIR = _HELP_DIR / "icon_path"
_TEXTURE_DIR = _HELP_DIR / "texture2d"
_DEFAULT_BANNER_BG_PATH = _TEXTURE_DIR / "banner_bg.png"
_DEFAULT_BG_PATH = _TEXTURE_DIR / "bg.jpg"


def _load_help_data() -> dict:
    with _HELP_JSON_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def _show_config_path(key: str) -> Path | None:
    value = str(CHISA_APPEARANCE_CONFIG.get_config(key).data or "").strip().strip('"')
    if not value:
        return None
    path = Path(value).expanduser()
    return path if path.is_file() else None


def _help_column() -> int:
    value = CHISA_APPEARANCE_CONFIG.get_config("ChisaHelpColumn").data
    try:
        column = int(value)
    except (TypeError, ValueError):
        column = 3
    return max(1, min(10, column))


def _load_icon() -> Image.Image | None:
    icon_path = _show_config_path("ChisaHelpIconUpload") or _ICON_PATH
    if not icon_path.is_file():
        logger.warning(f"[ChisaEating] 插件图标不存在: {icon_path}")
        return None
    with Image.open(icon_path) as icon:
        return icon.convert("RGBA")


def _load_banner_bg() -> Image.Image | None:
    custom_path = _show_config_path("ChisaHelpBannerBgUpload")
    banner_path = custom_path or _DEFAULT_BANNER_BG_PATH
    if not banner_path.is_file():
        return None
    with Image.open(banner_path) as banner:
        banner = banner.convert("RGBA")
        if custom_path is not None:
            return banner
        bw, bh = banner.size
        return banner.crop((0, 0, bw, int(bh * 0.40)))


def _load_help_bg() -> Image.Image | None:
    custom_path = _show_config_path("ChisaHelpBgUpload")
    bg_path = custom_path or _DEFAULT_BG_PATH
    if not bg_path.is_file():
        return None
    with Image.open(bg_path) as bg:
        bg = bg.convert("RGBA")
        if custom_path is not None:
            return bg
        bgw, bgh = bg.size
        pad_h = 700
        padded = Image.new("RGBA", (bgw, bgh + pad_h), (15, 15, 25, 255))
        padded.paste(bg, (0, pad_h))
        return padded


@sv.on_fullmatch(
    ("千小妹还在吃帮助", "千咲吃什么帮助", "干饭帮助", "美食帮助"),
    prefix=False,
    block=True,
)
async def chisa_help(bot: Bot, ev: Event) -> None:
    logger.info(f"[ChisaEating] 帮助指令 | uid={ev.user_id} gid={ev.group_id}")
    icon = _load_icon()
    if icon is None:
        return await bot.send("帮助图片生成失败，ICON.png 缺失。")

    extra: dict = {}
    banner_bg = _load_banner_bg()
    help_bg = _load_help_bg()
    if banner_bg is not None:
        extra["banner_bg"] = banner_bg
    if help_bg is not None:
        extra["help_bg"] = help_bg
    if _ICON_DIR.is_dir():
        extra["icon_path"] = _ICON_DIR

    img = await get_new_help(
        plugin_name="ChisaEating",
        plugin_info={f"v{ChisaEating_version}": ""},
        plugin_icon=icon,
        plugin_help=_load_help_data(),
        plugin_prefix="",
        help_mode="dark",
        banner_sub_text="今天也要好好干饭",
        enable_cache=False,
        column=_help_column(),
        pm=ev.user_pm,
        **extra,
    )
    await bot.send(MessageSegment.image(img))


if _ICON_PATH.is_file():
    try:
        with Image.open(_ICON_PATH) as _icon:
            register_help("ChisaEating", "千小妹还在吃帮助", _icon.convert("RGBA"))
    except Exception as _exc:
        logger.warning(f"[ChisaEating] 注册插件帮助失败: {_exc}")
