# Codex 操作规则

## 触发词

用户说以下任一句时，默认启动 Fanbook/格隆汇最新观点采集流程：

- `整理一下最新观点`
- `整理一下最新的观点`
- `整理最新观点`
- `更新最新观点`
- `跑一轮最新观点`

这里的“最新观点”不是指整理本地已有日报或精简版，而是指打开 Fanbook 圈子 `最新` 流，从顶部开始按 checkpoint 采集新增内容。

## 默认执行流程

1. 读取 `state/checkpoint.json`，确认上一轮断点。
2. 使用 Chrome 访问 `https://web.fanbook.cn/channels/887510463079116800/circle?sort=publish`。
3. 从 `最新` 顶部开始，只读采集新增帖子，扫到上一轮 checkpoint 停止。
4. 按 Fanbook 外层作者归档；截图内作者只作为 `inner_author` 元数据。
5. 长图、密集文字图、首屏缩略图必须打开原图或详情图复核后，才能写成强观点。
6. 更新 `data/ocr/`、`data/structured/`、`outputs/daily/`、`outputs/authors/`、`docs/操作日志.md`、`state/checkpoint.json`。
7. 不在 Fanbook 发布、发送、删除、上传或修改任何内容。

如果用户明确说“只看本地已有内容”或“不要打开 Fanbook”，才改成本地整理。
