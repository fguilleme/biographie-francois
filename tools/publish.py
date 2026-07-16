#!/usr/bin/env python3
"""Construit une édition PDF et un corpus ZIP depuis le dépôt biographique.

Le dépôt reste la source de vérité. Les fichiers de build sont régénérables.
"""

from __future__ import annotations

import datetime as dt
import os
import re
import shutil
import subprocess
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
BOOK_DIR = BUILD / "book"
NOTEBOOK_DIR = BUILD / "notebook"
REPORT_DIR = BUILD / "reports"
TODAY = dt.date.today().isoformat()

EXCLUDED_PARTS = {
    ".git",
    ".github",
    "build",
    "bundles",
    "raw conversations",
    "inbox",
    "journal",
    "meta",
    "connaissances",
    "archives",
    "tools",
}

SECTION_ORDER = [
    ("Ouverture", ["README.md", "chronologie.md"]),
    ("Famille", ["famille"]),
    ("Scolarité", ["scolarite"]),
    ("Formation", ["formation"]),
    ("Service militaire", ["militaire"]),
    ("Vie professionnelle", ["professionnel"]),
    ("Santé", ["sante"]),
    ("Informatique", ["informatique"]),
    ("Voyages", ["voyages"]),
    ("Souvenirs", ["souvenirs"]),
]


def git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def tracked_files() -> list[Path]:
    return [ROOT / p for p in git(["ls-files"]).splitlines() if p]


def primary_markdown_files() -> list[Path]:
    tracked = tracked_files()
    selected: list[Path] = []
    seen: set[Path] = set()
    for _, entries in SECTION_ORDER:
        for entry in entries:
            p = ROOT / entry
            candidates = [p] if p.is_file() else sorted(p.glob("*.md")) if p.is_dir() else []
            for candidate in candidates:
                if candidate.suffix.lower() == ".md" and candidate not in seen:
                    selected.append(candidate)
                    seen.add(candidate)
    return selected


def register_fonts() -> tuple[str, str]:
    serif = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
    serif_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    if Path(serif).exists() and Path(serif_bold).exists():
        pdfmetrics.registerFont(TTFont("BookSerif", serif))
        pdfmetrics.registerFont(TTFont("BookSerifBold", serif_bold))
        return "BookSerif", "BookSerifBold"
    return "Times-Roman", "Times-Bold"


def clean_inline(text: str) -> str:
    text = re.sub(r"!\[[^]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    return escape(text, entities={"<b>": "<b>", "</b>": "</b>", "<i>": "<i>", "</i>": "</i>"})


def markdown_story(path: Path, styles: dict[str, ParagraphStyle]) -> list:
    lines = path.read_text(encoding="utf-8").splitlines()
    story: list = []
    paragraph: list[str] = []

    def flush() -> None:
        if paragraph:
            text = " ".join(x.strip() for x in paragraph).strip()
            if text:
                story.append(Paragraph(clean_inline(text), styles["body"]))
                story.append(Spacer(1, 0.16 * cm))
            paragraph.clear()

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            flush()
            continue
        if line.startswith("# "):
            flush()
            story.append(Paragraph(clean_inline(line[2:].strip()), styles["chapter"]))
            story.append(Spacer(1, 0.25 * cm))
        elif line.startswith("## "):
            flush()
            story.append(Paragraph(clean_inline(line[3:].strip()), styles["h2"]))
        elif line.startswith("### "):
            flush()
            story.append(Paragraph(clean_inline(line[4:].strip()), styles["h3"]))
        elif line.startswith("> "):
            flush()
            story.append(Paragraph(clean_inline(line[2:].strip()), styles["quote"]))
            story.append(Spacer(1, 0.12 * cm))
        elif re.match(r"^\s*[-*]\s+", line):
            flush()
            item = re.sub(r"^\s*[-*]\s+", "", line)
            story.append(Paragraph("• " + clean_inline(item), styles["bullet"]))
        elif re.match(r"^\s*\d+\.\s+", line):
            flush()
            story.append(Paragraph(clean_inline(line.strip()), styles["bullet"]))
        elif line.startswith("---"):
            flush()
            story.append(Spacer(1, 0.25 * cm))
        else:
            paragraph.append(line)
    flush()
    return story


class BookDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates(PageTemplate(id="book", frames=[frame], onPage=self._footer))

    def _footer(self, canvas, doc) -> None:
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredString(A4[0] / 2, 0.65 * cm, f"Biographie de François Guillemé - édition {TODAY} - {doc.page}")
        canvas.restoreState()


def build_pdf() -> Path:
    BOOK_DIR.mkdir(parents=True, exist_ok=True)
    normal_font, bold_font = register_fonts()
    sample = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle("Title", parent=sample["Title"], fontName=bold_font, fontSize=28, leading=34, alignment=TA_CENTER, spaceAfter=18),
        "subtitle": ParagraphStyle("Subtitle", parent=sample["Normal"], fontName=normal_font, fontSize=13, leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#555555")),
        "section": ParagraphStyle("Section", parent=sample["Heading1"], fontName=bold_font, fontSize=20, leading=24, spaceBefore=8, spaceAfter=14, pageBreakBefore=True),
        "chapter": ParagraphStyle("Chapter", parent=sample["Heading1"], fontName=bold_font, fontSize=17, leading=22, spaceBefore=8, spaceAfter=8, keepWithNext=True),
        "h2": ParagraphStyle("H2", parent=sample["Heading2"], fontName=bold_font, fontSize=13.5, leading=18, spaceBefore=10, spaceAfter=5, keepWithNext=True),
        "h3": ParagraphStyle("H3", parent=sample["Heading3"], fontName=bold_font, fontSize=11.5, leading=15, spaceBefore=8, spaceAfter=4, keepWithNext=True),
        "body": ParagraphStyle("Body", parent=sample["BodyText"], fontName=normal_font, fontSize=10.5, leading=15.5, alignment=TA_LEFT, spaceAfter=2),
        "bullet": ParagraphStyle("Bullet", parent=sample["BodyText"], fontName=normal_font, fontSize=10.2, leading=14.5, leftIndent=0.55 * cm, firstLineIndent=-0.35 * cm, spaceAfter=3),
        "quote": ParagraphStyle("Quote", parent=sample["BodyText"], fontName=normal_font, fontSize=10.2, leading=15, leftIndent=0.8 * cm, rightIndent=0.8 * cm, textColor=colors.HexColor("#444444"), borderColor=colors.HexColor("#BBBBBB"), borderWidth=0, borderPadding=5),
        "toc": ParagraphStyle("TOC", parent=sample["BodyText"], fontName=normal_font, fontSize=10.5, leading=15, leftIndent=0.5 * cm),
    }

    versioned = BOOK_DIR / f"Biographie-Francois-v{TODAY}.pdf"
    doc = BookDocTemplate(
        str(versioned),
        pagesize=A4,
        rightMargin=2.1 * cm,
        leftMargin=2.1 * cm,
        topMargin=2.0 * cm,
        bottomMargin=1.5 * cm,
        title="Biographie de François Guillemé",
        author="François Guillemé",
        subject="Édition générée depuis le dépôt Git",
    )

    story: list = [
        Spacer(1, 5.0 * cm),
        Paragraph("Biographie de François Guillemé", styles["title"]),
        Paragraph("Une mémoire en construction", styles["subtitle"]),
        Spacer(1, 1.2 * cm),
        Paragraph(f"Édition du {TODAY}", styles["subtitle"]),
        Spacer(1, 2.0 * cm),
        Paragraph("Cette édition est générée automatiquement depuis le dépôt Git, qui reste la source de vérité. Les souvenirs, faits vérifiés et incertitudes sont conservés comme tels.", styles["quote"]),
        PageBreak(),
        Paragraph("Sommaire", styles["chapter"]),
    ]

    for section, entries in SECTION_ORDER:
        files: list[Path] = []
        for entry in entries:
            p = ROOT / entry
            files.extend([p] if p.is_file() else sorted(p.glob("*.md")) if p.is_dir() else [])
        if files:
            story.append(Paragraph(clean_inline(section), styles["toc"]))
            for file in files:
                title = next((ln[2:].strip() for ln in file.read_text(encoding="utf-8").splitlines() if ln.startswith("# ")), file.stem)
                story.append(Paragraph("- " + clean_inline(title), styles["toc"]))
    story.append(PageBreak())

    for section, entries in SECTION_ORDER:
        files: list[Path] = []
        for entry in entries:
            p = ROOT / entry
            files.extend([p] if p.is_file() else sorted(p.glob("*.md")) if p.is_dir() else [])
        if not files:
            continue
        story.append(Paragraph(clean_inline(section), styles["section"]))
        for index, file in enumerate(files):
            if index:
                story.append(Spacer(1, 0.55 * cm))
            story.extend(markdown_story(file, styles))

    doc.build(story)
    shutil.copy2(versioned, BOOK_DIR / "Biographie-Francois-latest.pdf")
    return versioned


def build_notebook_zip() -> Path:
    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    out = NOTEBOOK_DIR / f"notebook-biographie-francois-{TODAY}.zip"
    include_suffixes = {".md", ".txt", ".pdf", ".jpg", ".jpeg", ".png", ".json"}
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in tracked_files():
            rel = path.relative_to(ROOT)
            if "build" in rel.parts or path.suffix.lower() not in include_suffixes:
                continue
            archive.write(path, rel.as_posix())
        latest_pdf = BOOK_DIR / "Biographie-Francois-latest.pdf"
        archive.write(latest_pdf, "publication/Biographie-Francois-latest.pdf")
    latest = NOTEBOOK_DIR / "notebook-biographie-francois-latest.zip"
    shutil.copy2(out, latest)
    return out


def write_report(pdf: Path, notebook: Path) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    md_files = primary_markdown_files()
    report = REPORT_DIR / f"publication-{TODAY}.md"
    report.write_text(
        "\n".join(
            [
                f"# Publication du {TODAY}",
                "",
                f"- Commit source : `{git(['rev-parse', 'HEAD'])}`",
                f"- Fichiers narratifs intégrés au livre : {len(md_files)}",
                f"- PDF : `{pdf.relative_to(ROOT)}`",
                f"- Corpus Notebook/RAG : `{notebook.relative_to(ROOT)}`",
                "- Source de vérité : fichiers Markdown du dépôt.",
                "- Les répertoires `build/` sont régénérables.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return report


def main() -> None:
    pdf = build_pdf()
    notebook = build_notebook_zip()
    report = write_report(pdf, notebook)
    print(pdf.relative_to(ROOT))
    print(notebook.relative_to(ROOT))
    print(report.relative_to(ROOT))


if __name__ == "__main__":
    main()
