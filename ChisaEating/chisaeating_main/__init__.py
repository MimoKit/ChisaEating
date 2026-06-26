import random
from pathlib import Path
from typing import Optional

from gsuid_core.bot import Bot
from gsuid_core.logger import logger
from gsuid_core.models import Event
from gsuid_core.segment import MessageSegment
from gsuid_core.sv import SV

from ..chisaeating_config import CHISA_CONFIG
from ..utils.food_data import FoodDataManager
from ..utils.image_manager import ImageManager
from ..utils.rate_limiter import RateLimiter

sv = SV("千小妹还在吃", pm=6, area="ALL")

_plugin_dir = Path(__file__).parent.parent.parent
_image_mgr = ImageManager(_plugin_dir)
_data_mgr = FoodDataManager()
_rate_limiter = RateLimiter()

_EAT_KWS = ("吃什么", "吃啥", "吃点儿啥", "吃点啥")
_DRINK_KWS = ("喝什么", "喝啥", "喝点儿啥", "喝点啥")
_DARK_KWS = ("来点黑暗料理", "黑暗料理")
_COMMON_EAT_KWS = ("来点现实的食物", "来点三次元食物")
_COMMON_DRINK_KWS = ("来点现实的饮品", "来点三次元饮品")
_ALL_CAT_KWS = _EAT_KWS + _DRINK_KWS + _DARK_KWS + _COMMON_EAT_KWS + _COMMON_DRINK_KWS

_WORLD_PHRASES: dict = {
    "world1": {
        "专属句式": [
            "{bot}觉得今天这顿非{food}莫属啦",
            "唔...根据{bot}的精密测算，今天你和{food}的相性是百分之百哦",
            "{bot}强烈建议你尝尝{food}，绝对不踩雷",
            "既然不知道吃什么，那就来一份索拉里斯特产的{food}吧",
            "快看快看，新鲜出炉的{food}！这可是索拉里斯最抢手的美食呢",
        ],
        "厨师句式": [
            "哇！这可是【{chef}】亲自下厨特制的{food}哦",
            "尝尝看！【{chef}】对这份{food}可是非常有自信呢",
            "这份{food}里满满都是【{chef}】的心意，不吃完的话{bot}可要生气啦",
            "天哪，居然能捕捉到【{chef}】亲手捏制的{food}，今天运气简直太好啦",
            "【{chef}】带着热腾腾的{food}走过来了，快趁热吃吧",
        ],
        "打断句式": [
            "{bot}认为吃得太多对健康不好哦，稍微休息会儿吧",
            "哎呀，后厨的锅都被你点冒烟啦，{bot}觉得需要给厨师放个假",
            "数据终端显示你的饱食度已经超标了呢，{bot}建议先去散散步哦",
            "警报！检测到点菜频率过快，{bot}申请开启防刷屏管制！",
            "再吃下去肚子就要变成圆滚滚的啦，{bot}才不帮你抱走呢",
        ],
    },
    "world2": {
        "专属句式": [
            "前面的区域，以后再来探索吧！先跟{bot}吃点{food}填饱肚子",
            "旅行者，{bot}的肚子已经咕咕叫了...我们快去吃{food}好不好",
            "愿风神保佑你今天吃到的{food}是最美味的",
            "听冒险家协会的人说，提瓦特的{food}最近超级火爆哦",
            "看在{food}的份上，{bot}就勉为其难再给你当一天向导吧",
        ],
        "厨师句式": [
            "哇！是【{chef}】的特色料理{food}！快分{bot}一口，就一口",
            "【{chef}】特意为你准备了{food}哦，吃饱了才有力气冒险嘛",
            "这份{food}可是【{chef}】花了好长时间才做好的，旅行者可千万别浪费",
            "天哪，是【{chef}】亲手掌勺的美味！这盘{food}归{bot}了",
            "闻到万民堂的香味了！【{chef}】端着热腾腾的{food}来看我们啦",
        ],
        "打断句式": [
            "喂！你点得太快啦！{bot}的嘴巴都要跟不上了",
            "再吃下去莫娜都要看不起我们了...{bot}建议先消化一下",
            "你这家伙，是想把万民堂吃破产吗！{bot}命令你停止点菜",
            "嗝~{bot}揉了稳滚滚的肚子，表示真的塞不下更多的菜了",
            "前面的区域（指厨房）以后再来探索吧！厨师已经被你刷罢工了",
        ],
    },
    "world3": {
        "专属句式": ["{bot}为你推荐了{food}", "{bot}觉得今天吃{food}不错"],
        "厨师句式": ["【{chef}】特制了{food}哦"],
        "打断句式": ["别刷啦！{bot}已经跟不上了"],
    },
    "world4": {
        "专属句式": ["{bot}为你推荐了{food}", "{bot}觉得今天吃{food}不错"],
        "厨师句式": ["【{chef}】特制了{food}哦"],
        "打断句式": ["别刷啦！{bot}已经跟不上了"],
    },
}

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


def _cfg(key, default=None):
    try:
        return CHISA_CONFIG.get_config(key).data
    except Exception:
        return default


def _get_wv_settings() -> dict:
    result = {}
    for i in range(1, 5):
        wk = f"world{i}"
        result[wk] = {
            "名称": _cfg(f"{wk}_name", f"世界{i}"),
            "别称": _cfg(f"{wk}_aliases", []),
            "自称池": _cfg(f"{wk}_selfnames", [f"向导{i}"]),
            "文字食物": _cfg(f"{wk}_food_text", []),
            "文字饮品": _cfg(f"{wk}_drink_text", []),
            "文字黑暗料理": _cfg(f"{wk}_dark_text", []),
        }
    return result


def _build_alias_map(wv_settings: dict) -> dict:
    alias_map: dict = {}
    for wk, conf in wv_settings.items():
        for alias in conf.get("别称", []):
            if alias:
                alias_map[str(alias).strip()] = wk
    return alias_map


def _resolve_active_key() -> str:
    sel = _cfg("active_world", "world1")
    if sel in ("world1", "world2", "world3", "world4"):
        return sel
    return "world1"


def _build_config_snapshot() -> dict:
    keys = [
        "mode_loyal", "mode_roller", "mode_normie",
        "history_limit", "spam_threshold",
        "egg_prob", "egg_pool",
        "repeat_prob", "repeat_cooldown",
        "global_meme_prob", "chef_meme_prob", "interception_egg_chance",
    ]
    return {k: _cfg(k) for k in keys}


@sv.on_fullmatch(
    ("千小妹还在吃帮助", "千咲吃什么帮助", "干饭帮助", "美食帮助"),
    prefix=False,
    block=True,
)
async def chisa_help(bot: Bot, ev: Event) -> None:
    logger.info(f"[ChisaEating] 帮助指令 | uid={ev.user_id} gid={ev.group_id}")
    await bot.send(_HELP_TEXT)


@sv.on_keyword(_EAT_KWS, prefix=False)
async def on_eat(bot: Bot, ev: Event) -> None:
    logger.info(f"[ChisaEating] 点餐(食) | uid={ev.user_id} gid={ev.group_id}")
    await _process_request(bot, ev, "food")


@sv.on_keyword(_DRINK_KWS, prefix=False)
async def on_drink(bot: Bot, ev: Event) -> None:
    logger.info(f"[ChisaEating] 点餐(饮) | uid={ev.user_id} gid={ev.group_id}")
    await _process_request(bot, ev, "drink")


@sv.on_keyword(_DARK_KWS, prefix=False)
async def on_dark(bot: Bot, ev: Event) -> None:
    logger.info(f"[ChisaEating] 点餐(黑暗料理) | uid={ev.user_id} gid={ev.group_id}")
    await _process_request(bot, ev, "dark")


@sv.on_keyword(_COMMON_EAT_KWS, prefix=False)
async def on_common_eat(bot: Bot, ev: Event) -> None:
    logger.info(f"[ChisaEating] 点餐(三次元食) | uid={ev.user_id} gid={ev.group_id}")
    await _process_request(bot, ev, "food", forced_world="common")


@sv.on_keyword(_COMMON_DRINK_KWS, prefix=False)
async def on_common_drink(bot: Bot, ev: Event) -> None:
    logger.info(f"[ChisaEating] 点餐(三次元饮) | uid={ev.user_id} gid={ev.group_id}")
    await _process_request(bot, ev, "drink", forced_world="common")


@sv.on_keyword(("特产",), prefix=False)
async def on_world_special(bot: Bot, ev: Event) -> None:
    msg = ev.raw_text.strip()
    if any(k in msg for k in _ALL_CAT_KWS):
        logger.debug(f"[ChisaEating] 特产+吃喝词同现，交由对应处理器 | msg={msg!r}")
        return
    wv_settings = _get_wv_settings()
    alias_map = _build_alias_map(wv_settings)
    forced_world = next((wk for alias, wk in alias_map.items() if alias in msg), None)
    if not forced_world:
        logger.debug(f"[ChisaEating] 特产：未匹配到世界别称，忽略 | msg={msg!r}")
        return
    logger.info(f"[ChisaEating] 世界特产 | world={forced_world} uid={ev.user_id} gid={ev.group_id}")
    await _process_request(bot, ev, "food", forced_world=forced_world)


async def _process_request(
    bot: Bot,
    ev: Event,
    category: str,
    forced_world: Optional[str] = None,
) -> None:
    msg = ev.raw_text.strip()
    uid = ev.user_id
    group_id = ev.group_id or ev.user_id
    gid_str = str(group_id) if group_id else ""

    # 黑白名单
    if gid_str:
        if _cfg("enable_blacklist", False):
            bl = [str(x).strip() for x in (_cfg("blacklist_groups") or []) if str(x).strip()]
            if gid_str in bl:
                logger.debug(f"[ChisaEating] 群 {gid_str} 在黑名单，跳过")
                return
        if _cfg("enable_whitelist", False):
            wl = [str(x).strip() for x in (_cfg("whitelist_groups") or []) if str(x).strip()]
            if gid_str not in wl:
                logger.debug(f"[ChisaEating] 群 {gid_str} 不在白名单，跳过")
                return

    wv_settings = _get_wv_settings()

    # 未由调用方指定世界时，从消息别称自动检测
    if forced_world is None:
        alias_map = _build_alias_map(wv_settings)
        for alias, wk in alias_map.items():
            if alias in msg:
                forced_world = wk
                logger.debug(f"[ChisaEating] 别称匹配 alias={alias!r} -> world={wk}")
                break

    active_key = forced_world if (forced_world and forced_world != "common") else _resolve_active_key()
    active_conf = wv_settings.get(active_key, {})
    active_phrases = _WORLD_PHRASES.get(active_key, {})

    bot_pool = active_conf.get("自称池", ["推荐官"])
    bot_name = random.choice(bot_pool) if bot_pool else "推荐官"

    world_name = active_conf.get("名称", f"世界{active_key[-1]}")
    world_aliases = [a for a in active_conf.get("别称", []) if a]
    if world_aliases:
        world_name = random.choice([world_name] + world_aliases)

    config_snap = _build_config_snapshot()

    # 防刷屏
    spam_threshold = config_snap.get("spam_threshold", 3)
    if _rate_limiter.is_spaming(uid, spam_threshold):
        interception_chance = config_snap.get("interception_egg_chance", 50)
        logger.debug(f"[ChisaEating] 触发防刷屏 uid={uid}")
        if random.randint(1, 100) <= interception_chance:
            inter_text = "【拦截警报】你点得太快啦！千咲怕你撑着，已经先你一步把厨房吃空了！"
            meme_file = _image_mgr.get_egg_meme("千咲")
        else:
            inter_pool = active_phrases.get("打断句式", [f"{bot_name}觉得你点得太频繁了。"])
            inter_text = random.choice(inter_pool).format(bot=bot_name)
            meme_file = _image_mgr.get_bot_meme(active_key, "speechless")
        segs = [MessageSegment.text(inter_text)]
        if meme_file:
            segs.append(MessageSegment.image(Path(meme_file)))
        await bot.send(segs)
        return

    # 摆烂复读
    repeat_cooldown = config_snap.get("repeat_cooldown", 60)
    repeat_prob = config_snap.get("repeat_prob", 10)
    if not _rate_limiter.is_repeat_in_cooldown(gid_str, repeat_cooldown) and random.randint(1, 100) <= repeat_prob:
        _rate_limiter.record_repeat_trigger(gid_str)
        logger.debug(f"[ChisaEating] 触发摆烂复读 gid={gid_str}")
        fallback_pool = _cfg("generic_templates") or ["是啊，{food}好像都不错"]
        text = random.choice(fallback_pool).format(bot=bot_name, food="什么")
        meme_file = _image_mgr.get_bot_meme(active_key, "think")
        segs = [MessageSegment.text(text)]
        if meme_file:
            segs.append(MessageSegment.image(Path(meme_file)))
        await bot.send(segs)
        return

    # 扫描卡池
    pool = _image_mgr.scan_all_items(wv_settings, category)

    # 混入三次元文字池
    if category == "food":
        common_texts = _cfg("common_food_text", []) or []
    elif category == "drink":
        common_texts = _cfg("common_drink_text", []) or []
    else:
        common_texts = []

    for text_item in common_texts:
        name = str(text_item).strip()
        if name:
            pool.append({"wv": "common", "food": name, "raw_name": name, "chef": "none", "has_image": False, "path": None})

    logger.debug(f"[ChisaEating] 卡池扫描完毕 size={len(pool)} category={category} forced_world={forced_world}")

    # 强制世界过滤
    if forced_world:
        strict = [item for item in pool if item["wv"] == forced_world]
        if strict:
            pool = strict

    if not pool:
        logger.warning(f"[ChisaEating] 卡池为空 category={category} forced_world={forced_world}")
        await bot.send("【卡池告急】未找到可用的食物/饮品数据！请检查资源目录或配置。")
        return

    picked = _data_mgr.filter_and_pick(gid_str, pool, active_key, config_snap)

    if not picked:
        logger.warning(f"[ChisaEating] filter_and_pick 返回空 category={category} forced_world={forced_world}")
        await bot.send("【卡池告急】未找到可用的食物/饮品数据！请检查资源目录或配置。")
        return

    food_name = picked["food"]
    chef_name = picked["chef"]
    origin_key = picked["wv"]
    full_food_desc = f"由【{chef_name}】特制的{food_name}" if chef_name != "none" else food_name

    logger.info(
        f"[ChisaEating] 推荐 food={food_name!r} chef={chef_name!r} "
        f"origin={origin_key} img={bool(picked.get('has_image'))}"
    )

    fmt_args = {
        "bot": bot_name, "bot_a": bot_name,
        "food": food_name, "chef": chef_name,
        "full_food_desc": full_food_desc,
        "world_a": world_name,
    }

    is_crossover = origin_key != "common" and origin_key != active_key
    mood = "like"

    if category == "dark":
        pool_text = _cfg("dark_templates") or ["这{full_food_desc}……{bot}已经在害怕了。"]
        final_text = random.choice(pool_text).format(**fmt_args)
        mood = "scared"
    elif is_crossover:
        cross_conf = wv_settings.get(origin_key, {})
        world_b = cross_conf.get("名称", "异世界")
        world_b_aliases = [a for a in cross_conf.get("别称", []) if a]
        if world_b_aliases:
            world_b = random.choice([world_b] + world_b_aliases)
        fmt_args["world_b"] = world_b
        bot_b_pool = cross_conf.get("自称池", ["异界人"])
        fmt_args["bot_b"] = random.choice(bot_b_pool) if bot_b_pool else "异界人"
        pool_text = _cfg("crossover_templates") or ["{bot_a}和{bot_b}一起分享了{full_food_desc}！"]
        final_text = random.choice(pool_text).format(**fmt_args)
    elif chef_name != "none":
        chef_phrases = active_phrases.get("厨师句式", ["【{chef}】特制了{food}哦"])
        final_text = random.choice(chef_phrases).format(**fmt_args)
    elif origin_key == "common":
        pool_text = _cfg("generic_templates") or ["铛铛！为你抽中了{food}！"]
        final_text = random.choice(pool_text).format(**fmt_args)
    else:
        spec_phrases = active_phrases.get("专属句式", [])
        generic = _cfg("generic_templates") or ["铛铛！为你抽中了{food}！"]
        pool_text = spec_phrases + generic
        final_text = random.choice(pool_text).format(**fmt_args)

    # 图片配装
    img_to_send = picked.get("path") if picked.get("has_image") else None
    meme_to_send = None

    egg_prob = config_snap.get("egg_prob", 10)
    chef_meme_prob = config_snap.get("chef_meme_prob", 50)
    global_meme_prob = config_snap.get("global_meme_prob", 30)

    if random.randint(1, 100) <= egg_prob:
        ganfanren_pool = _image_mgr.get_ganfanren_data()
        if ganfanren_pool:
            egg_pool_cfg = config_snap.get("egg_pool", "") or ""
            if egg_pool_cfg.strip() and egg_pool_cfg.strip().lower() != "random":
                cleaned = egg_pool_cfg.replace("；", ";")
                allowed = [n.strip() for n in cleaned.split(";") if n.strip()]
                valid = [n for n in allowed if n in ganfanren_pool] or list(ganfanren_pool.keys())
            else:
                valid = list(ganfanren_pool.keys())
            lucky_name = random.choice(valid)
            meme_to_send = random.choice(ganfanren_pool[lucky_name]["images"])
            words_list = ganfanren_pool[lucky_name]["words"]
            word = random.choice(words_list) if words_list else "但是所有食物被一个神秘吃货一扫而空！"
            final_text += f"\n\n{word}"
        else:
            final_text += "\n\n但是所有食物被一个神秘吃货一扫而空！"
    else:
        if chef_name != "none" and random.randint(1, 100) <= chef_meme_prob:
            meme_to_send = _image_mgr.get_chef_image(chef_name)
        elif random.randint(1, 100) <= global_meme_prob:
            meme_to_send = _image_mgr.get_bot_meme(active_key, mood)

    segs = [MessageSegment.text(final_text)]
    if img_to_send:
        segs.append(MessageSegment.image(Path(img_to_send)))
    if meme_to_send:
        segs.append(MessageSegment.image(Path(meme_to_send)))
    await bot.send(segs)
