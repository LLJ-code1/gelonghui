# Fanbook 圈子观点采集与汇总设计

## 背景

Fanbook 圈子中的内容来自二次转发。帖子外层通常没有稳定发布日期，日期主要存在于截图内部，有些截图甚至没有日期。因此，本项目不能按截图内日期作为归档主线，而要按实际采集批次管理。

## 目标

- 定期采集 Fanbook 圈子 `最新` 流中的新增内容。
- 保存原始素材，确保观点可追溯。
- 从截图中识别来源作者、日期、标题和观点。
- 按实际采集日期生成每日汇总。
- 按 Fanbook 外层发帖人建立长期归档。

## 非目标

- 第一版不处理登录绕过、验证码或账号安全流程。
- 第一版不保证 OCR 100% 准确。
- 第一版不做完整金融事实核查，只整理来源观点。
- 第一版不反向分析 Fanbook 私有接口，优先使用浏览器可见内容。

## 核心规则

1. 文件归属按 `collection_date`，也就是实际运行日期。
2. 截图内日期只记录为 `inner_date_text`。
3. 增量判断按断点，不按截图内日期。
4. 断点记录上一轮最顶部帖子。
5. 下一轮从顶部往下扫，遇到上一轮顶部帖子即停止。
6. 素材留存和日报输出同步进行。
7. 作者归档按外层发帖人，截图内作者只作为来源元数据。

## 数据流

```text
Fanbook 最新流
  -> 批次采集
  -> 原始截图保存
  -> OCR 文本
  -> 结构化记录
  -> 去重与断点更新
  -> 作者归档
  -> 每日观点汇总
```

## 目录设计

```text
data/raw/YYYY-MM-DD/
data/ocr/YYYY-MM-DD/
data/structured/YYYY-MM-DD/
outputs/daily/
outputs/authors/
state/checkpoint.json
state/seen_items.json
docs/操作日志.md
```

## 数据模型

每条内容至少包含：

- `item_id`
- `batch_id`
- `collection_date`
- `collected_at`
- `source_position`
- `outer_author`
- `inner_author`
- `summary_author`
- `inner_date_text`
- `title`
- `market_tags`
- `topic_tags`
- `raw_image_paths`
- `ocr_text_path`
- `image_hash`
- `ocr_fingerprint`
- `duplicate_of`
- `status`
- `summary`
- `viewpoint`

## 断点设计

断点使用上一轮最顶部帖子作为锚点。这样下一轮只要从顶部扫到旧锚点，就可以停止。

匹配优先级：

1. 图片 hash
2. OCR 指纹
3. 外层作者 + 截图内作者 + 截图内日期 + 标题
4. 外层作者 + 标题 + 页面位置，作为弱匹配

## 输出设计

每日汇总结构：

```text
# YYYY-MM-DD 观点汇总

## 今日采集
## 今日主线
## 按市场分类
## 按作者汇总
## 共识观点
## 冲突观点
## 可转述话术
## 原始素材索引
```

作者归档结构：

```text
# 作者名

## YYYY-MM-DD

- 观点摘要
- 原始素材
- 相关市场/主题
```

## 错误处理

- 登录失效：停止采集，记录日志，等待手动登录。
- 断点缺失：有限范围继续扫描，标记 `checkpoint_missing`。
- OCR 失败：保留原图，状态为 `ocr_failed`。
- 重复内容：记录出现，但日报不重复总结。
- 作者冲突：同时保留外层作者和截图内作者，观点归档固定使用外层作者。

## 验收标准

- 每次运行都有批次记录。
- 每日汇总能追溯到原始截图。
- 下一轮能识别上一轮顶部断点。
- 同一天多次运行能合并到同一个日报。
- 作者归档能持续累积，不因截图内日期不同而分散。
