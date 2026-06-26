from typing import Dict
from gsuid_core.utils.plugins_config.models import (
    GSC,
    GsStrConfig,
    GsBoolConfig,
    GsIntConfig,
    GsListStrConfig,
)

CONFIG_DEFAULT: Dict[str, GSC] = {
    # 黑白名单
    "enable_blacklist": GsBoolConfig(
        title="启用群聊黑名单",
        desc="开启后黑名单内的群组无法触发功能（最高优先级）",
        data=False,
    ),
    "blacklist_groups": GsListStrConfig(
        title="群聊黑名单列表",
        desc="填写需要屏蔽的群号，一行一个",
        data=[],
    ),
    "enable_whitelist": GsBoolConfig(
        title="启用群聊白名单",
        desc="开启后只有白名单内的群组可触发功能",
        data=False,
    ),
    "whitelist_groups": GsListStrConfig(
        title="群聊白名单列表",
        desc="填写允许使用的群号，一行一个",
        data=[],
    ),
    # 世界
    "active_world": GsStrConfig(
        title="默认激活世界",
        desc="world1 / world2 / world3 / world4，决定默认推荐官人称与表情包来源",
        data="world1",
    ),
    # 世界 1（鸣潮）
    "world1_name": GsStrConfig(title="世界1名称", desc="世界1的主名称", data="鸣潮"),
    "world1_aliases": GsListStrConfig(
        title="世界1别名",
        desc="触发世界1特产的关键词，如：鸣潮特产",
        data=["鸣潮", "索拉里斯"],
    ),
    "world1_selfnames": GsListStrConfig(
        title="世界1推荐官自称池",
        desc="推荐官随机选取一个自称",
        data=["爱弥斯", "小爱", "雪绒豹豹"],
    ),
    "world1_food_text": GsListStrConfig(
        title="世界1文字食物池",
        desc="无图片时也能推荐的鸣潮特产文字列表",
        data=["香柠切片", "冷调激浪", "今州排骨", "龙吐珠"],
    ),
    "world1_drink_text": GsListStrConfig(
        title="世界1文字饮品池",
        desc="鸣潮特色饮品文字列表",
        data=["今州特调", "清神茶"],
    ),
    "world1_dark_text": GsListStrConfig(
        title="世界1文字黑暗料理池",
        desc="鸣潮的危险特产",
        data=["工业爆炸物", "清汤变异巨蜥", "异种残响烤串"],
    ),
    # 世界 2（原神）
    "world2_name": GsStrConfig(title="世界2名称", desc="世界2的主名称", data="原神世界"),
    "world2_aliases": GsListStrConfig(
        title="世界2别名",
        desc="触发世界2特产的关键词",
        data=["原神", "提瓦特"],
    ),
    "world2_selfnames": GsListStrConfig(
        title="世界2推荐官自称池",
        desc="",
        data=["派蒙", "本向导"],
    ),
    "world2_food_text": GsListStrConfig(
        title="世界2文字食物池",
        desc="",
        data=["甜甜花酿鸡", "蜜酱胡萝卜煎肉", "水煮黑背鲈", "摩拉肉"],
    ),
    "world2_drink_text": GsListStrConfig(
        title="世界2文字饮品池",
        desc="",
        data=["蒲公英酒", "苹果酿", "莓果味汽水"],
    ),
    "world2_dark_text": GsListStrConfig(
        title="世界2文字黑暗料理池",
        desc="",
        data=["奇怪的烤肉排", "微妙的甜甜花酿鸡", "散发诡异气息的冷面"],
    ),
    # 世界 3（自定义）
    "world3_name": GsStrConfig(title="世界3名称", desc="", data="世界3"),
    "world3_aliases": GsListStrConfig(title="世界3别名", desc="", data=[]),
    "world3_selfnames": GsListStrConfig(title="世界3推荐官自称池", desc="", data=["向导3"]),
    "world3_food_text": GsListStrConfig(title="世界3文字食物池", desc="", data=[]),
    "world3_drink_text": GsListStrConfig(title="世界3文字饮品池", desc="", data=[]),
    "world3_dark_text": GsListStrConfig(title="世界3文字黑暗料理池", desc="", data=[]),
    # 世界 4（自定义）
    "world4_name": GsStrConfig(title="世界4名称", desc="", data="世界4"),
    "world4_aliases": GsListStrConfig(title="世界4别名", desc="", data=[]),
    "world4_selfnames": GsListStrConfig(title="世界4推荐官自称池", desc="", data=["向导4"]),
    "world4_food_text": GsListStrConfig(title="世界4文字食物池", desc="", data=[]),
    "world4_drink_text": GsListStrConfig(title="世界4文字饮品池", desc="", data=[]),
    "world4_dark_text": GsListStrConfig(title="世界4文字黑暗料理池", desc="", data=[]),
    # 触发词
    "trigger_eat": GsListStrConfig(
        title="吃什么触发词",
        desc="包含这些词的消息触发食物推荐",
        data=["吃什么", "吃啥", "吃点儿啥"],
    ),
    "trigger_drink": GsListStrConfig(
        title="喝什么触发词",
        desc="",
        data=["喝什么", "喝啥", "喝点儿啥"],
    ),
    "trigger_dark": GsListStrConfig(
        title="黑暗料理触发词",
        desc="",
        data=["来点黑暗料理", "黑暗料理"],
    ),
    "trigger_common_eat": GsListStrConfig(
        title="现实食物触发词",
        desc="强制只从三次元卡池抽取食物",
        data=["来点现实的食物", "来点三次元食物"],
    ),
    "trigger_common_drink": GsListStrConfig(
        title="现实饮品触发词",
        desc="强制只从三次元卡池抽取饮品",
        data=["来点现实的饮品", "来点三次元饮品"],
    ),
    # 三次元文字池
    "common_food_text": GsListStrConfig(
        title="三次元文字食物池",
        desc="无图片时推荐的现实食物",
        data=["黄焖鸡米饭", "麻婆豆腐", "猪脚饭", "兰州牛肉面"],
    ),
    "common_drink_text": GsListStrConfig(
        title="三次元文字饮品池",
        desc="",
        data=["冰可乐", "乌龙茶", "冰吸生椰拿铁", "白开水"],
    ),
    # 概率设置
    "global_meme_prob": GsIntConfig(
        title="常规表情包掉落概率 %",
        desc="0-100，普通推荐时附带发送表情包的概率",
        data=30,
    ),
    "chef_meme_prob": GsIntConfig(
        title="厨师图鉴触发概率 %",
        desc="0-100，抽到厨师特制料理时展示厨师图的概率",
        data=50,
    ),
    "interception_egg_chance": GsIntConfig(
        title="拦截彩蛋概率 %",
        desc="0-100，触发防刷屏时干饭人抢饭的概率",
        data=50,
    ),
    "egg_prob": GsIntConfig(
        title="抢饭彩蛋概率 %",
        desc="0-100，每次推荐触发干饭人抢饭事件的概率",
        data=10,
    ),
    "egg_pool": GsStrConfig(
        title="指定干饭人卡池",
        desc="留空=全员随机；多个名字用英文分号;隔开，如：千咲;派蒙",
        data="",
    ),
    "repeat_prob": GsIntConfig(
        title="摆烂复读概率 %",
        desc="0-100，推荐官陷入沉思并摆烂的概率",
        data=10,
    ),
    "repeat_cooldown": GsIntConfig(
        title="摆烂复读冷却秒数",
        desc="触发一次摆烂后，该群聊的冷却时间（秒）",
        data=60,
    ),
    "history_limit": GsIntConfig(
        title="群组防重复记忆长度",
        desc="最近 N 次推荐的食物不会重复出现，0 表示关闭",
        data=30,
    ),
    "spam_threshold": GsIntConfig(
        title="防刷屏拦截触发次数",
        desc="60 秒内允许连续触发的最大次数",
        data=3,
    ),
    # 互斥模式
    "mode_loyal": GsBoolConfig(
        title="誓死效忠模式",
        desc="开启后推荐官只推荐本世界的特产，不吃其他世界的",
        data=False,
    ),
    "mode_roller": GsBoolConfig(
        title="压路机模式",
        desc="只推荐二次元世界特产，屏蔽三次元普通食物",
        data=False,
    ),
    "mode_normie": GsBoolConfig(
        title="二刺猿不熟模式",
        desc="只推荐三次元普通食物，完全不推荐二次元特产",
        data=False,
    ),
    # 模板池
    "crossover_templates": GsListStrConfig(
        title="跨次元联动句式池",
        desc="跨界抽中其他世界食物时的句式，支持变量: {bot_a} {bot_b} {world_a} {world_b} {full_food_desc}",
        data=[
            "{bot_a}在穿过隧门的过程中，意外来到了{world_b}，并和{bot_b}一起吃了{full_food_desc}！",
            "{bot_a}为了寻找稀有食材，不小心跌入时空裂缝掉进{world_b}，被{bot_b}请客吃了一顿{full_food_desc}。",
            "次元壁破裂啦！{bot_a}从{world_b}顺手拿走了一份{full_food_desc}，并高高兴兴地带回了{world_a}。",
            "{bot_a}在探索新区域时迷路到了{world_b}，刚好遇到了正端着一盘{full_food_desc}的{bot_b}。",
        ],
    ),
    "dark_templates": GsListStrConfig(
        title="黑暗料理句式池",
        desc="抽到黑暗料理时的句式，支持变量: {bot} {full_food_desc}",
        data=[
            "救命，这{full_food_desc}真的是碳基生物能咽下去的吗？！",
            "端上来的居然是{full_food_desc}...{bot}看了一眼，决定战术后仰。",
            "看到{full_food_desc}的那一刻，{bot}的沉默震耳欲聋...",
            "这盘{full_food_desc}散发着诡异的光芒，谁敢动筷子啊！",
            "警报！{bot}发现了一份危险的{full_food_desc}，建议立刻销毁！",
        ],
    ),
    "generic_templates": GsListStrConfig(
        title="通用推荐句式池",
        desc="抽中三次元或普通食物时的句式，支持变量: {bot} {food}",
        data=[
            "铛铛！为你抽中了美味的{food}！",
            "经过深思熟虑，{bot}把这盘{food}端到了你面前。",
            "别纠结啦，今天就吃{food}吧！",
            "经过一番精密的摇号，{bot}宣布今天派发的美食是{food}！",
            "听{bot}的，今天尝试一下{food}准没错~",
        ],
    ),
}
