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