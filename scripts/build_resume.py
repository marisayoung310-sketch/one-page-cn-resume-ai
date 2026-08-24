#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Table, TableStyle

NAVY = colors.HexColor("#17365D")
TEXT = colors.HexColor("#20252B")
MUTED = colors.HexColor("#56616F")
RULE = colors.HexColor("#A9B8C8")


def font_defaults():
    regular = Path("/System/Library/Fonts/STHeiti Light.ttc")
    bold = Path("/System/Library/Fonts/STHeiti Medium.ttc")
    return regular, bold


def register_fonts(regular, bold):
    pdfmetrics.registerFont(TTFont("CN", str(regular), subfontIndex=0))
    pdfmetrics.registerFont(TTFont("CN-Bold", str(bold), subfontIndex=0))
    pdfmetrics.registerFontFamily("CN", normal="CN", bold="CN-Bold", italic="CN", boldItalic="CN-Bold")


def make_styles():
    return {
        "name": ParagraphStyle("name", fontName="CN-Bold", fontSize=23, leading=25, textColor=NAVY, alignment=TA_CENTER, spaceAfter=3),
        "contact": ParagraphStyle("contact", fontName="CN", fontSize=10, leading=12, textColor=MUTED, alignment=TA_CENTER, spaceAfter=8),
        "section": ParagraphStyle("section", fontName="CN-Bold", fontSize=11.5, leading=13.5, textColor=NAVY),
        "company": ParagraphStyle("company", fontName="CN-Bold", fontSize=9.5, leading=12, textColor=TEXT),
        "position": ParagraphStyle("position", fontName="CN-Bold", fontSize=9.5, leading=12, textColor=NAVY, alignment=TA_CENTER),
        "date": ParagraphStyle("date", fontName="CN", fontSize=8.8, leading=12, textColor=MUTED, alignment=TA_RIGHT),
        "body": ParagraphStyle("body", fontName="CN", fontSize=9.1, leading=15.2, textColor=TEXT, alignment=TA_LEFT),
        "bullet": ParagraphStyle("bullet", fontName="CN", fontSize=9.1, leading=15.2, textColor=TEXT, leftIndent=10, firstLineIndent=-9, bulletIndent=0, spaceAfter=2.8),
    }


def section(title, styles):
    table = Table([[Paragraph(title, styles["section"])]], colWidths=[178 * mm])
    table.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.65, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return table


def role(company, position, date, styles):
    table = Table([[
        Paragraph(company, styles["company"]),
        Paragraph(position, styles["position"]),
        Paragraph(date, styles["date"]),
    ]], colWidths=[72 * mm, 34 * mm, 72 * mm])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    return table


def bullet(item, styles):
    return Paragraph(f'• <b>{item["label"]}：</b>{item["text"]}', styles["bullet"])


def build(data, output, regular_font, bold_font):
    register_fonts(regular_font, bold_font)
    styles = make_styles()
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(output), pagesize=A4,
        leftMargin=16 * mm, rightMargin=16 * mm, topMargin=10 * mm, bottomMargin=9 * mm,
        title=f'{data["name"]} - 简历', author=data["name"],
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="resume", frames=[frame])])

    education = data["education"]
    story = [
        Paragraph(data["name"], styles["name"]),
        Paragraph(data["contact"], styles["contact"]),
        section("教育经历", styles),
        role(education["school"], education["degree"], education["date"], styles),
        Paragraph(f'<b>主修课程：</b>{education["courses"]}', styles["body"]),
        section("实习经历", styles),
    ]
    for experience in data["experiences"]:
        story.append(role(experience["company"], experience["position"], experience["date"], styles))
        story.extend(bullet(item, styles) for item in experience["bullets"])
    story.append(section("专业技能", styles))
    story.extend(bullet(item, styles) for item in data["skills"])
    doc.build(story)


def main():
    parser = argparse.ArgumentParser(description="Build a one-page Chinese resume PDF from JSON.")
    parser.add_argument("data", type=Path)
    parser.add_argument("--output", type=Path, default=Path("output/resume.pdf"))
    regular, bold = font_defaults()
    parser.add_argument("--font", type=Path, default=regular)
    parser.add_argument("--bold-font", type=Path, default=bold)
    args = parser.parse_args()
    for path in (args.data, args.font, args.bold_font):
        if not path.exists():
            parser.error(f"File not found: {path}")
    data = json.loads(args.data.read_text(encoding="utf-8"))
    build(data, args.output, args.font, args.bold_font)
    print(args.output.resolve())


if __name__ == "__main__":
    main()

