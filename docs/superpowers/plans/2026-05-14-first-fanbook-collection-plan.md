# First Fanbook Collection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run the first Fanbook circle collection with no existing checkpoint, stopping when screenshot content first shows yesterday's date.

**Architecture:** This first run is a semi-automated browser-assisted collection. The browser provides visible cards and screenshots; project files preserve raw evidence, structured records, the first checkpoint, author notes, and the daily summary.

**Tech Stack:** Chrome extension browser control, Markdown docs, JSON/JSONL records, local filesystem evidence storage, Git for project history.

---

## File Structure

- Modify: `/Users/a123/Downloads/格隆汇观点汇总/docs/流程说明.md`
  Records the first-run no-checkpoint stopping rule.
- Modify: `/Users/a123/Downloads/格隆汇观点汇总/docs/断点规则.md`
  Defines how first-run temporary stopping works before checkpoint exists.
- Modify: `/Users/a123/Downloads/格隆汇观点汇总/docs/操作日志.md`
  Logs the rule decision and first-run outcome.
- Create: `/Users/a123/Downloads/格隆汇观点汇总/data/raw/2026-05-14/`
  Stores full visible screenshots and card-level screenshots when available.
- Create: `/Users/a123/Downloads/格隆汇观点汇总/data/ocr/2026-05-14/`
  Stores recognized text from screenshots.
- Create: `/Users/a123/Downloads/格隆汇观点汇总/data/structured/2026-05-14/items.jsonl`
  Stores one JSON object per collected item.
- Create: `/Users/a123/Downloads/格隆汇观点汇总/outputs/daily/2026-05-14_观点汇总.md`
  Stores the first daily summary.
- Create or modify: `/Users/a123/Downloads/格隆汇观点汇总/outputs/authors/*.md`
  Stores author-based accumulated notes.
- Create: `/Users/a123/Downloads/格隆汇观点汇总/state/checkpoint.json`
  Stores the first top-item checkpoint.

---

### Task 1: Record First-Run Rule

**Files:**
- Modify: `/Users/a123/Downloads/格隆汇观点汇总/docs/流程说明.md`
- Modify: `/Users/a123/Downloads/格隆汇观点汇总/docs/断点规则.md`
- Modify: `/Users/a123/Downloads/格隆汇观点汇总/docs/操作日志.md`

- [ ] **Step 1: Add first-run rule to process docs**

Add this rule:

```markdown
首次采集没有 `state/checkpoint.json` 时，从 `最新` 流顶部开始识别；当截图内部明确出现昨天日期时停止。截图无日期、日期识别不清、只有外层页面信息时，不作为停止条件。
```

- [ ] **Step 2: Verify no placeholder text remains**

Run:

```bash
rg -n "TODO|TBD|待生成|待确认|FIXME|xxx" README.md docs/*.md templates state/checkpoint.example.json
```

Expected: no output.

- [ ] **Step 3: Commit docs update**

Run:

```bash
git add docs/流程说明.md docs/断点规则.md docs/操作日志.md docs/superpowers/plans/2026-05-14-first-fanbook-collection-plan.md
git commit -m "docs: add first Fanbook collection plan"
```

Expected: commit succeeds.

---

### Task 2: Capture First Batch Evidence

**Files:**
- Create: `/Users/a123/Downloads/格隆汇观点汇总/data/raw/2026-05-14/`
- Create: `/Users/a123/Downloads/格隆汇观点汇总/data/structured/2026-05-14/items.jsonl`
- Create: `/Users/a123/Downloads/格隆汇观点汇总/state/checkpoint.json`

- [ ] **Step 1: Open Fanbook latest feed**

Open:

```text
https://web.fanbook.cn/channels/887510463079116800/circle?sort=publish
```

Expected: the `最新` tab is selected.

- [ ] **Step 2: Capture top visible screen**

Save the visible screenshot to:

```text
data/raw/2026-05-14/2026-05-14_first_batch_screen_001.png
```

Expected: screenshot shows the top of the `最新` feed.

- [ ] **Step 3: Identify current top item**

Record the top item as:

```json
{
  "source_position": 1,
  "outer_author": "visible outer author",
  "inner_author": "recognized screenshot author",
  "inner_date_text": "recognized screenshot date",
  "title": "recognized title or first line",
  "image_hash": "sha256 of screenshot/card image",
  "ocr_fingerprint": "fingerprint of recognized text"
}
```

Expected: fields are specific to the real top item, not template examples.

- [ ] **Step 4: Continue until yesterday date appears**

Scroll downward and inspect screenshots. Stop when screenshot content clearly shows one of:

```text
5月13日
5月13
2026-05-13
20260513
```

Expected: items above this stop line are treated as first-batch candidates.

- [ ] **Step 5: Write structured records**

Write `/Users/a123/Downloads/格隆汇观点汇总/data/structured/2026-05-14/items.jsonl` with one JSON object per collected item. Each object must include:

```json
{
  "item_id": "2026-05-14_first_001",
  "batch_id": "2026-05-14_first",
  "collection_date": "2026-05-14",
  "collected_at": "2026-05-14T00:00:00+08:00",
  "feed_sort": "latest",
  "source_url": "https://web.fanbook.cn/channels/887510463079116800/circle?sort=publish",
  "source_position": 1,
  "outer_author": "",
  "inner_author": "",
  "inner_date_text": "",
  "title": "",
  "market_tags": [],
  "topic_tags": [],
  "raw_image_paths": [],
  "ocr_text_path": "",
  "image_hash": "",
  "ocr_fingerprint": "",
  "duplicate_of": null,
  "status": "captured",
  "summary": "",
  "viewpoint": "",
  "evidence_note": ""
}
```

Expected: JSONL parses successfully line by line.

- [ ] **Step 6: Write checkpoint**

Write `/Users/a123/Downloads/格隆汇观点汇总/state/checkpoint.json` using the first real top item.

Expected: next run can stop when it sees this item.

---

### Task 3: Produce First Daily Summary

**Files:**
- Create: `/Users/a123/Downloads/格隆汇观点汇总/outputs/daily/2026-05-14_观点汇总.md`
- Create or modify: `/Users/a123/Downloads/格隆汇观点汇总/outputs/authors/*.md`
- Modify: `/Users/a123/Downloads/格隆汇观点汇总/docs/操作日志.md`

- [ ] **Step 1: Draft daily summary**

Create:

```markdown
# 2026-05-14 观点汇总

## 今日采集

## 今日主线

## 按市场分类

## 按作者汇总

## 共识观点

## 冲突观点

## 可转述话术

## 原始素材索引
```

Expected: the summary references collected item IDs and raw screenshot paths.

- [ ] **Step 2: Update author archives**

For each recognized `inner_author`, create or update:

```text
outputs/authors/<作者名>.md
```

Expected: each author note includes date, item ID, summary, and evidence path.

- [ ] **Step 3: Log first run**

Append to `/Users/a123/Downloads/格隆汇观点汇总/docs/操作日志.md`:

```markdown
### 首次采集执行

- 状态：initial_stop_by_yesterday_inner_date
- 采集日期：2026-05-14
- 批次：2026-05-14_first
- 停止条件：截图内部首次出现昨天日期
- 输出：outputs/daily/2026-05-14_观点汇总.md
```

Expected: log records what happened and where outputs are stored.

- [ ] **Step 4: Verify files**

Run:

```bash
find data outputs state docs -maxdepth 3 -type f | sort
python3 -m json.tool state/checkpoint.json
python3 - <<'PY'
import json
from pathlib import Path
for line in Path("data/structured/2026-05-14/items.jsonl").read_text().splitlines():
    if line.strip():
        json.loads(line)
print("items.jsonl ok")
PY
```

Expected: files exist, checkpoint JSON is valid, JSONL check prints `items.jsonl ok`.

- [ ] **Step 5: Commit first collection**

Run:

```bash
git add docs data/structured outputs state/checkpoint.example.json templates README.md
git add -f state/checkpoint.json
git commit -m "data: add first Fanbook collection"
```

Expected: commit succeeds. Raw screenshots may remain untracked if `.gitignore` excludes them.

---

## Self-Review

- Spec coverage: the plan covers first-run stop logic, evidence capture, structured records, checkpoint creation, daily summary, author archive, logging, and verification.
- Placeholder scan: examples use explicit sample strings; real execution steps require replacing them with captured values.
- Type consistency: field names match `/Users/a123/Downloads/格隆汇观点汇总/docs/字段说明.md` and `/Users/a123/Downloads/格隆汇观点汇总/templates/item_record_template.json`.
