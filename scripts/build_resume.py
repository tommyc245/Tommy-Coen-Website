"""Build the portfolio's one-page resume: python scripts/build_resume.py.

Requires reportlab. Content lives here so future updates remain editable.
"""

from hashlib import sha256
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "resume.pdf"
WIDTH = 540
FONT_BODY, FONT_BOLD = "Times-Roman", "Times-Bold"
font_files = ["times.ttf", "timesbd.ttf", "timesi.ttf", "timesbi.ttf"]
font_dir = Path("C:/Windows/Fonts")
if all((font_dir / name).is_file() for name in font_files):
    for name, filename in zip(
        ["ResumeTimes", "ResumeTimes-Bold", "ResumeTimes-Italic", "ResumeTimes-BoldItalic"],
        font_files,
    ):
        pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
    pdfmetrics.registerFontFamily(
        "ResumeTimes", normal="ResumeTimes", bold="ResumeTimes-Bold",
        italic="ResumeTimes-Italic", boldItalic="ResumeTimes-BoldItalic",
    )
    FONT_BODY, FONT_BOLD = "ResumeTimes", "ResumeTimes-Bold"
STYLES = {
    "name": ParagraphStyle(
        "name", fontName=FONT_BOLD, fontSize=22, leading=25, alignment=TA_CENTER
    ),
    "contact": ParagraphStyle(
        "contact", fontName=FONT_BODY, fontSize=10, leading=13, alignment=TA_CENTER
    ),
    "section": ParagraphStyle(
        "section", fontName=FONT_BOLD, fontSize=11, leading=13
    ),
    "body": ParagraphStyle(
        "body", fontName=FONT_BODY, fontSize=10.5, leading=12.7
    ),
    "bullet": ParagraphStyle(
        "bullet", fontName=FONT_BODY, fontSize=10.5, leading=12.7,
        bulletFontName=FONT_BODY, bulletFontSize=9,
        leftIndent=12, firstLineIndent=0, bulletIndent=2, spaceAfter=3,
    ),
}
story = []


def para(text, style="body"):
    return Paragraph(text, STYLES[style])


def row(left, right):
    right_style = ParagraphStyle("right", parent=STYLES["body"], alignment=2)
    table = Table(
        [[para(left), Paragraph(right, right_style)]], colWidths=[WIDTH - 112, 112]
    )
    table.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return table


def section(title):
    story.extend([
        Spacer(1, 8),
        KeepTogether([
            para(title, "section"),
            Spacer(1, 2),
            HRFlowable(width="100%", thickness=0.55, color=colors.black),
            Spacer(1, 4),
        ]),
    ])


def bullet(text):
    story.append(Paragraph(text, STYLES["bullet"], bulletText="\u2022"))


story.extend([
    para("Thomas Coen", "name"),
    Spacer(1, 3),
    para(
        '<link href="mailto:thomas.coen@duke.edu">thomas.coen@duke.edu</link>'
        ' | 831-717-8006 | '
        '<link href="https://tommyc245.github.io/Tommy-Coen-Website/">'
        'tommyc245.github.io/Tommy-Coen-Website</link>',
        "contact",
    ),
])

section("EDUCATION")
story.append(row("<b>Duke University, Pratt School of Engineering</b>", "Durham, NC"))
story.append(para(
    "B.S.E. Mechanical Engineering, Class of 2029 &middot; "
    "Aerospace Engineering Certificate &middot; GPA: 3.78"
))
story.append(para(
    "Relevant coursework: Thermodynamics, Mechanics of Solids, "
    "Differential Equations, Engineering Design"
))

section("ENGINEERING EXPERIENCE")
story.append(row("<b>Duke AERO (Rocketry Team)</b>", "Durham, NC"))
story.append(row("<i>Structures Lead</i>", "<i>July 2026 - Present</i>"))
bullet(
    "Lead ~12 active structures members developing a 30,000 ft student-researched "
    "and developed (SRAD) rocket for IREC 2027; rebuilt the team from 3 returning members"
)
bullet(
    "Led fabrication of composite test articles ahead of flight hardware production, "
    "including a body tube, nose cone, fin can, and coupler"
)
bullet(
    "Commissioned the team's first filament winder; designed a 3:1 gear drive in "
    "Onshape to replace a slipping belt drive and upgraded the motor to an "
    "8.2 N&middot;m NEMA 34 to resolve stalling, among numerous other modifications"
)
bullet(
    "Upgraded the control board and migrated from Marlin to Klipper; improved "
    "tow-placement consistency with fewer gaps and produced dry- and wet-wound test tubes"
)
story.append(Spacer(1, 2))
story.append(row("<i>Structures &amp; Solid Propulsion Member</i>", "<i>2025 - 2026</i>"))
bullet(
    "Machined a 6061 aluminum nozzle casing and programmed lightening features "
    "and a fourth-axis bolt-hole pattern; hardware survived full-duration static "
    "hot fire and flight. Team placed 3rd in the 30,000 ft SRAD propulsion category "
    "at IREC 2026"
)

story.append(Spacer(1, 5))
story.append(row("<b>BreakerBots, FIRST Robotics Team 5104</b>", "Pacific Grove, CA"))
story.append(row(
    "<i>Machinist / Manufacturing Lead / Co-Captain &amp; CAD Lead</i>",
    "<i>2022 - 2025</i>",
))
bullet(
    "Programmed CAM in Fusion 360 and machined 150+ robot parts across four seasons "
    "using Tormach CNC mills and Gerber and Tormach routers; grew the machining team "
    "from 2 to 15+ machinists through "
    "hands-on training in CAM and machine operation"
)
bullet(
    "Redesigned Leviathan's three-stage cascade elevator reaching 9.5 ft using two "
    "Kraken X60 motors and a 5:1 reduction; added constant-force spring assistance, "
    "reducing measured extension time from 3.5 s to 1.8 s (2025)"
)
bullet(
    "Helped reduce robot weight from 134 lb to 114 lb, below the 115 lb limit, by "
    "redesigning and machining pocketed aluminum elevator components and replacing "
    "aluminum brackets with 3D-printed polymer and composite parts (2025)"
)
bullet("Designed and machined Typhoon's intake and pivot (2024)")
bullet("Coordinated 5 subteams and 35 members through robot design and construction (2025)")

story.append(Spacer(1, 5))
story.append(row("<b>Duke EGR 121, Sunflower Seed Sheller</b>", "Durham, NC"))
story.append(row("<i>Mechanical Design</i>", "<i>2026</i>"))
bullet("Designed the rollers, drive mechanism, and feed funnel for a four-person team's sunflower seed sheller")
bullet(
    "Iterated roller-groove geometry through 3D-printed prototypes and testing to "
    "crack shells along the seam while limiting kernel damage"
)
bullet(
    "Team produced 41 intact kernels in 3 minutes, earning the highest "
    "yield-minus-waste score among 8 section teams and 2nd among all first-year "
    "mechanical engineering teams"
)

section("SKILLS")
story.append(para("<b>Design:</b> SolidWorks, Onshape, Fusion 360 (CAD/CAM), AutoCAD"))
story.append(para(
    "<b>Manufacturing:</b> CNC milling (Tormach 1100MX, 770M, Viwa; fourth axis), "
    "CNC routing (Gerber, Tormach), CNC turning, manual lathe, 3D printing, carbon fiber and fiberglass layup, "
    "filament winding, laser cutting; Titans of CNC certification series"
))

SimpleDocTemplate(
    str(OUTPUT), pagesize=(612, 792), rightMargin=30, leftMargin=30,
    topMargin=29, bottomMargin=29, title="Thomas Coen - Resume",
    author="Thomas Coen", subject="Mechanical Engineering Resume",
).build(story)

# Refresh both the embedded PDF and download when the resume changes.
page = ROOT / "resume.html"
version = sha256(OUTPUT.read_bytes()).hexdigest()[:12]
html = page.read_text(encoding="utf-8")
html = re.sub(
    r'((?:href|src)="resume\.pdf)(?:\?v=[^"]*)?(")',
    rf'\1?v={version}\2',
    html,
)
page.write_text(html, encoding="utf-8")
print(f"Built {OUTPUT}")
