#!/usr/bin/env python3
"""Transcribe a local video with faster-whisper and save raw/corrected text."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

from faster_whisper import WhisperModel


@dataclass
class Segment:
    start: float
    end: float
    raw_text: str
    corrected_text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transcribe a local video file.")
    parser.add_argument("video", help="Input video file")
    parser.add_argument("--date", required=True, help="Archive date, e.g. 2026-05-24")
    parser.add_argument("--name", required=True, help="Stable output name")
    parser.add_argument("--title", default="", help="Human-readable title")
    parser.add_argument("--outer-author", default="", help="Fanbook outer author")
    parser.add_argument("--model", default="medium", help="faster-whisper model")
    parser.add_argument("--language", default="zh", help="Whisper language code")
    parser.add_argument("--duration", type=float, default=0, help="Optional seconds for sample runs")
    parser.add_argument("--corrections", default="data/video_terms_corrections.json")
    parser.add_argument("--output-root", default="data/video_transcripts")
    parser.add_argument("--tmp-root", default="tmp/video_transcribe")
    return parser.parse_args()


def safe_name(value: str) -> str:
    value = value.strip().replace(" ", "_")
    value = re.sub(r"[\\/:\*\?\"<>\|\s]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_")


def fmt_time(seconds: float) -> str:
    total = int(seconds)
    ms = int(round((seconds - total) * 100))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}.{ms:02d}"


def load_corrections(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Corrections file must be a JSON object: {path}")
    return {str(k): str(v) for k, v in data.items()}


def apply_corrections(text: str, corrections: dict[str, str]) -> str:
    for wrong, right in corrections.items():
        text = text.replace(wrong, right)
    return text


def run_ffmpeg(video: Path, audio: Path, duration: float) -> None:
    audio.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video),
    ]
    if duration > 0:
        cmd.extend(["-t", str(duration)])
    cmd.extend([
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(audio),
    ])
    subprocess.run(cmd, check=True)


def transcribe(audio: Path, model_name: str, language: str, corrections: dict[str, str]) -> tuple[list[Segment], dict]:
    model = WhisperModel(model_name, device="auto", compute_type="auto")
    segments_iter, info = model.transcribe(str(audio), language=language, vad_filter=True)
    segments: list[Segment] = []
    for index, seg in enumerate(segments_iter, start=1):
        raw = seg.text.strip()
        corrected = apply_corrections(raw, corrections)
        segments.append(Segment(round(seg.start, 2), round(seg.end, 2), raw, corrected))
        if index % 100 == 0:
            print(f"transcribed {index} segments, last={fmt_time(seg.end)}", flush=True)
    info_data = {
        "language": getattr(info, "language", ""),
        "language_probability": getattr(info, "language_probability", None),
        "duration": getattr(info, "duration", None),
    }
    return segments, info_data


def render_text(segments: list[Segment], field: str) -> str:
    lines = []
    for seg in segments:
        text = seg.raw_text if field == "raw_text" else seg.corrected_text
        lines.append(f"[{fmt_time(seg.start)} -> {fmt_time(seg.end)}] {text}")
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    video = Path(args.video)
    if not video.exists():
        print(f"Video not found: {video}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_root) / args.date
    output_dir.mkdir(parents=True, exist_ok=True)
    tmp_dir = Path(args.tmp_root)
    name = safe_name(args.name)
    model_name = safe_name(args.model)
    suffix = "sample" if args.duration > 0 else "full"
    base = f"{name}__{suffix}__{model_name}"
    audio = tmp_dir / f"{base}.wav"

    corrections_path = Path(args.corrections)
    corrections = load_corrections(corrections_path)

    print(f"extracting audio -> {audio}", flush=True)
    run_ffmpeg(video, audio, args.duration)

    print(f"transcribing with faster-whisper {args.model}", flush=True)
    segments, info_data = transcribe(audio, args.model, args.language, corrections)

    metadata = {
        "video_path": str(video),
        "date": args.date,
        "name": args.name,
        "title": args.title,
        "outer_author": args.outer_author,
        "model": args.model,
        "language": args.language,
        "duration_limit_seconds": args.duration or None,
        "corrections_file": str(corrections_path),
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "whisper_info": info_data,
        "segment_count": len(segments),
    }

    raw_path = output_dir / f"{base}__raw.txt"
    corrected_path = output_dir / f"{base}__corrected.txt"
    json_path = output_dir / f"{base}__segments.json"

    raw_path.write_text(render_text(segments, "raw_text"), encoding="utf-8")
    corrected_path.write_text(render_text(segments, "corrected_text"), encoding="utf-8")
    json_path.write_text(
        json.dumps({"metadata": metadata, "segments": [asdict(s) for s in segments]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"raw: {raw_path}")
    print(f"corrected: {corrected_path}")
    print(f"segments: {json_path}")
    print(f"segments_count: {len(segments)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
