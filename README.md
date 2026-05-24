# 格隆汇观点汇总

这是一个本地投研内容处理项目，一级项目是 `格隆汇观点汇总`，下面分为两个二级子项目：

```text
格隆汇观点汇总
  -> 文字版本：Fanbook 圈子最新观点采集、OCR、结构化、日报、作者归档
  -> 视频版本：Fanbook 视频频道网盘链接保存、保存清单、视频断点
```

两个子项目共用同一个 Fanbook 来源和本地仓库，但执行流程、checkpoint、输出文件和说明文档都分开维护。

## 文字版本

用途：把 Fanbook 圈子 `最新` 流里的二次转发观点沉淀成可追溯的文字资料库。

流水线：

```text
Fanbook 最新流 -> 截图留存 -> OCR/人工识别 -> 结构化记录 -> 日报 -> 作者归档 -> 断点续跑
```

触发词：

- `整理一下最新观点`
- `整理一下最新的观点`
- `整理最新观点`
- `更新最新观点`
- `跑一轮最新观点`

核心文件：

- [docs/文字版本/流程说明.md](docs/文字版本/流程说明.md)
- [docs/文字版本/字段说明.md](docs/文字版本/字段说明.md)
- [docs/文字版本/断点规则.md](docs/文字版本/断点规则.md)
- [docs/文字版本/建设路线.md](docs/文字版本/建设路线.md)
- [docs/文字版本/操作日志.md](docs/文字版本/操作日志.md)
- `state/checkpoint.json`
- `data/structured/`
- `data/author_daily/`
- `outputs/daily/`
- `outputs/authors/`

## 视频版本

用途：把 Fanbook `#视频` 频道里的夸克网盘视频保存到用户夸克网盘的 `格隆汇/当天日期` 文件夹，并保留保存记录。

流水线：

```text
Fanbook #视频 -> 识别网盘链接 -> 打开夸克分享页 -> 选择目标日期目录 -> 保存到网盘 -> 保存清单 -> 视频断点
```

触发词：

- `保存最新视频`
- `跑一轮视频保存`
- `保存格隆汇视频`
- `跑一下最新的视频`

核心文件：

- [docs/视频版本/流程说明.md](docs/视频版本/流程说明.md)
- [docs/视频版本/操作日志.md](docs/视频版本/操作日志.md)
- `state/video_checkpoint.json`
- `data/video_links/`
- `outputs/video/`

## 总入口

1. [AGENTS.md](AGENTS.md)：Codex 操作规则和触发词分流。
2. [docs/项目总览.md](docs/项目总览.md)：一级项目总览和两个子项目关系。
3. 按任务选择 `docs/文字版本/` 或 `docs/视频版本/`。

## 当前规则

- 文字版本按实际采集日期归档，不按截图内部日期归档。
- 文字版本按 Fanbook 外层发帖人归档，截图内作者只作为来源备注。
- 视频版本按实际保存日期记录，默认保存到夸克网盘 `全部文件/格隆汇/YY.M.DD`。
- 两个子项目不混用 checkpoint：文字用 `state/checkpoint.json`，视频用 `state/video_checkpoint.json`。
- 两个子项目不混用输出：文字进 `outputs/daily/` 和 `outputs/authors/`，视频进 `outputs/video/`。
