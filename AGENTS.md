# Codex 操作规则

## 项目层级

本仓库一级项目是 `格隆汇观点汇总`，下面分两个二级子项目：

1. `文字版本`：Fanbook 圈子 `最新` 流里的观点截图采集、OCR、结构化、日报和作者归档。
2. `视频版本`：Fanbook `#视频` 频道里的网盘视频链接识别、保存、本地下载、转写、观点整理和画面复核。

两个子项目必须分开执行、分开记录、分开维护文档。不要把视频保存流程写进文字观点流程，也不要把文字观点日报写进视频保存清单。

## 文字版本触发词

用户说以下任一句时，默认启动 Fanbook/格隆汇文字版最新观点采集流程：

- `整理一下最新观点`
- `整理一下最新的观点`
- `整理最新观点`
- `更新最新观点`
- `跑一轮最新观点`

这里的“最新观点”不是指整理本地已有日报或精简版，而是指打开 Fanbook 圈子 `最新` 流，从顶部开始按 checkpoint 采集新增内容。

### 文字版本默认执行流程

1. 读取 `state/checkpoint.json`，确认上一轮断点。
2. 使用 Chrome 访问 `https://web.fanbook.cn/channels/887510463079116800/circle?sort=publish`。
3. 从 `最新` 顶部开始，只读采集新增帖子，扫到上一轮 checkpoint 停止。
4. 按 Fanbook 外层作者归档；截图内作者只作为 `inner_author` 元数据。
5. 长图、密集文字图、首屏缩略图必须打开原图或详情图复核后，才能写成强观点。
6. 多图/轮播帖必须逐张打开、保存和复核；只复核第一张时，不得把整帖写成完整观点。
7. 长图要区分缩略图、裁切图和完整原图；URL 或素材带 `thumbnail`、`cut` 等裁切痕迹时，必须补抓无裁切原图或详情图后再引用细节。
8. 本轮产生的 `needs_review` 必须进入复核清单；用户要求“待复核都要做”时，必须逐条补复核到 `summarized` 或明确说明无法完成的原因。
9. 更新 `data/ocr/`、`data/structured/`、`data/author_daily/`、`outputs/daily/`、`outputs/authors/`、`docs/文字版本/操作日志.md`、`state/checkpoint.json`。
10. 不在 Fanbook 发布、发送、删除、上传或修改任何内容。

如果用户明确说“只看本地已有内容”或“不要打开 Fanbook”，才改成本地整理。

## 视频版本触发词

用户说以下任一句时，默认启动 Fanbook/格隆汇视频保存流程：

- `保存最新视频`
- `跑一轮视频保存`
- `保存格隆汇视频`

用户说以下任一句时，默认启动 Fanbook/格隆汇视频内容整理流程，但执行前必须先向用户复述本轮流程、目标日期、输出位置和是否会访问 Fanbook/夸克，等用户确认后再开始：

- `跑一下最新的视频`

这里的“视频”指 Fanbook `#视频` 频道里的网盘分享，不是圈子 `最新` 观点流。`保存最新视频` 只做保存；`跑一下最新的视频` 默认走保存、下载、转写、观点整理、画面复核的完整链路。

### 视频保存默认执行流程

1. 读取 `state/video_checkpoint.json`，确认上一轮视频断点。
2. 使用 Chrome 访问 `https://web.fanbook.cn/channels/887510463079116800/887585348161761280`。
3. 从顶部开始识别新增消息，扫到上一轮视频断点停止。
4. 只处理 `https://pan.quark.cn/s/` 开头的夸克链接。
5. 腾讯会议、其他网盘或非视频链接只记录，不执行保存。
6. 打开夸克分享页，确认文件名、大小、修改时间。
7. 先在分享页底部选择 `转存至：全部文件/格隆汇/YY.M.DD`，确认目标目录后再点 `保存到网盘`。
8. 页面出现 `保存成功` 且 `已保存至：YY.M.DD` 后，记录为 `saved_to_target`。
9. 更新 `data/video_links/`、`outputs/video/`、`docs/视频版本/操作日志.md`、`state/video_checkpoint.json`。
10. 不在 Fanbook 发布、发送、删除、上传或修改任何内容；不删除、分享、重命名网盘文件。

### 视频内容整理默认执行流程

当用户说 `跑一下最新的视频`：

1. 先回复本轮流程说明，不直接操作：
   - 读取 `state/video_checkpoint.json`。
   - 访问 Fanbook `#视频`，从顶部扫到上一轮视频断点。
   - 识别新增夸克视频链接并保存到夸克 `全部文件/格隆汇/YY.M.DD`。
   - 下载到本地 `data/video_files/YYYY-MM-DD/`。
   - 使用 faster-whisper `medium` 转写。
   - 生成音频观点整理、画面复核候选、抽帧复核结果和最终整理稿。
   - 所有素材和输出按 `YYYY-MM-DD` 归档。
2. 等用户确认后，才执行 Fanbook/夸克访问、保存、下载、转写和整理。
3. 每个视频只创建一个按日期归档的视频任务包，不要在仓库根目录或 docs 里散落临时文件。
4. 目录规范：
   - 网盘链接：`data/video_links/YYYY-MM-DD.jsonl`
   - 下载记录：`data/video_downloads/YYYY-MM-DD.jsonl`
   - 本地视频：`data/video_files/YYYY-MM-DD/`
   - 转写稿：`data/video_transcripts/YYYY-MM-DD/{video_key}__*.txt/json`
   - 结构化观点：`data/video_structured/YYYY-MM-DD/{video_key}__*.json`
   - 复核截帧：`data/video_frames/YYYY-MM-DD/{video_key}/`
   - 当日清单：`outputs/video/YYYY-MM-DD_保存清单.md`
   - 视频整理稿：`outputs/video/YYYY-MM-DD_{video_key}_视频观点整理.md`
5. 视频内容整理状态必须明确区分：
   - `saved_to_target`
   - `downloaded`
   - `transcribed`
   - `audio_summarized_needs_visual_review`
   - `visual_reviewed_partial`
   - `visual_reviewed`

## 操作要点沉淀

执行过程中如果发现新的操作差异、例外情况或更稳妥的处理办法，先完成当前采集或修正，再提示用户是否要沉淀进对应子项目文档：

- 文字版本：`docs/文字版本/流程说明.md`
- 视频版本：`docs/视频版本/流程说明.md`

提示格式建议：

> 这次发现一个新的操作要点：……。是否要整理进说明文档，作为下次默认规则？
