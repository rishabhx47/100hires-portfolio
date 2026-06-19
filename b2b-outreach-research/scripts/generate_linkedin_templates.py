"""Generate LinkedIn post collection templates for each expert in sources.md."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES_FILE = ROOT / "research" / "sources.md"
OUTPUT_DIR = ROOT / "research" / "linkedin-posts"

TEMPLATES_PER_EXPERT = 3


def parse_experts(sources_text: str) -> list[dict]:
    pattern = re.compile(
        r"^\d+\.\s+\*\*(.+?)\*\*\s*\n"
        r"(?:\s+-\s+\*Focus:\*\s*(.+?)\s*\n)?"
        r"\s+-\s+\*Links:\*\s*(.+?)\s*\n"
        r"\s+-\s+\*Why chosen:\*\s*(.+?)(?=\n\n|\Z)",
        re.MULTILINE | re.DOTALL,
    )

    experts: list[dict] = []
    for match in pattern.finditer(sources_text):
        name = match.group(1).strip()
        focus = (match.group(2) or "").strip()
        links = match.group(3).strip()
        why_chosen = match.group(4).strip()

        linkedin_match = re.search(r"\[LinkedIn\]\((https://[^)]+)\)", links)
        linkedin_url = linkedin_match.group(1) if linkedin_match else ""

        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        experts.append(
            {
                "name": name,
                "slug": slug,
                "focus": focus,
                "linkedin_url": linkedin_url,
                "why_chosen": why_chosen,
            }
        )
    return experts


def build_template(expert: dict, template_number: int) -> str:
    return f"""# LinkedIn Post Template {template_number} — {expert["name"]}

- **Expert:** {expert["name"]}
- **Focus area:** {expert["focus"]}
- **LinkedIn profile:** {expert["linkedin_url"]}
- **Template created:** {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}

## Instructions
1. Open the expert's LinkedIn profile and sort by recent posts.
2. Find a post focused on outbound tactics, cold email, or SDR workflows.
3. Paste the full post content below (keep formatting where possible).
4. Add your notes on why this post is high-signal for the playbook.

## Post Metadata
- **Post URL:**
- **Post date:**
- **Engagement (likes/comments):**
- **Topic tag:** (e.g., sequencing, deliverability, objection handling)

## Post Content
<!-- Paste the LinkedIn post text here -->

## Analyst Notes
<!-- Why this post matters for the B2B SaaS cold outreach playbook -->

## Key Takeaways
- 
- 
- 

## Source Context
*Why this expert was selected:* {expert["why_chosen"]}
"""


def main() -> None:
    if not SOURCES_FILE.exists():
        raise FileNotFoundError(f"Missing sources file: {SOURCES_FILE}")

    sources_text = SOURCES_FILE.read_text(encoding="utf-8")
    experts = parse_experts(sources_text)
    if not experts:
        raise RuntimeError("No experts parsed from research/sources.md")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for expert in experts:
        for number in range(1, TEMPLATES_PER_EXPERT + 1):
            filename = f"{expert['slug']}__post-template-{number}.md"
            output_path = OUTPUT_DIR / filename
            output_path.write_text(build_template(expert, number), encoding="utf-8")
            created.append(output_path)

    print(f"Created {len(created)} LinkedIn template file(s) in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
