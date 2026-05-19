# Author Viewpoint Waterfall Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the first version of author viewpoint waterfall output for Fanbook/格隆汇, using 2026-05-19 data to generate author daily snapshots and upgraded author Markdown for 王炽、周阳、herry.

**Architecture:** Keep the existing Markdown + JSONL local-file workflow. `data/structured/YYYY-MM-DD/items.jsonl` remains the item source of truth; new `data/author_daily/YYYY-MM-DD.jsonl` stores one author daily snapshot per author; `outputs/authors/作者.md` renders those snapshots as a readable timeline. Existing dirty collection outputs must be preserved and worked with, not reverted.

**Tech Stack:** Markdown, JSONL, shell validation with `python3 -m json.tool` / JSONL parsing, existing Git workflow.

---

### Task 1: Add Author Daily Snapshot Template

**Files:**
- Create: `templates/author_daily_record_template.json`
- Verify: `python3 -m json.tool templates/author_daily_record_template.json`

- [ ] **Step 1: Create template JSON**

Create `templates/author_daily_record_template.json` with this exact structure:

```json
{
  "author": "王炽",
  "date": "2026-05-19",
  "batch_ids": ["2026-05-19_1034"],
  "item_ids": ["2026-05-19_1034_005"],
  "source_status": "summarized",
  "confidence": "high",
  "today_conclusion": "市场进入震荡阶段，量能不过分萎缩时仍有轮动机会。",
  "focus": ["CPO", "OCS", "硅光", "英伟达财报"],
  "bullish": ["有产业节点催化的光通信方向"],
  "cautious": ["高位追涨", "缺少事件验证的科技题材"],
  "operation": ["降低追高", "控仓低吸", "等产业节点确认"],
  "change_vs_previous": "延续前一轮科技分化判断，但更强调震荡和低吸节奏。",
  "watchlist": ["英伟达财报后光通信链反馈", "OCS/硅光产业节点是否继续发酵"],
  "raw_evidence": [
    {
      "item_id": "2026-05-19_1034_005",
      "ocr_text_path": "data/ocr/2026-05-19/2026-05-19_1034_005.txt",
      "raw_image_paths": ["data/raw/2026-05-19/2026-05-19_1034_screen_001_D1.png"]
    }
  ],
  "review_note": "已打开详情页视觉复核。"
}
```

- [ ] **Step 2: Validate template JSON**

Run:

```bash
python3 -m json.tool templates/author_daily_record_template.json
```

Expected: command exits 0 and prints formatted JSON.

### Task 2: Create 2026-05-19 Author Daily JSONL

**Files:**
- Create: `data/author_daily/2026-05-19.jsonl`
- Read: `data/structured/2026-05-19/items.jsonl`
- Verify: JSONL parsing command below

- [ ] **Step 1: Read source records for sample authors**

Run:

```bash
python3 -c "import json; p='data/structured/2026-05-19/items.jsonl'; rows=[json.loads(x) for x in open(p, encoding='utf-8') if x.strip()]; print(len(rows)); [print(r['item_id'], r['summary_author'], r['status'], r['title']) for r in rows if r['summary_author'] in {'王炽','周阳','herry'}]"
```

Expected: prints 10 total rows and rows for `周阳`、`王炽`、`herry`.

- [ ] **Step 2: Create author daily JSONL**

Create `data/author_daily/2026-05-19.jsonl` with three rows:

```jsonl
{"author":"王炽","date":"2026-05-19","batch_ids":["2026-05-19_1034"],"item_ids":["2026-05-19_1034_005"],"source_status":"summarized","confidence":"high","today_conclusion":"市场进入震荡阶段，量能不过分萎缩时仍有轮动机会。","focus":["CPO","OCS","硅光","英伟达财报"],"bullish":["有产业节点催化的光通信方向","震荡中仍有轮动机会的科技细分"],"cautious":["高位追涨","缺少事件验证的科技题材"],"operation":["降低追高","控仓低吸","等产业节点确认"],"change_vs_previous":"延续5月18日科技分化判断，但更强调市场进入震荡后要降低追高、等待低吸和产业节点确认。","watchlist":["英伟达财报后光通信链反馈","OCS/硅光产业节点是否继续发酵","市场量能是否明显萎缩"],"raw_evidence":[{"item_id":"2026-05-19_1034_005","ocr_text_path":"data/ocr/2026-05-19/2026-05-19_1034_005.txt","raw_image_paths":["data/raw/2026-05-19/2026-05-19_1034_screen_001_D1.png"]}],"review_note":"本条在2026-05-19日报中标记为summarized，可写入强观点。"}
{"author":"周阳","date":"2026-05-19","batch_ids":["2026-05-19_1034"],"item_ids":["2026-05-19_1034_004"],"source_status":"summarized","confidence":"high","today_conclusion":"海外科技调整预计会传导到国内，半导体短期可能回落，机器人可能成为阶段性接力方向。","focus":["海外科技映射","半导体回落","机器人接力","A股科技轮动"],"bullish":["机器人阶段性接力方向","调整后仍有产业逻辑支撑的科技链"],"cautious":["海外科技调整对A股科技的负反馈","短期半导体回落压力"],"operation":["降低对半导体短期追高","观察机器人承接强度","等待海外科技波动释放"],"change_vs_previous":"相比5月18日继续关注海外科技映射，但5月19日更明确提示海外调整会传导国内，并把机器人作为可能接力方向。","watchlist":["海外科技是否继续调整","机器人板块能否持续承接资金","半导体回落后的修复强度"],"raw_evidence":[{"item_id":"2026-05-19_1034_004","ocr_text_path":"data/ocr/2026-05-19/2026-05-19_1034_004.txt","raw_image_paths":["data/raw/2026-05-19/2026-05-19_1034_screen_001_D1.png"]}],"review_note":"本条在2026-05-19日报中标记为summarized，可写入强观点。"}
{"author":"herry","date":"2026-05-19","batch_ids":["2026-05-19_1034"],"item_ids":["2026-05-19_1034_007","2026-05-19_1034_010"],"source_status":"needs_review","confidence":"low","today_conclusion":"可确认herry继续围绕算力链、英伟达、商业航天/SST、碳化硅和AI电源展开，但当天关键内容仍需补原图或局部放大复核。","focus":["算力链","英伟达","商业航天/SST","碳化硅","AI电源"],"bullish":[],"cautious":["多主题产业长图文字过密","碳化硅卡片未打开原图细节"],"operation":["先作为待复核素材保留","不纳入强观点","后续补原图后再判断是否转为summarized"],"change_vs_previous":"延续5月18日对碳化硅和AI电源空间的关注，但5月19日缺少足够清晰原图复核，不能判断观点是否明显加强或转向。","watchlist":["补开herry多主题产业长图原图","复核碳化硅卡片细节","确认AI电源空间论证是否延续"],"raw_evidence":[{"item_id":"2026-05-19_1034_007","ocr_text_path":"data/ocr/2026-05-19/2026-05-19_1034_007.txt","raw_image_paths":["data/raw/2026-05-19/2026-05-19_1034_screen_001_D1.png"]},{"item_id":"2026-05-19_1034_010","ocr_text_path":"data/ocr/2026-05-19/2026-05-19_1034_010.txt","raw_image_paths":["data/raw/2026-05-19/2026-05-19_1034_screen_001_D1.png"]}],"review_note":"两条源记录均为needs_review，只写可确认主题和待复核，不写强结论。"}
```

- [ ] **Step 3: Validate author daily JSONL**

Run:

```bash
python3 -c "import json; p='data/author_daily/2026-05-19.jsonl'; rows=[json.loads(x) for x in open(p, encoding='utf-8') if x.strip()]; assert len(rows)==3; assert {r['author'] for r in rows}=={'王炽','周阳','herry'}; assert [r for r in rows if r['author']=='herry'][0]['confidence']=='low'; print('author_daily ok', len(rows))"
```

Expected: `author_daily ok 3`.

### Task 3: Upgrade Three Author Files to Waterfall Format

**Files:**
- Modify: `outputs/authors/王炽.md`
- Modify: `outputs/authors/周阳.md`
- Modify: `outputs/authors/herry.md`
- Read: `data/author_daily/2026-05-19.jsonl`

- [ ] **Step 1: Upgrade `outputs/authors/王炽.md`**

Rewrite the top of `outputs/authors/王炽.md` into:

```markdown
# 王炽观点瀑布流

## 作者画像

- 长期关注：CPO、OCS、硅光、光模块、科技分化（待继续验证）
- 风格：偏交易节奏 + 产业催化
- 常见判断维度：市场阶段、量能、事件催化、仓位
- 主要风险：高位追涨、产业节点不及预期

## 最新状态

- 当前主线：科技进入震荡和分化后，继续围绕 CPO、OCS、硅光、英伟达财报做节点观察。
- 最近变化：从 5 月 18 日强调科技普涨结束，转为 5 月 19 日强调震荡中控仓低吸。
- 当前风险：追高、量能萎缩、英伟达财报不及预期。
- 下一步跟踪：英伟达财报后光通信链反馈，OCS/硅光节点是否继续发酵。

## 观点时间线

### 2026-05-19

#### 今日结论

市场进入震荡阶段，量能不过分萎缩时仍有轮动机会。

#### 关注什么

- CPO
- OCS
- 硅光
- 英伟达财报

#### 看好什么

- 有产业节点催化的光通信方向。
- 震荡中仍有轮动机会的科技细分。

#### 不看好/谨慎什么

- 高位追涨。
- 缺少事件验证的科技题材。

#### 操作含义

- 降低追高。
- 控仓低吸。
- 等产业节点确认。

#### 相比上一轮变化

延续 5 月 18 日科技分化判断，但更强调市场进入震荡后要降低追高、等待低吸和产业节点确认。

#### 待跟踪

- 英伟达财报后光通信链反馈。
- OCS/硅光产业节点是否继续发酵。
- 市场量能是否明显萎缩。

#### 原始素材

- `2026-05-19_1034_005`，状态：`summarized`
- OCR：`data/ocr/2026-05-19/2026-05-19_1034_005.txt`
- 素材：`data/raw/2026-05-19/2026-05-19_1034_screen_001_D1.png`

## 历史素材索引
```

Then keep existing older date sections under `## 历史素材索引`, preserving their content.

- [ ] **Step 2: Upgrade `outputs/authors/周阳.md`**

Use the same structure and these 2026-05-19 fields:

- 作者画像长期关注：海外科技映射、A股科技轮动、半导体、机器人。
- 当前主线：海外科技调整传导国内，机器人可能成为阶段性接力。
- 今日结论：海外科技调整预计会传导到国内，半导体短期可能回落，机器人可能成为阶段性接力方向。
- 关注什么：海外科技映射、半导体回落、机器人接力、A股科技轮动。
- 看好什么：机器人阶段性接力方向；调整后仍有产业逻辑支撑的科技链。
- 谨慎什么：海外科技调整对A股科技的负反馈；短期半导体回落压力。
- 操作含义：降低对半导体短期追高；观察机器人承接强度；等待海外科技波动释放。
- 相比上一轮变化：相比5月18日继续关注海外科技映射，但5月19日更明确提示海外调整会传导国内，并把机器人作为可能接力方向。
- 原始素材：`2026-05-19_1034_004`。

- [ ] **Step 3: Upgrade `outputs/authors/herry.md`**

Use the same structure but reflect `needs_review`:

- 作者画像长期关注：碳化硅、AI电源、算力链、户储、产业空间。
- 当前主线：继续围绕碳化硅/AI电源和算力链，但5月19日关键内容需要补原图。
- 今日结论：可确认herry继续围绕算力链、英伟达、商业航天/SST、碳化硅和AI电源展开，但当天关键内容仍需补原图或局部放大复核。
- 关注什么：算力链、英伟达、商业航天/SST、碳化硅、AI电源。
- 看好什么：不写强结论，写“待复核后确认”。
- 谨慎什么：多主题产业长图文字过密；碳化硅卡片未打开原图细节。
- 操作含义：先作为待复核素材保留；不纳入强观点；后续补原图后再判断是否转为 `summarized`。
- 相比上一轮变化：延续5月18日对碳化硅和AI电源空间的关注，但5月19日缺少足够清晰原图复核，不能判断观点是否明显加强或转向。
- 原始素材：`2026-05-19_1034_007`、`2026-05-19_1034_010`，状态均为 `needs_review`。

### Task 4: Update Workflow Docs and Operation Log

**Files:**
- Modify: `docs/流程说明.md`
- Modify: `AGENTS.md`
- Modify: `docs/操作日志.md`

- [ ] **Step 1: Update `docs/流程说明.md` output layer**

Add author waterfall output to the output section:

```markdown
   - 作者每日快照：`data/author_daily/YYYY-MM-DD.jsonl`
   - 作者观点瀑布流：`outputs/authors/作者.md`
```

- [ ] **Step 2: Update `AGENTS.md` default flow**

Change the output update step so it includes `data/author_daily/`:

```markdown
6. 更新 `data/ocr/`、`data/structured/`、`data/author_daily/`、`outputs/daily/`、`outputs/authors/`、`docs/操作日志.md`、`state/checkpoint.json`。
```

- [ ] **Step 3: Append operation log entry**

Append to `docs/操作日志.md`:

```markdown
### 作者观点瀑布流第一版设计落地

- 状态：`author_waterfall_v1_sample`
- 新增结构化层：`data/author_daily/2026-05-19.jsonl`
- 新增模板：`templates/author_daily_record_template.json`
- 样例作者：`王炽`、`周阳`、`herry`
- 处理原则：`summarized` 可以写入强观点；`needs_review` 只进入待复核素材，不进入看好/不看好/操作含义强字段。
- 输出方式：`outputs/authors/作者.md` 从帖子索引升级为观点瀑布流，最新日期在上，历史素材保留在下。
```

### Task 5: Verification and Commit

**Files:**
- Verify all files above.
- Commit only author waterfall implementation files plus any already-tracked files intentionally changed by this task. Do not stage unrelated dirty files that pre-existed this task unless they are required for the waterfall sample.

- [ ] **Step 1: Validate JSON template and JSONL**

Run:

```bash
python3 -m json.tool templates/author_daily_record_template.json
python3 -c "import json; rows=[json.loads(x) for x in open('data/author_daily/2026-05-19.jsonl', encoding='utf-8') if x.strip()]; assert len(rows)==3; print('author_daily ok', len(rows))"
```

Expected: both commands exit 0; second command prints `author_daily ok 3`.

- [ ] **Step 2: Check Markdown and whitespace**

Run:

```bash
git diff --check
python3 -c "from pathlib import Path; files=['templates/author_daily_record_template.json','data/author_daily/2026-05-19.jsonl','outputs/authors/王炽.md','outputs/authors/周阳.md','outputs/authors/herry.md','docs/流程说明.md','AGENTS.md','docs/操作日志.md']; bad=['待'+'生成','x'*3,'?'*2]; hits=[(f,b) for f in files for b in bad if b in Path(f).read_text(encoding='utf-8')]; assert not hits, hits; print('placeholder scan ok')"
```

Expected: `git diff --check` exits 0; placeholder scan prints `placeholder scan ok`.

- [ ] **Step 3: Inspect staged scope before commit**

Run:

```bash
git status --short
git diff --cached --stat
```

Expected: staged files are limited to:

- `templates/author_daily_record_template.json`
- `data/author_daily/2026-05-19.jsonl`
- `outputs/authors/王炽.md`
- `outputs/authors/周阳.md`
- `outputs/authors/herry.md`
- `docs/流程说明.md`
- `AGENTS.md`
- `docs/操作日志.md`

- [ ] **Step 4: Commit and push**

Run:

```bash
git commit -m "feat: add author viewpoint waterfall sample"
git push
```

Expected: commit succeeds and push updates `origin/main`.

---

## Self-Review

- Spec coverage: covers `data/author_daily`, author Markdown waterfall, `needs_review` safety, sample authors, docs and operation log.
- Placeholder scan: no unresolved placeholders should remain after the plan edits.
- Scope: first implementation is intentionally limited to one date and three sample authors; full automation can be a later task after format approval.
