"""Fetch YouTube transcripts for experts listed in research/sources.md."""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

ROOT = Path(__file__).resolve().parent.parent
SOURCES_FILE = ROOT / "research" / "sources.md"
OUTPUT_DIR = ROOT / "research" / "youtube-transcripts"

YOUTUBE_EXPERTS = [
    {
        "name": "Jason Bay",
        "slug": "jason-bay",
        "channel_urls": [
            "https://www.youtube.com/@jasondbay/videos",
            "https://www.youtube.com/@JasonBayOutbound/videos",
            "https://www.youtube.com/@JasonBayOutbound",
        ],
    },
    {
        "name": "Eric Nowoslawski",
        "slug": "eric-nowoslawski",
        "channel_urls": [
            "https://www.youtube.com/@EricNowoslawski/videos",
            "https://www.youtube.com/@EricNowoslawski",
            "https://www.youtube.com/@GrowthEngineX/videos",
        ],
    },
    {
        "name": "Jed Mahrle",
        "slug": "jed-mahrle",
        "channel_urls": [
            "https://www.youtube.com/@PracticalProspecting/videos",
            "https://www.youtube.com/@PracticalProspecting",
        ],
    },
]

RECENT_VIDEO_COUNT = 3


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def get_recent_videos(channel_urls: list[str], limit: int = RECENT_VIDEO_COUNT) -> list[dict]:
    last_error = "No channel URLs provided"

    for channel_url in channel_urls:
        command = [
            sys.executable,
            "-m",
            "yt_dlp",
            "--flat-playlist",
            "--playlist-end",
            str(limit),
            "--print",
            "%(id)s|||%(title)s|||%(upload_date)s",
            channel_url,
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            last_error = result.stderr.strip() or "yt-dlp failed to fetch channel videos"
            continue

        videos: list[dict] = []
        for line in result.stdout.splitlines():
            if "|||" not in line:
                continue
            video_id, title, upload_date = line.split("|||", 2)
            videos.append(
                {
                    "id": video_id.strip(),
                    "title": title.strip(),
                    "upload_date": upload_date.strip(),
                }
            )
        if videos:
            return videos

    raise RuntimeError(last_error)


def format_upload_date(upload_date: str) -> str:
    if len(upload_date) == 8 and upload_date.isdigit():
        return f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
    return upload_date or "Unknown"


def fetch_transcript(video_id: str) -> str | None:
    api = YouTubeTranscriptApi()
    try:
        transcript = api.fetch(video_id, languages=["en", "en-US", "en-GB"])
    except Exception:
        try:
            transcript = api.fetch(video_id)
        except Exception:
            return None

    return "\n".join(snippet.text.strip() for snippet in transcript if snippet.text.strip())


def save_transcript(
    expert_slug: str,
    video: dict,
    transcript_text: str,
) -> Path:
    title_slug = slugify(video["title"])[:80] or video["id"]
    filename = f"{expert_slug}__{video['id']}__{title_slug}.md"
    output_path = OUTPUT_DIR / filename

    uploaded = format_upload_date(video["upload_date"])
    content = f"""# {video["title"]}

- **Expert slug:** {expert_slug}
- **Video ID:** {video["id"]}
- **Upload date:** {uploaded}
- **URL:** https://www.youtube.com/watch?v={video["id"]}
- **Fetched at:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}

## Transcript

{transcript_text}
"""
    output_path.write_text(content, encoding="utf-8")
    return output_path


def main() -> None:
    if not SOURCES_FILE.exists():
        raise FileNotFoundError(f"Missing sources file: {SOURCES_FILE}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    saved_files: list[Path] = []
    skipped: list[str] = []

    for expert in YOUTUBE_EXPERTS:
        print(f"Fetching recent videos for {expert['name']}...")
        try:
            videos = get_recent_videos(expert["channel_urls"], RECENT_VIDEO_COUNT)
        except RuntimeError as exc:
            print(f"  ! Could not fetch channel videos: {exc}")
            continue

        for video in videos:
            print(f"  - {video['title']} ({video['id']})")
            transcript_text = fetch_transcript(video["id"])
            if not transcript_text:
                skipped.append(f"{expert['name']} / {video['id']} / {video['title']}")
                continue
            saved_files.append(save_transcript(expert["slug"], video, transcript_text))

    print(f"\nSaved {len(saved_files)} transcript file(s) to {OUTPUT_DIR}")
    if skipped:
        print(f"Skipped {len(skipped)} video(s) without available transcripts:")
        for item in skipped:
            print(f"  - {item}")


if __name__ == "__main__":
    main()
