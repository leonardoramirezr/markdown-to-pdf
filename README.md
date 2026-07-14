# Markdown to PDF

Converts Markdown files into styled PDFs (designed for CVs/resumes). The layout is entirely defined in `templates/template.html` and `templates/style.css`; the script simply orchestrates the process: it reads Markdown from `inputs/`, converts it to HTML, inserts it into the template, and uses WeasyPrint to generate the PDF in `output/`.

## Requirements

- Python >= 3.11
- [uv](https://docs.astral.sh/uv/) to manage the environment and dependencies

## Installation

```bash
uv sync
```

## Usage

Place your `.md` files in `inputs/` and run:

```bash
uv run convert.py
```

This converts all `.md` files in `inputs/` and writes the resulting PDFs to `output/`.

You can also specify individual files, a different output directory, or a different template:

```bash
uv run convert.py inputs/my-resume.md
uv run convert.py inputs/my-resume.md -o another-folder/
uv run convert.py --template another-template.html
```

The PDF title is taken from the first `# ` heading in the Markdown; if none exists, the filename is used.

## Project Structure

```
convert.py            # conversion script (CLI)
inputs/               # input Markdown files (ignored by git)
output/                # generated PDFs (ignored by git)
templates/
  template.html         # base HTML structure
  style.css             # PDF styles
  fonts/                # embedded fonts
```

## Markdown to Style Mapping

`templates/style.css` doesn't style headings generically — it targets specific selectors inside the `.resume` container. Here's how each Markdown element is rendered in the PDF:

| Markdown | CSS selector | Font | Weight | Size |
|---|---|---|---|---|
| `# Title` (only the first `#`, e.g. the name) | `.resume > h1:first-child` | "IBM Plex Mono" (monospace) | 700 (bold) | 26pt, centered |
| `## Section` | `h2` | Inherits "IBM Plex Sans" from `.resume` | 700 (bold) | 12.5pt, underlined |
| `### Subtitle` | `h3` | Inherits "IBM Plex Sans" | 700 (bold) | 11pt |
| `#### / ##### / ######` | *(no dedicated rule)* | Inherits "IBM Plex Sans" | Falls back to the browser/WeasyPrint default (usually bold) | — |
| `**bold**` / `__bold__` | `strong` | Inherits surrounding font | 700 (bold) | Inherits size |
| `*italic*` / `_italic_` | `em` (no general rule) | Inherits surrounding font | Normal weight with `font-style: italic` (default browser/WeasyPrint behavior) | Inherits size |
| `*italic*` on the line right under a `###` (e.g. company/dates) | `h3 + p em` | Inherits surrounding font | 400 (normal, not bold) + italic | 10.5pt (inherited from `h3 + p`) |

Notes:
- Only the **first** `h1` in the document (the name) uses the monospace font "IBM Plex Mono" at 26pt; any subsequent `h1` has no dedicated rule and would inherit the base `.resume` style (IBM Plex Sans, 10.5pt, normal weight).
- `**` and `__` are equivalent in Markdown — both produce `<strong>`, so both end up at weight 700.