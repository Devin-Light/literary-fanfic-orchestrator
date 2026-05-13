# literary-fanfic-orchestrator

> 一个用于严肃文学向同人创作的 Claude Code 元技能。不代你写，而是帮你以正确的方式调用正确的技能——并在此过程中逐步建立你自己的创作方法论。

## 这是什么？

此仓库提供一个**通用创作方法论层**（元 skill），配合已有的 craft skill 生态（`@arcanea/skills`、`beautiful-prose`、`deep-reading-analyst` 等），形成一套从细读原著到句子抛光、从人物推演到伏笔管理的完整管线。

它和现有写作 skill 的**本质区别**：

| 现有写作 skill | 本体系 |
|---|---|
| 网络小说量产（扫榜→拆文→量产） | 严肃文学导向，一个场景一个场景地磨 |
| 类型小说脚手架（魔法系统、英雄之旅） | 关注句子层面的技艺、叙事声音、潜台词 |
| "写出来" | "推演出来"——作者是观测者，不是上帝 |
| 一次性生成 | 迭代式拟合——大纲是约束集合，不是铁轨 |

## 架构

```
literary-fanfic-orchestrator  (元 skill · 通用层)
    │
    ├── 路由：0-7 创作阶段 → 对应 craft skill
    ├── 约束：10 条通用创作原则（持续演化中）
    ├── 用户专属约束：你自己的偏好积累
    │
    └── 作品子 skill 索引
        │
        └── fanfic-你的作品名  (专属层，不在此仓库中)
            ├── 人物设定
            ├── 世界观
            ├── 大纲
            └── 专属约束
```

**元 skill 只做三件事：**
1. **路由** —— 你说"对话不对"，它知道调 `dialogue-mastery`；你说"句子太平"，它调 `beautiful-prose`
2. **约束** —— 通用创作原则 + 你的个人偏好，跨作品继承
3. **索引** —— 指向你的各个作品子 skill，创作时同时加载

**它不做的事：**
- 不包含任何具体作品的设定、人物或情节
- 不重复 craft skill 的内容（那些 skill 已经写好了）
- 不替代你的创作判断

## 方法论核心：10 条约束

约束是本体系的核心竞争力。这些不是"写作建议"——每一条都来自真实的创作推演过程中踩过的坑，是可操作、可验证的规则。

### 基约束（通用方法）

1. **尊重原著内核** —— 同人创作的自由在于"填补留白"，不是"改写设定"
2. **主题驱动** —— 情节服务于主题探索。主题是问题，不是答案
3. **潜台词优先** —— 不直说。信任读者
4. **去 AI 腔** —— 消灭 AI 模板句式（hedging、three-part lists、em dash 等）
5. **中文创作** —— Beautiful Prose 的英文约束转化为中文等效原则

### 核心约束（创作哲学）

6. **反刻意原则** —— 不要鬼鬼祟祟地"不经意"。大大方方写，不需要时不硬塞
6b. **明目张胆原则** —— 伏笔藏于明处。只要伏笔在当前的局部信息中有合理解释，读者就会自己帮我们把它归档为"已处理信息"
7. **推演者原则** —— 作者是观测者/推演者，不是上帝。输入初始条件，让角色自己"活过来"完成剧情
8. **大纲即约束集合** —— 大纲不是铁轨，是初始约束+边界条件+目标的总和。通过推演去拟合大纲，拟合不上就改大纲
9. **少即是多，元叙事应慎用** —— 环境已经变了，就不需要旁白说"穿越完成了"。相信读者

## 依赖

本元 skill 需要以下 craft skill 体系配合：

| 阶段 | 所需 skill | 来源 |
|---|---|---|
| 细读 | `deep-reading-analyst` | `npx skills-installer add @hacket/ClaudeCodeTips/deep-reading-analyst` |
| 人物 | `character-forge`, `voice-alchemy` | `npx @arcanea/skills` |
| 场景 | `scene-craft`, `dialogue-mastery` | `npx @arcanea/skills` |
| 结构 | `story-weave`, `world-build` | `npx @arcanea/skills` |
| 语言 | `beautiful-prose` | 见 [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) |
| 流程 | `creative-flow`, `bestiary-nav`, `centaur-mode` | `npx @arcanea/skills` |

## 快速开始

### 1. 安装依赖 skill

```bash
npx @arcanea/skills
npx skills-installer add @hacket/ClaudeCodeTips/deep-reading-analyst --client shared
# beautiful-prose 需手动安装到 ~/.claude/skills/beautiful-prose/
```

### 2. 安装本元 skill

```bash
mkdir -p ~/.claude/skills/literary-fanfic-orchestrator
cp path/to/this/repo/SKILL.md ~/.claude/skills/literary-fanfic-orchestrator/
```

重启 Claude Code 后，元 skill 自动激活。

### 3. 创建你的第一个作品子 skill

```bash
mkdir -p ~/.claude/skills/fanfic-你的作品名
```

子 skill 必须包含：
- 基本信息（原著、主角、一句话梗概）
- 人物设定
- 世界观设定
- 大纲或章节结构
- 作品专属约束（如有）

然后在元 skill 的「作品子 skill 索引」中添加一行指向它。

### 4. 开始创作

直接用自然语言描述你当前的需求——元 skill 会根据路由表自动调用对应的 craft skill。约束条件在全局生效，不需要每次重复。

## 为什么用这个？

- **避免每次遍历全部 skill** —— 你装了 30 个 skill，但不是每个都和"写对话"有关。元 skill 帮你路由
- **积累个人方法论** —— 你给出的每个约束（"不要这样写""应该那样处理"）都会被记下来，跨作品复用
- **人机协作而非 AI 代笔** —— 推演者原则确保你始终是创作的主体，AI 是观测和辅助的工具
- **版本控制友好** —— 全部 markdown，每次约束变更都可以 git diff

## 许可

MIT

## 贡献

欢迎分享你从实际创作中提炼的约束条件、路由规则优化建议，或改进作品子 skill 的模板结构。发 Issue 或 PR 即可。
