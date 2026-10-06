> **说明（先读这一段）**：这是**完整中文说明**，为中文读者保留，内容仍然有效。
> 但它与 [`SKILL.md`](../SKILL.md) 有大量重复，而 SKILL.md 是**权威版本**且已改为英文原生
> （策略：native skill 用英文，**生成出来的笔记跟随用户语言**）。
> 两者不一致时**以 SKILL.md 为准**。想要最短的上手路径请看 [`../README.md`](../README.md)。

# Review Anything

> **把任何学习素材，变成能独立阅读、经得起校验的 Markdown 复习文档。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
![version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Format](https://img.shields.io/badge/format-SKILL.md-blue)
![Agents](https://img.shields.io/badge/works%20with-Hermes%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20any%20LLM-green)

教材 PDF、课件、讲义、课堂录音的字幕、和 AI 的教学对话、别人发来的长文、自己写的代码——
丢给 AI 说一句「帮我整理成复习笔记」，得到的东西经常是这样：

- 把课件原文**复制一遍**，只是加了个标题
- 讲过的知识点**缺一半**（老师随口带过的那半句，考试偏偏考它）
- 例题里的数字**是抄的**，而原书印错了
- 公式渲染**全挂**，三个月后自己打开一看全是红字
- 一份 300 页的扫描书，AI 读了 20 页就说"整理完了"

**Review Anything 是一份给 AI 助手看的操作规程**（一个 `SKILL.md` 技能包），用来把这些坑全部堵上。
它不生成"摘要"，它生成的是一套**结构化的复习文档工程**——按主题分文件夹、编号、可扩展、
带自测、附知识依赖图，每一句断言都能回答"这是哪来的"。

它的核心主张只有一句：

> **不同学科的知识长得不一样，所以笔记也不该长一个样。**
> 数学的一条定理、一段 C 代码、一个历史事件，它们的"学会了"是三件完全不同的事——
> 分别由**逻辑**、**运行**、**出处**来保证。所以本技能给三套策略，而不是一套模板硬套。

---

## 它产出什么

一个文件夹，里面是一条完整的知识链：

```
数据库系统原理/
├── 00-总览与知识链.md        # 知识链图、概念职责表、学习路径、笔记索引、疑问速查
├── 01-SQL概述与三级模式.md
├── 02-数据定义-DDL.md
├── 03-单表查询.md
├── 04-连接查询.md
├── 05-嵌套查询.md
├── 06-集合查询与派生表.md
├── 07-数据更新.md
├── 08-空值与三值逻辑.md
├── 09-视图.md
├── 10-SQL语句速查表.md
├── 11-跨DBMS差异与优化器全景.md
├── 12-考前速查表.md           # 一页可打印（可选但强烈建议）
├── 13-勘误与未解问题.md        # 仅记「知识点错误」/ 未解问题（可选但强烈建议）
└── _sources/                  # 提取产物（不可再生的转录文本），见「交付」一节
```

每一篇都是**独立可读**的——不翻原书也能看懂；每篇结尾有**快速自测**（答案折叠）；
篇与篇之间用链接串成**依赖链**；凡是能跑的例子**都真跑过**，跑出来的错误单独记在勘误里。

`00-总览` 长这样：

```markdown
## 知识链

三级模式 → DDL(表/约束) → DML(增删改) → DQL(查) → 视图 → 安全(权限)
                              ↑
                      连接/嵌套/集合（查询的三种组合方式）

## 疑问速查（复习时最容易卡住的点）

| 疑问 | 一句话答案 | 详见 |
|---|---|---|
| `WHERE` 和 `HAVING` 到底谁先执行 | `WHERE` 在分组前过滤行，`HAVING` 在分组后过滤组 | [[03-单表查询]] |
| 成绩是 NULL 的同学为什么"不及格"查询查不到 | 三值逻辑：`NULL < 60` 结果是 UNKNOWN，不是 TRUE | [[08-空值与三值逻辑]] |
```

---

## 五条铁律（不因学科而变）

这五条是通用底线，任何学科都不放松。流程可以简化，铁律不能破。

> **注意**：通用这五条里**没有**「能跑就跑」——实跑是**工程类学科的策略**，不是对数学、文科也生效的通用要求。
> 数学笔记不该被逼着逐题实跑（理论类的核对靠**手算抽样**），文科笔记也不该被逼着跑代码。

| # | 铁律 | 反例（常见的 AI 输出） |
|---|---|---|
| 1 | **重写，不摘抄** — 丢掉讲授语气、章节导语、过渡句，按本学科的结构重组 | 把课件原文抄一遍，只加标题 |
| 2 | **补全知识簇** — 提到 A，就把 A 所在的整个簇一起介绍 | 只总结"交换机"，不提分组交换 / 路由 / 复用 |
| 3 | **固定编号槽位** — `01-`, `02-`… 后续素材往后接，不重命名、不断链 | 用章节名当文件名，加一章全乱 |
| 4 | **自足可读** — 单独发给没看过原素材的人，他也能看懂 | 满篇"如上图所示""参见课件第 12 页" |
| 5 | **标注来源与置信度** — 每条信息都要能回答"这是哪来的" | 把自己推测的东西写得像事实 |

**谁属于哪个知识簇**（第 2 条的判断法）：

| 素材提到 | 必须补全的簇 |
|---|---|
| 交换机 | 分组交换 / 电路交换、路由选择、复用方式 |
| `NOT EXISTS` | `EXISTS` / `IN` / 集合差，以及遇 NULL 时的行为差异 |
| 归一化到 3NF | 1NF / 2NF / BCNF / 反规范化 |
| 行列式 | 矩阵、秩、可逆性、线性相关性 |
| 某个历史事件 | 前因、后果、同期对照 |

**置信度标记**（第 5 条，宁可示弱，不要冒功）：

| 标记 | 含义 |
|---|---|
| （无标记） | 来自素材 |
| `[扩展]` | 我补充的、素材没有的（是增值，但要让人知道） |
| ✅ 实测 | 在本机跑过，附环境 / 版本 |
| 📖 文档 | 查了官方文档 / 权威来源，附链接 |
| ⚠️ 未验证 | 没跑过也没查到权威来源，存疑 |
| **来源不明** | 素材给了论断但查不到出处（文科常见） |

---

## 三种学科策略（本技能的核心）

拿到素材后**第一件事是判断学科类型**，它决定后面所有动作。判错了后面全歪。

| 类型 | 典型素材 | 靠什么保证正确 | 该强调 |
|---|---|---|---|
| **A 理论类** | 数学、物理、化学、统计 | **逻辑** | 公式、推导、关系、用法、例题 |
| **B 工程类** | 编程、网络、操作系统、数据库、电子 | **运行** | 代码、错误分析、实测效果、环境差异、例题 |
| **C 文科类** | 历史、哲学、法学、文学、社科 | **出处** | 主干提取、分类归纳、便于检索 |

**判断口诀**：这东西**错了会怎样**？

> 推不出来（A）／跑不起来（B）／查不到出处（C）。那就是它的核心策略。

完整版（骨架、动作、示例）见 **[`references/subject-strategies.md`](../references/subject-strategies.md)**，
**动笔前必读对应那一节**。

### A 理论类（数学 / 物理 / 化学 / 统计）

**「学会」意味着**：能独立把结论推出来，并且知道它在什么条件下成立、什么条件下失效。
数学的灵魂藏在推导的每一步里（换元、归纳、放缩、基变换）——**只抄结论等于什么都没学到**。

**笔记骨架**：
对象与记号 → 命题陈述（**条件 + 结论完整**）→ 推导 / 证明（**每步标依据**）→
适用条件与等号 → 例题（**每条例题开头写"什么时候用"**）→ 变体与反例 → 常见错误 → 关系（依赖图）

**四个要害**：

1. **每步推导标依据**（`← 因式分解`、`← 拉格朗日中值定理`）——这是区分"有用的笔记"和"抄写"的唯一标准
2. **公式记三件套**：公式本体 + 适用条件 + 等号成立条件（缺后两条的公式是**危险**的）
3. **反例与条件边界**：每个定理追问"去掉某个条件，结论还成立吗"
4. **物理专属**：量纲检查 + 极限退回（$v \ll c$ 是否退化成经典结论）——两把免费的自查尺

**验证方式**：公式渲染校验（必做）· 推导链自检 · **关键数值抽样复核 3–5 处**（sympy / numpy，抓系统性算术倾向）·
适用条件完备性 · 记号一致性 · 编号交叉校验。
→ **不做全量实跑**。理论类的正确性由推导保证，数值抽查只是取样质检。

### B 工程类（编程 / 网络 / 操作系统 / 数据库 / 电子）

**「学会」意味着**：能在自己的环境里把它跑起来、跑错时知道错在哪、并且知道换一个环境会不会变。

> 工程类知识的一句话本质：**「能运行」是唯一的裁判，「在谁的环境下能运行」是第二个裁判。**

**笔记骨架**：
它解决什么问题 → 最小可运行例子（**输出原样贴**）→ 机制 → **错误分析** →
**环境与版本差异** → 边界与陷阱 → 变体 / 替代方案 → 速查表

**四个要害**：

1. **实跑并原样贴输出**——这是本学科的核心策略（工程知识的正确性只有执行能证明）
2. **错误分析块**（四要素缺一不可）：场景 → 根因 → **怎么确认的** → 教训
3. **环境差异表**：OS / 运行时版本 / 依赖版本 / 引擎 / 字符集 ——"我这能跑"的照妖镜
4. **结论写成条件式**："在 A 上实测如此；B 上未测，可能不同"

**验证方式**：实跑（必做）· 照抄测试（只复制笔记里的代码能否复现同样输出）· 环境标注（必做）·
错误复现验证（笔记里写的报错，真去触发一次）。

### C 文科类（历史 / 哲学 / 法学 / 文学 / 社科）

**「学会」意味着**：记住主干骨架，需要时能迅速定位回来，并能分辨"谁在什么立场上说了什么"。
文科知识量大、细节密、且**观点与事实混杂**，所以策略的重心是
**提取主干 → 分类归纳 → 便于检索 → 标注出处与立场**。

**笔记骨架**：
一句话主旨 → **主干骨架（3–7 条，每条一句）** → 展开（论据 / 事例 / 数据）→
概念辨析表 → 人物-事件-年代表 → 流派与争论 → **出处** → 康奈尔式自测

**四个要害**：

1. **主干先行**：先写 3–7 条一句话主干，再挂细节。遮住展开能否复述主干 = 复习的检验
2. **分类归纳**：按**有用的维度**（时间线 / 流派 / 主题 / 争议点）重组，不按原书目录；`00-总览` 放多维索引
3. **出处追溯**：每个论断标页码；**区分一手与转引**，转引必须说明
4. **观点与事实分离**：某学者的观点必须写成「X 认为……」——**把观点写成事实是文科最严重的失真**

**验证方式**：出处完备性（必做）· 术语 / 译名一致性 · 主干自测 · 观点-事实分离自查 ·
硬事实（年代 / 人名 / 地点）抽点外部核查 3–5 处。→ **不实跑**。

### 混合型（很常见，别硬套）

| 混合情形 | 做法 |
|---|---|
| 数学教材里的编程实验单元 | 主体走 A，代码部分按 B（实跑 + 环境标注） |
| 网络课本里的协议公式与推导 | 主体走 B，公式部分按 A（标适用条件） |
| 经济学教材（模型 + 数据 + 思想史） | 按章节分别套用，`00-总览` 注明每篇类型 |
| 一次对话 / 一份课件跨多个学科 | **按篇拆分**，每篇内部保持一致 |

### 三策略速查

| | A 理论类 | B 工程类 | C 文科类 |
|---|---|---|---|
| **核心** | 推导 | 运行 | 出处 |
| **必做** | 每步标依据 | 实跑 + 贴输出 | 标出处 |
| **骨架关键词** | 定义·定理·证明·例题 | 例子·报错·环境·边界 | 主旨·主干·归类·索引 |
| **验证** | 公式渲染 + 推导自检 + 数值抽查 | 实跑 + 照抄测试 + 环境标注 | 出处完备 + 术语一致 + 事实抽点 |
| **最有价值的一节** | 适用条件与反例 | 错误分析 | 观点与事实的分离 |
| **最大陷阱** | 只抄结论 | 把"我能跑"当普适 | 把观点当事实 |

---

## 快速开始

### 1. 安装（选一种）

**Hermes Agent**

```bash
git clone https://github.com/6duck/review-anything.git \
  "$HERMES_HOME/skills/note-taking/review-anything"
```

（`HERMES_HOME` 默认即 Hermes 的安装目录，例如 Windows 上的 `D:\hermes`。
装好后技能名是 `review-anything`，下次会话自动可被加载。）

**Claude Code / 其他支持 SKILL.md 的助手**（Cursor、Cline 等）

```bash
# 用户级（所有项目可用）
git clone https://github.com/6duck/review-anything.git ~/.claude/skills/review-anything

# 或项目级
git clone https://github.com/6duck/review-anything.git .claude/skills/review-anything
```

> 如果你的平台不接受 frontmatter 里的 `metadata:` 扩展字段，删掉那一段即可，
> `name` / `description` / `version` / `license` 是通用字段。

**没有 skill 体系的纯对话模型**

把 [`SKILL.md`](../SKILL.md) 全文贴进对话开头当系统提示，或直接说：
「按 review-anything 的流程处理这份材料」。需要时再把 `references/` 与 `templates/` 里对应的文件追加进去。

### 2. 依赖（只有脚本需要）

```bash
pip install pymupdf                   # PDF 提取（处理 PDF 才需要）
pip install python-pptx python-docx   # 处理 PPTX / DOCX 才需要
# scripts/check_notes.py 纯标准库，零依赖，装好 Python 就能跑
```

三个脚本都声明支持 Linux / macOS / Windows，中文路径可用。

### 3. 用

对助手说：

```
按 review-anything 整理 @第3章-1.pdf，输出到 notes/数据库系统原理/
```

或者更具体：

```
把这份扫描版教材的第 4 章整理成复习笔记，公式要准，例题要跑
```

助手会走完五个阶段：

```
Phase 0 侦察 → Phase 1 提取 → Phase 2 结构 → Phase 3 写作 → Phase 4 校验 → Phase 5 交付
```

然后给你一份**带统计的交付报告**，而不是一句"整理好了"：

```
✅ 完成：数据库系统原理/ 共 13 篇（类型：B 工程类）
   00-总览 + 11 篇正文 + 12-速查表 + 13-勘误
   正文合计 8,400 字 · 公式 176 条 · MathJax 编译 0 失败 · 断链 0 条
   实跑例题 31 道 → 发现素材错误 3 处（已记入 13-勘误）
   ⚠️ 未实跑：MySQL 特有语法 6 条（本机无 MySQL），标 📖 文档
   📁 已保留：_sources/ 转录文本 4 份（约 1.2 MB）—— 扫描件不可再生，想删可删整个 _sources/
```

---

## 工作流五个阶段详解

```
Phase 0  侦察   素材是什么？什么学科？能提取吗？章节边界在哪？输出到哪？
Phase 1  提取   全部转成纯文本落盘（一次转换，反复使用）
Phase 2  结构   知识簇地图 → 文件夹 → 编号方案 → 总览骨架
Phase 3  写作   套用对应学科策略，逐篇成文
Phase 4  校验   机器自检 → 按学科的验证 → 自足性检查
Phase 5  交付   报统计 + 说明保留了什么中间产物 + 清理可再生的临时文件
```

### Phase 0 · 侦察（不要跳过）

**第一件事：判断学科类型**（A / B / C，见上），它决定后面所有动作。判错了后面全歪。

然后回答四个问题，**不要凭文件名猜内容**：

```bash
# 1) 有多少、是什么格式
ls -la <素材>
file <素材>                       # 真格式（扩展名会骗人）

# 2) 是文字层还是扫描层？（决定走哪条提取路线）
python scripts/extract_material.py <素材> --probe

# 3) 章节边界（PDF 书签经常是错的，用页眉页码反算偏移）
#    渲染几页 → 看页眉上的"书内页码" → PDF页 = 书内页 + 偏移
#    若某页无印刷页码（章首页常见），用相邻有页码页 ±1 推定，并把该例外记进提取产物

# 4) 输出到哪、什么语言、多深？
#    必须问，不要假设。默认：与素材同语言的 Markdown，放用户指定的仓库/文件夹
```

**判据（主判据只有一个：近零字符页占比）**：

| 现象 | 判断 | 路线 |
|---|---|---|
| 近零字符页 **< 10%** | 有可用文字层 | **文字型**，走 `get_text()` |
| 近零字符页 **> 50%** | 扫描 / 图片为主 | **扫描型**，走视觉模型转录 |
| 两者之间 | 混合型 | 文字页走文字路线，图片页走视觉路线 |

平均字符数只作辅助信息——**课件转 PDF 每页字少但有文字层，不能拿它当判据**。

### Phase 1 · 提取

**唯一原则：先全部落盘成纯文本，再开始写笔记。** 理由：一次转换反复使用，
上下文不会被"再读一遍 PDF"反复撑爆，出错也能回溯到原文。

按素材类型选路线 → 详见 [`references/extraction-playbook.md`](../references/extraction-playbook.md)，
配套脚本 [`scripts/extract_material.py`](../scripts/extract_material.py)。文字型 PDF、扫描型、PPT、对话记录、
网页、视频字幕、代码仓库各有对应的提取方式；**扫描型是重头戏，见「效率与成本」一节**。

### Phase 2 · 结构

**先画知识簇地图，再动笔。** 在纸上 / 脑子里列出：素材覆盖了哪几个概念？谁依赖谁？
哪个是根（不依赖别的）？哪个是叶（被别的依赖）？

然后定目录结构（详见 [`references/note-conventions.md`](../references/note-conventions.md)）：
`00-总览` 打头，正文 `01-` 起，速查表/勘误**接着正文的序号**排（如 `12-` / `13-`），`_sources/` 存提取产物。
**先写 `00-总览` 的骨架**（标题 + 空的索引表），最后再回头填——它逼你先把结构想清楚。

> **一篇笔记 = 一个知识簇**，不是一页课件、也不是一章教材。判断标准：
> **「这一篇能不能单独拿去复习？」** 不能就调整边界。

### Phase 3 · 写作

用对应学科的模板起手：

| 学科 | 模板 |
|---|---|
| A 理论类 | `templates/note-math.md` |
| B 工程类 | `templates/note-cs.md` |
| C 文科类 | `templates/note-humanities.md` |
| 通用骨架 | [`templates/topic-note.md`](../templates/topic-note.md) |
| 00-总览（MOC） | [`templates/00-overview.md`](../templates/00-overview.md) |
| 考前速查表 | [`templates/cheatsheet.md`](../templates/cheatsheet.md) |

写作时不停对照**五条铁律**，尤其中途停下来问自己「这个概念属于哪个更大的簇」。

### Phase 4 · 校验

**这一步不能省，也不能只靠肉眼。** 三层校验，**第二层随学科而变**。
详见 [`references/verification.md`](../references/verification.md)。

| 层 | 做什么 | 目的 |
|---|---|---|
| **机器** | `check_notes.py` + 公式全量渲染（MathJax / KaTeX 编译） | 语法错、坏链接、渲染失败 |
| **学科** | A：推导自检 + 数值抽样 · B：实跑 + 照抄测试 + 环境标注 · C：出处完备 + 事实抽点 | 按该学科的方式证明内容正确 |
| **自足** | 遮住推导能否重做（A）／照抄能否复现（B）／只看主干能否复述（C） | 证明读者能独立使用 |

> **阴性对照必做**：校验器报 0 错误时，故意塞一条错公式看它会不会报。否则"0 错误"可能只是检测器失效。

### Phase 5 · 交付

**① 报告统计，而不是说"整理好了"。** 具体数字才可验证（见上「快速开始」里的交付报告样例）。

**② 中间产物的处置 —— 先判断"能不能再生"**：

| 类别 | 例子 | 处置 |
|---|---|---|
| **可再生** | 渲染的 PNG、探针脚本、临时 txt | **删掉**（重跑即可，成本低） |
| **不可再生** | 扫描件的**视觉转录文本**、对话提取稿 | **保留**到 `_sources/`（重做要几十分钟 + 大量模型调用） |
| **交付物** | 笔记本身 | 保留 |

> ⚠️ **必须告知用户**：交付时明确写出「保留了什么、为什么保留、占多大空间、想删怎么删」。
> 不要默默保留，也不要默默删除。

**③ 清理工作区**：删掉可再生的临时文件，把工作区恢复原样。

---

## 三个脚本

仓库自带三个轻量脚本。它们不是"锦上添花"，
而是把「我以为检查过了」变成「机器确认过了」的手段。

### `scripts/check_notes.py` —— 笔记自检（十一项，纯标准库）

```bash
python scripts/check_notes.py notes/数据库系统原理/      # 默认 obsidian 模式
python scripts/check_notes.py notes/ --mode plain        # GitHub / 通用 Markdown
python scripts/check_notes.py notes/ --json              # 给 CI / pre-commit 用
python scripts/check_notes.py notes/ --quiet             # 只输出汇总
```

| # | 检查 | 级别 |
|---|---|---|
| C1 | YAML frontmatter 存在且含 `tags` / `created` / `source` | warn |
| C2 | `$` 配对（行内 / 块级）；并识别**字面美元符被当成公式**（如 `价格是 100$ 和 200$ 两个数。`） | error |
| C3 | 公式区域内裸 `#` `%` `&`（未转义） | error |
| C4 | `[[wikilink]]` / 相对链接的目标文件存在（**跳过 frontmatter**——`related` / `source` 允许引用尚未创建的笔记） | error |
| C5 | 占位符残留（`TODO` / `待补` / `XXX` / `???`） | warn |
| C6 | 两位编号的连续性（**缺号 + 重号**） | warn |
| C7 | `00-总览` 索引与磁盘实际文件**双向一致**（磁盘有但索引没收 / 索引有但磁盘没有） | warn |
| C8 | 空文件 / 过短文件（< 200 字） | warn |
| C9 | 行内公式首尾多余空格（`$ x $` 不渲染） | error |
| C10 | 表格行内出现裸 `\|` 的 wikilink 别名 | error |
| C11 | 段落内 `$` 分散在多行且总数为偶数 —— 可能是**跨行行内公式**（不渲染），也可能是多个不相关的字面 `$` | error |

```bash
$ python scripts/check_notes.py notes/数据库系统原理/
检查目录：notes/数据库系统原理
模式：obsidian

[ERROR] 03-单表查询.md:47  C3 公式内含未转义的 '#'  $#G$ → 应为 $\#G$（MathJax 会把 # 当宏参数，整条公式渲染失败）
[ERROR] 04-连接查询.md:112 C4 断链：[[06-集合查询]] 不存在（最接近：06-集合查询与派生表）
[WARN ] 09-视图.md:1       C1 frontmatter 缺少 'source'

共 13 篇 · 正文 8400 字 · 公式 176 条 · ERROR 2 · WARN 1
```

**退出码**：`0` 全过 / `1` 有 error / `2` 仅 warn——可以直接挂到 CI 或 pre-commit。

### `scripts/extract_material.py` —— 素材提取与路线侦察

支持 PDF / PPTX / DOCX / TXT / MD / CSV / JSON。**先用 `--probe` 判路线，再提取。**

```bash
# 侦察：这个素材该走哪条提取路线？（主判据 = 近零字符页占比）
python scripts/extract_material.py 第3章.pdf --probe

# 文字型 PDF → 纯文本（分批写进同一个文件）
python scripts/extract_material.py 第3章.pdf --out ./_extract/src.txt

# 扫描型 PDF → 渲染成 PNG，交视觉模型转录（dpi=150 是甜点）
python scripts/extract_material.py 扫描版.pdf --render-png ./_extract/pages/ --dpi 150
python scripts/extract_material.py 扫描版.pdf --render-png ./_extract/pages/ --pages 40-80

# PPTX / DOCX
python scripts/extract_material.py 课件.pptx --out ./_extract/src.txt
```

要点：

- **主判据统一为「近零字符页占比」**：< 10% 文字型 / > 50% 扫描型 / 之间混合型。平均字符数只作辅助信息打印（课件转 PDF 每页字少但仍有文字层，不能当判据）。
- `--render-png` 会做**页数对账**：打印「PDF 共 N 页 / 本次目标 M 页 / 目录内 K 张 PNG」，并列出未渲染页。分段渲染是合法的，但**转录前必须确认所有区间都渲染完了**，否则笔记会静默缺章。
- `--batch N`（默认 3）输出**批次清单** `batches.txt`，每行一批 3 张独立图片，便于批量调度。
- 示例路径一律用相对路径 `./_extract/`。`/tmp/` 只在 Linux / macOS 存在，Windows 下会失败。

**退出码**：`0` 成功（`--probe` 的 0 表示"侦察完成"，**不代表素材没问题**）/
`1` 失败（依赖缺失 / 目标页范围内缺 PNG / 文件不存在 / 类型不支持）/
`2` 部分完成（`--render-png` 只覆盖了 PDF 的一部分页）。目标范围内缺页退出码 1，只覆盖部分页退出码 2 并警告。

### `scripts/merge_ranges.py` —— 分片转录的覆盖率对账与合并

一本 200+ 页的书拆成 2–4 个 worker 并行转录后，**没有人能靠感觉知道「1..N 每页都被覆盖了吗」**。
这个脚本回答这个问题，做**两层互相独立的对账**：

1. 看**文件名声明的区间**（`p0001-0040.md`）——布局是否完整
2. 看**文件内部的页标记**（`===== p12 =====`）——实际内容是否完整

两者不一致就报警：文件名说 40 页、里面只有 38 个页标记 → 漏转录了 2 页。**只靠文件名，这种漏页永远查不出来。**

```bash
# 对账（默认，不写文件）
python scripts/merge_ranges.py ./_sources/pages/ --total 241

# 对账并合并成一份完整转录稿（按页序）
python scripts/merge_ranges.py ./_sources/pages/ --total 241 --concat ./_sources/full.md

# 分片文件不带区间名（如 a.md / b.md），只按内部页标记对账
python scripts/merge_ranges.py ./_sources/ --total 241 --no-range-check
```

**退出码**：`0` 全覆盖、无重叠、无漏页 / `1` 存在缺口 / 重叠 / 漏页。

---

## 效率与成本

扫描件的视觉转录是整个流程里最贵的一步。下面这些数字是**实测**的，照做能省掉大部分时间。

**单页串行 vs 批量 vs 拼图**：

| 做法 | 效果 |
|---|---|
| ✗ 一次读一页 | 每页一次完整的模型往返，**实测约 8 秒** → 110 页要 **14 分钟** |
| ✓ 一次调用传 **3 张独立图片** | 往返数 ÷3，且每页保持**完整分辨率**，不损失清晰度 |
| ✗ 把两页**拼成一张图** | 会被降采样到约 **620px/页**，**下标和上标糊掉** |

> **「不要拼图」≠「一页一次调用」。** 一次传 3 张独立图片完全没问题；某页转录失败就单独重读那一页。
> `dpi=150` 是甜点：文字清晰，再高也会被下游降采样。

**长任务（200+ 页）不要一个 worker 干到底**——上下文会持续膨胀，越到后面越慢：

| 做法 | 说明 |
|---|---|
| **分片** | 拆成 2–4 个不重叠页区间，每个 worker 负责一段（`pXXX-YYY.md` 命名） |
| **上下文预算** | 每 20–30 页落盘一次；单个 worker 的上下文涨到约 200 轮就换新窗口 |
| **覆盖率对账** | 合并后跑 [`scripts/merge_ranges.py`](../scripts/merge_ranges.py)，确认 1..N 每页都被某个区间覆盖（**别靠感觉**） |
| **编号清单** | 每份转录结尾附本区间的定义 / 定理 / 例编号清单，供后续交叉校验 |

**综合下来，批量 + 分片相对逐页串行大约省 3/4 的时间。**

**上下文预算**：一本扫描书的原始像素远大于其文本——逐页读图会把上下文迅速撑爆。
所以规矩是「**先全部落盘成纯文本，再开始写**」：提取阶段一次做完并写进 `_sources/`，
写作阶段只读文本，不再回头读图。分片任务则靠「每 20–30 页落盘 + 换窗口」把单次上下文维持在可控规模。

> ⚠️ **OCR 读不了数学**：实测通用 OCR 对中文印刷体正文约 85% 准确率，但公式区
> `$a_i$`→`α:`、`=`→`二`、下标乱码。**公式一律靠视觉模型或原文核对，OCR 只用于编号交叉查漏。**

---

## 已知的坑（都写进 SKILL.md 了）

**公式与渲染**

- **`#` 在公式里必须写 `\#`** — `$#G$` 会让**整条公式**渲染失败（MathJax 报宏参数错）。
  群阶 `#G`、基数 `#A` 是高危区。同理警惕 `%` `&` 和裸 `_` `^`。
- **行内公式 `$ x $` 首尾空格不渲染**；块级 `$$...$$` 必须独占一行。
- **引用块里的多行公式和 callout 内公式**在 Obsidian 编辑态会挂 → 引用块里改用行内 `$...$`。
- **表格里的 wikilink 别名要写 `[[路径\|别名]]`**（裸 `|` 撕表格），**正文里反而要写 `[[路径|别名]]`**。

**素材与提取**

- **PDF 书签不可信**，页码偏移用页眉反算；章首页常无页码，用相邻页 ±1 推定。
- 扫描件**不要两页拼一张图**给视觉模型（会被降采样，下标糊掉）；但**一次传 3 张独立图片完全没问题**——
  别把"不拼图"误解成"必须一页一次"。
- 视觉转录**逐页串行**是最大的时间浪费——批量 + 分片能省 3/4 时间。

**工具与路径**

- 中文路径下部分搜索工具会返回 0 结果 → 换 `ls` / `grep` 直接验证，别据此断言文件不存在。
- Windows 下 MSYS 风格路径（`/c/...`）传给原生程序（python / node / git）常常不认 →
  用 `C:/...` 正斜杠原生路径；**`/tmp/` 在 Windows 上不存在** → 用相对路径 `./_extract/`。

**认知**

- 素材**会错**（教材、课件、讲义都会）。发现错误别默默改掉，记进勘误页 —— 但**只记知识点错误**（跟着学会学错的那种）：公式错、数值与自己的方程矛盾、结论丢了前提、引用张冠李戴。错别字、字体、页码顺序、自己渲染时掉的字，都不算。
- 别把「进行中」写成「已完成」。置信度标记就是为此存在的。
- **别把某个学科的做法当成通用铁律**：数学不该被要求逐题实跑，文科不该被要求跑代码。

---

## 输出模式

默认 **obsidian 模式**（`[[wikilink]]` + callout + `$公式$`）。
若目标是 GitHub / 通用 Markdown，切换 **plain 模式**：
用相对路径链接指向 `01-xxx.md` 这类文件（取代 `[[wikilink]]`）、用引用块代替 callout、
公式仍用 `$...$`（GitHub 原生支持）。
`check_notes.py --mode plain` 会跳过只适用于 Obsidian 的检查项。

---

## 目录结构

```
review-anything/
├── SKILL.md                              # 技能本体（给 AI 看的操作规程）
├── README.md                             # 你正在看的这份（给人看的门面）
├── CHANGELOG.md                          # 版本变更记录
├── LICENSE                               # MIT
├── references/
│   ├── subject-strategies.md             # ★ 三种学科策略：骨架 / 动作 / 验证 / 示例（动笔前必读）
│   ├── note-conventions.md               # 笔记结构约定（目录 / frontmatter / MOC / callout / 自测）
│   ├── extraction-playbook.md            # 各类素材的提取手册 + 批量读图 + 分片并行 + 上下文预算
│   └── verification.md                   # 三层校验手册 + 编号交叉校验 + 公式渲染验证
├── templates/
│   ├── note-math.md                      # A 理论类模板
│   ├── note-cs.md                        # B 工程类模板
│   ├── note-humanities.md                # C 文科类模板
│   ├── topic-note.md                     # 通用骨架
│   ├── 00-overview.md                    # 总览（MOC）模板
│   └── cheatsheet.md                     # 考前速查表模板
└── scripts/
    ├── check_notes.py                    # 笔记自检（十一项，纯标准库）
    ├── extract_material.py               # 素材提取（PDF / PPTX / DOCX / TXT）+ 路线侦察
    └── merge_ranges.py                   # 分片转录的覆盖率与编号对账
```

### 配套文件一览

| 文件 | 用途 |
|---|---|
| **[`references/subject-strategies.md`](../references/subject-strategies.md)** | **★ 三种学科策略：骨架 / 动作 / 验证 / 示例（动笔前必读）** |
| [`references/note-conventions.md`](../references/note-conventions.md) | 笔记结构约定：目录、frontmatter、MOC、callout、ASCII 图、自测、链接写法 |
| [`references/extraction-playbook.md`](../references/extraction-playbook.md) | 各类素材的提取手册 + 批量读图 + 分片并行 + 上下文预算 |
| [`references/verification.md`](../references/verification.md) | 三层校验手册 + 编号交叉校验 + 公式渲染验证 |
| [`templates/topic-note.md`](../templates/topic-note.md) · [`templates/00-overview.md`](../templates/00-overview.md) · [`templates/cheatsheet.md`](../templates/cheatsheet.md) | 通用骨架 / 总览（MOC）/ 考前速查表模板；学科专用模板见 `templates/note-math.md`、`templates/note-cs.md`、`templates/note-humanities.md` |
| [`scripts/check_notes.py`](../scripts/check_notes.py) | 笔记自动自检（十一项，纯标准库） |
| [`scripts/extract_material.py`](../scripts/extract_material.py) | 素材提取（PDF / PPTX / DOCX / TXT）+ 路线侦察 |
| [`scripts/merge_ranges.py`](../scripts/merge_ranges.py) | 分片转录的覆盖率与编号对账 |

---

## 设计理念

> 一份复习文档的价值，不在于它收录了多少，而在于**三个月后的你打开它，
> 能不能不翻原书就重新学会**。

所以这个技能宁愿慢一点：先落盘再写、代码真跑、公式真渲染、数字真回验。
慢的这部分，恰好是 AI 最容易偷懒、也最容易被使用者忽略的部分。

而"不同学科用不同策略"这条主线，是因为**通用流程会淹没学科特性**：
逼数学笔记逐题实跑是浪费，逼文科笔记跑代码是错位，逼工程笔记抄结论是危险。
**用对应学科的方式证明内容正确，才是真的正确。**

---

## 贡献

欢迎 PR：新的素材类型提取方案（Markdown / EPUB / 视频字幕 / 手写笔记 OCR）、
新的校验项、别的平台的适配（Notion / Logseq / Anki 导入格式）、
以及更多学科的模板（`templates/note-*.md`）。
提 issue 请附**脱敏后的最小复现素材**。

## License

[MIT](../LICENSE) © 2026 6duck

---

<details>
<summary><b>English TL;DR</b></summary>

**Review Anything** is an agent skill (a `SKILL.md` playbook) that turns *any* study material —
textbook PDFs, lecture slides, scanned chapters, chat transcripts, web articles, source code —
into a **structured, self-contained, verified Markdown review document set**.

Its core claim: **different subjects must be studied differently.** Math/theory notes are proven
correct by *logic*, engineering notes by *running code*, humanities notes by *sources*. So it ships
**three subject strategies** instead of one rigid template. Pick one with the test
*"what happens if this is wrong?"* — can't derive it (theory) / can't run it (engineering) /
can't trace the citation (humanities).

Five universal rules: (1) rewrite instead of transcribe, (2) expand every concept to its full
knowledge cluster, (3) stable numbered slots so the set can grow, (4) each note stands alone,
(5) label provenance and confidence (`[extended]` / ✅ verified / 📖 docs / ⚠️ unverified).
(Note: "run every example" is no longer a universal rule — it is now the *engineering* strategy.)

Pipeline: **recon → extract (dump to plain text first) → structure (cluster map, then MOC) →
write → verify (machine / subject-specific / self-containment) → deliver with statistics**.

Ships with three scripts: `check_notes.py` (**11 checks**, stdlib only),
`extract_material.py` (PDF/PPTX/DOCX + route probing, batch PNG rendering),
and `merge_ranges.py` (coverage reconciliation for sharded transcription).
Plain Markdown output mode is supported for GitHub-friendly notes. MIT licensed.

</details>
