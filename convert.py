#!/usr/bin/env python3
"""
Markdown -> PDF converter.

Design lives entirely in templates/template.html and templates/style.css.
This script only orchestrates: it reads Markdown from inputs/, turns it
into HTML, drops that HTML into the template, and asks WeasyPrint to
render the result to PDF in output/.
"""

import argparse
import re
import sys
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

ROOT = Path(__file__).resolve().parent
INPUTS_DIR = ROOT / "inputs"
OUTPUT_DIR = ROOT / "output"
TEMPLATES_DIR = ROOT / "templates"

MARKDOWN_EXTENSIONS = ["extra", "sane_lists", "smarty"]


def markdown_to_html(md_text: str) -> str:
    return markdown.markdown(md_text, extensions=MARKDOWN_EXTENSIONS)


def guess_title(md_text: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", md_text, flags=re.MULTILINE)
    return match.group(1).strip() if match else fallback


def render_pdf(md_path: Path, output_dir: Path, template_name: str = "template.html") -> Path:
    md_text = md_path.read_text(encoding="utf-8")
    content_html = markdown_to_html(md_text)
    title = guess_title(md_text, md_path.stem)

    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template(template_name)
    full_html = template.render(content=content_html, title=title)

    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = output_dir / f"{md_path.stem}.pdf"

    # base_url lets the template's relative "style.css" link resolve.
    HTML(string=full_html, base_url=str(TEMPLATES_DIR)).write_pdf(str(pdf_path))
    return pdf_path


def collect_inputs(paths: list[str]) -> list[Path]:
    if not paths:
        found = sorted(INPUTS_DIR.glob("*.md"))
        if not found:
            print(f"No .md files found in {INPUTS_DIR}", file=sys.stderr)
        return found
    return [Path(p) for p in paths]


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Markdown files to styled PDF resumes.")
    parser.add_argument(
        "inputs",
        nargs="*",
        help="Specific Markdown file(s) to convert. Defaults to every *.md file in inputs/.",
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=str(OUTPUT_DIR),
        help="Directory to write PDFs to (default: output/).",
    )
    parser.add_argument(
        "--template",
        default="template.html",
        help="Template filename inside templates/ (default: template.html).",
    )
    args = parser.parse_args()

    md_files = collect_inputs(args.inputs)
    if not md_files:
        sys.exit(1)

    output_dir = Path(args.output_dir)
    for md_path in md_files:
        if not md_path.exists():
            print(f"Skipping {md_path}: not found", file=sys.stderr)
            continue
        pdf_path = render_pdf(md_path, output_dir, args.template)
        print(f"{md_path} -> {pdf_path}")


if __name__ == "__main__":
    main()
