<p align="center">
  <a href="https://github.com/nnlmc/ChisaEating"><img src="logo.png" width="256" height="256" alt="ChisaEating"></a>
</p>
<h1 align="center">千小妹还在吃 3.0.0</h1>
<h4 align="center">🚧 支持 gscore 框架的跨次元干饭插件，功能持续更新中 🚧</h4>
<div align="center">
  <a href="#丨安装">安装说明</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/Gscore/gsuid_core">gsuid_core</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/dddada123/astrbot_plugin_chisa_still_eating">原版插件</a>
</div>

---

## 丨安装提醒

> **注意：该插件为 [早柚核心 (gsuid_core)](https://github.com/Gscore/gsuid_core) 的扩展插件，使用前请确保已正确安装 gsuid_core。**

> 🚧 插件仍在持续完善中，欢迎提交 issue 或 PR 🚧

将本插件克隆到 gscore 插件目录并重启：

```bash
cd gsuid_core/gsuid_core/plugins
git clone https://github.com/nnlmc/ChisaEating ChisaEating
```

重启 gscore 后插件自动加载，无需额外配置即可使用内置资源包。

> [!CAUTION]
> 请勿将本插件克隆到 `gsuid_core/plugins` 等非标准路径，否则可能导致加载失败。

---

## 丨功能

- 🍔 **随机干饭**：支持鸣潮、原神等多世界食物卡池随机抽取，附带角色人设化台词
- 🌀 **跨次元大乱斗**：抽到其他世界特产时触发联动串门剧情
- 📸 **图文同步**：食物图片与角色表情包同时发送
- 🍳 **厨师系统**：文件名以 `【厨师名】` 开头时触发厨师专属联动台词
- 🎭 **MOD 干饭人**：在数据目录自由添加自定义抢饭角色与语录
- 🛡️ **防刷屏**：滑动时间窗口限流，触发拦截时随机发送干饭人抢饭彩蛋

---

## 丨命令

| 命令 | 说明 |
|------|------|
| `吃什么` / `吃啥` / `吃点儿啥` / `吃点啥` | 全宇宙随机推荐食物 |
| `喝什么` / `喝啥` / `喝点儿啥` / `喝点啥` | 全宇宙随机推荐饮品 |
| `来点黑暗料理` / `黑暗料理` | 触发危险料理卡池 |
| `来点现实的食物` / `来点三次元食物` | 仅从三次元食物卡池抽取 |
| `来点现实的饮品` / `来点三次元饮品` | 仅从三次元饮品卡池抽取 |
| `鸣潮特产` / `原神特产` | 指定世界抽取（支持世界别称） |
| `鸣潮吃什么` / `原神吃什么` | 指定世界推荐食物 |
| `干饭帮助` / `美食帮助` / `千小妹还在吃帮助` | 查看帮助 |

> 所有命令无需前缀，直接发送关键词即可触发。

---

## 丨资源包

内置基础干饭人表情包（千咲、派蒙、达妮娅），预设食物图片库已内置在 `bundled_food_data/` 目录中，无需额外下载即可开箱使用。

**自定义图片**：将食物 / 饮品图片放入 `data/ChisaEating/food/world1/`（对应世界）目录即可自动加载。

**自定义干饭人**：在 `data/ChisaEating/ganfanren/` 下新建文件夹，放入表情包和 `words.txt`（每行一句语录）。

**厨师系统**：文件命名为 `【厨师名】食物名.png` 即可触发厨师联动；厨师立绘放入 `data/ChisaEating/chefs/`。

---

## 丨常用配置

在 gscore Webconsole 的 **ChisaEating** 配置页进行调整，无需手动修改文件。

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| 默认激活世界 | world1 ~ world4 | world1 |
| 抢饭彩蛋概率 % | 干饭人抢饭事件触发概率 | 10 |
| 防刷屏拦截触发次数 | 60 秒内允许的最大触发次数 | 3 |
| 世界1文字食物池 | 无图片时也能推荐的鸣潮特产 | 香柠切片等 |
| 誓死效忠模式 | 只推荐本世界特产 | 关闭 |
| 启用群聊黑名单 | 屏蔽指定群组 | 关闭 |

---

## 丨致谢

- [Rua432 (dddada123)](https://github.com/dddada123) — 原版插件作者
- [gsuid_core](https://github.com/Gscore/gsuid_core) — 早柚核心框架

---

## 丨其他

- 本项目基于 [dddada123/astrbot_plugin_chisa_still_eating](https://github.com/dddada123/astrbot_plugin_chisa_still_eating) 移植，保留原有核心逻辑与资源，重构为 gscore 框架插件
- 本项目仅供学习使用，请勿用于商业用途
- [MIT License](LICENSE)
