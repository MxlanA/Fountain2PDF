import flet as ft
from pathlib import Path

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ============================================================
# SETTINGS
# ============================================================

PAGE_WIDTH, PAGE_HEIGHT = LETTER

FONT_NAME = "CourierPrime"

FONT_FILE = Path(__file__).parent / "courier-prime.regular.ttf"

FONT_SIZE = 12

TOP_MARGIN = 72
BOTTOM_MARGIN = 72

ACTION_LEFT = 72
ACTION_RIGHT = PAGE_WIDTH - 72

CHARACTER_LEFT = 216

DIALOGUE_LEFT = 144
DIALOGUE_RIGHT = 468

PARENTHETICAL_LEFT = 180
PARENTHETICAL_RIGHT = 432

TRANSITION_RIGHT = PAGE_WIDTH - 72


# ============================================================
# LOAD FONT
# ============================================================

pdfmetrics.registerFont(
    TTFont(
        FONT_NAME,
        str(FONT_FILE)
    )
)


# ============================================================
# PAGE MANAGEMENT
# ============================================================

def new_page(pdf, page_number):

    pdf.showPage()

    pdf.setFont(
        FONT_NAME,
        FONT_SIZE
    )

    # Page number
    pdf.drawRightString(
        PAGE_WIDTH - 72,
        PAGE_HEIGHT - 45,
        str(page_number)
    )


# ============================================================
# READ FOUNTAIN
# ============================================================

def read_fountain(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ============================================================
# TITLE PAGE
# ============================================================

def extract_title_page(text):

    fields = {
        "title": "",
        "credit": "",
        "author": "",
        "source": "",
        "draft date": "",
        "contact": ""
    }

    lines = text.splitlines()

    screenplay_start = 0

    for i, line in enumerate(lines):

        stripped = line.strip()

        if stripped == "":
            continue

        if ":" in stripped:

            key, value = stripped.split(
                ":",
                1
            )

            key = key.strip().lower()
            value = value.strip()

            if key in fields:

                fields[key] = value

                screenplay_start = i + 1

                continue

        break

    return fields, lines[screenplay_start:]


# ============================================================
# WORD WRAPPING
# ============================================================

def wrap_text(text, width):

    words = text.split()

    if not words:
        return [""]

    lines = []

    current = ""

    for word in words:

        if current == "":
            test = word

        else:
            test = current + " " + word

        if pdfmetrics.stringWidth(
            test,
            FONT_NAME,
            FONT_SIZE
        ) <= width:

            current = test

        else:

            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


# ============================================================
# TITLE PAGE
# ============================================================

def draw_title_page(pdf, fields):

    pdf.setFont(
        FONT_NAME,
        FONT_SIZE
    )

    # TITLE

    if fields["title"]:

        pdf.drawCentredString(
            PAGE_WIDTH / 2,
            PAGE_HEIGHT * 0.62,
            fields["title"].upper()
        )

    # CREDIT

    if fields["credit"]:

        pdf.drawCentredString(
            PAGE_WIDTH / 2,
            PAGE_HEIGHT * 0.55,
            fields["credit"]
        )

    # AUTHOR

    if fields["author"]:

        pdf.drawCentredString(
            PAGE_WIDTH / 2,
            PAGE_HEIGHT * 0.51,
            fields["author"]
        )

    # SOURCE

    if fields["source"]:

        pdf.drawCentredString(
            PAGE_WIDTH / 2,
            PAGE_HEIGHT * 0.47,
            fields["source"]
        )

    # DRAFT DATE

    if fields["draft date"]:

        pdf.drawCentredString(
            PAGE_WIDTH / 2,
            PAGE_HEIGHT * 0.43,
            fields["draft date"]
        )

    # CONTACT

    if fields["contact"]:

        y = PAGE_HEIGHT * 0.12

        for line in fields["contact"].splitlines():

            pdf.drawString(
                PAGE_WIDTH * 0.12,
                y,
                line
            )

            y -= 14


# ============================================================
# ELEMENT DETECTION
# ============================================================

def is_scene_heading(line):

    upper = line.upper()

    return (
        upper.startswith("INT.")
        or upper.startswith("EXT.")
        or upper.startswith("INT./EXT.")
        or upper.startswith("EXT./INT.")
    )


def is_transition(line):

    upper = line.upper()

    transitions = [
        "CUT TO:",
        "FADE IN:",
        "FADE OUT.",
        "FADE OUT:",
        "FADE TO:",
        "DISSOLVE TO:",
        "SMASH CUT TO:"
    ]

    return upper in transitions or upper.endswith(" TO:")


def is_character(line):

    if not line:
        return False

    if line.startswith("("):
        return False

    if line.startswith("."):
        return False

    # Fountain character names are normally uppercase.
    return line.upper() == line


# ============================================================
# DRAW ACTION
# ============================================================

def draw_action(pdf, text, y):

    width = ACTION_RIGHT - ACTION_LEFT

    wrapped = wrap_text(
        text,
        width
    )

    for line in wrapped:

        if y < BOTTOM_MARGIN:

            return None

        pdf.drawString(
            ACTION_LEFT,
            y,
            line
        )

        y -= 14

    return y - 10


# ============================================================
# DRAW SCENE HEADING
# ============================================================

def draw_scene_heading(pdf, text, y):

    wrapped = wrap_text(
        text.upper(),
        ACTION_RIGHT - ACTION_LEFT
    )

    y -= 8

    for line in wrapped:

        if y < BOTTOM_MARGIN:

            return None

        pdf.drawString(
            ACTION_LEFT,
            y,
            line
        )

        y -= 14

    return y - 14


# ============================================================
# DRAW CHARACTER
# ============================================================

def draw_character(pdf, text, y):

    if y < BOTTOM_MARGIN:

        return None

    pdf.drawString(
        CHARACTER_LEFT,
        y,
        text.upper()
    )

    return y - 18


# ============================================================
# DRAW PARENTHETICAL
# ============================================================

def draw_parenthetical(pdf, text, y):

    wrapped = wrap_text(
        text,
        PARENTHETICAL_RIGHT - PARENTHETICAL_LEFT
    )

    for line in wrapped:

        if y < BOTTOM_MARGIN:

            return None

        pdf.drawString(
            PARENTHETICAL_LEFT,
            y,
            line
        )

        y -= 14

    return y - 2


# ============================================================
# DRAW DIALOGUE
# ============================================================

def draw_dialogue(pdf, text, y):

    wrapped = wrap_text(
        text,
        DIALOGUE_RIGHT - DIALOGUE_LEFT
    )

    for line in wrapped:

        if y < BOTTOM_MARGIN:

            return None

        pdf.drawString(
            DIALOGUE_LEFT,
            y,
            line
        )

        y -= 14

    return y - 10


# ============================================================
# DRAW TRANSITION
# ============================================================

def draw_transition(pdf, text, y):

    if y < BOTTOM_MARGIN:

        return None

    pdf.drawRightString(
        TRANSITION_RIGHT,
        y,
        text.upper()
    )

    return y - 18


# ============================================================
# DRAW SCREENPLAY
# ============================================================

def draw_screenplay(pdf, lines):

    page_number = 1

    y = PAGE_HEIGHT - TOP_MARGIN

    pdf.setFont(
        FONT_NAME,
        FONT_SIZE
    )

    pdf.drawRightString(
        PAGE_WIDTH - 72,
        PAGE_HEIGHT - 45,
        str(page_number)
    )

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        # ----------------------------------------------------
        # BLANK LINE
        # ----------------------------------------------------

        if line == "":

            y -= 12

            i += 1

            continue

        # ----------------------------------------------------
        # FOUNTAIN PAGE BREAK
        # ----------------------------------------------------

        if line == "===":

            page_number += 1

            new_page(
                pdf,
                page_number
            )

            y = PAGE_HEIGHT - TOP_MARGIN

            i += 1

            continue

        # ----------------------------------------------------
        # SCENE HEADING
        # ----------------------------------------------------

        if is_scene_heading(line):

            result = draw_scene_heading(
                pdf,
                line,
                y
            )

            if result is None:

                page_number += 1

                new_page(
                    pdf,
                    page_number
                )

                y = PAGE_HEIGHT - TOP_MARGIN

                continue

            y = result

            i += 1

            continue

        # ----------------------------------------------------
        # TRANSITION
        # ----------------------------------------------------

        if is_transition(line):

            result = draw_transition(
                pdf,
                line,
                y
            )

            if result is None:

                page_number += 1

                new_page(
                    pdf,
                    page_number
                )

                y = PAGE_HEIGHT - TOP_MARGIN

                continue

            y = result

            i += 1

            continue

        # ----------------------------------------------------
        # CHARACTER + DIALOGUE
        # ----------------------------------------------------

        if is_character(line):

            character = line

            # ------------------------------------------------
            # BASIC DUAL DIALOGUE DETECTION
            # ------------------------------------------------

            if character.endswith("^"):

                character = character[:-1].rstrip()

                dual = True

            else:

                dual = False

            result = draw_character(
                pdf,
                character,
                y
            )

            if result is None:

                page_number += 1

                new_page(
                    pdf,
                    page_number
                )

                y = PAGE_HEIGHT - TOP_MARGIN

                continue

            y = result

            i += 1

            # ------------------------------------------------
            # DIALOGUE LINES
            # ------------------------------------------------

            while i < len(lines):

                dialogue_line = lines[i].strip()

                if dialogue_line == "":

                    i += 1

                    break

                # PARENTHETICAL

                if (
                    dialogue_line.startswith("(")
                    and
                    dialogue_line.endswith(")")
                ):

                    result = draw_parenthetical(
                        pdf,
                        dialogue_line,
                        y
                    )

                    if result is None:

                        page_number += 1

                        new_page(
                            pdf,
                            page_number
                        )

                        y = PAGE_HEIGHT - TOP_MARGIN

                        continue

                    y = result

                    i += 1

                    continue

                # STOP DIALOGUE IF NEW ELEMENT APPEARS

                if is_scene_heading(
                    dialogue_line
                ):

                    break

                if is_transition(
                    dialogue_line
                ):

                    break

                if is_character(
                    dialogue_line
                ):

                    break

                result = draw_dialogue(
                    pdf,
                    dialogue_line,
                    y
                )

                if result is None:

                    page_number += 1

                    new_page(
                        pdf,
                        page_number
                    )

                    y = PAGE_HEIGHT - TOP_MARGIN

                    continue

                y = result

                i += 1

            continue

        # ----------------------------------------------------
        # ACTION
        # ----------------------------------------------------

        result = draw_action(
            pdf,
            line,
            y
        )

        if result is None:

            page_number += 1

            new_page(
                pdf,
                page_number
            )

            y = PAGE_HEIGHT - TOP_MARGIN

            continue

        y = result

        i += 1


# ============================================================
# CREATE PDF
# ============================================================

def create_pdf(file_path):

    fountain_text = read_fountain(
        file_path
    )

    fields, screenplay_lines = extract_title_page(
        fountain_text
    )

    output_file = Path(
        file_path
    ).with_suffix(".pdf")

    pdf = canvas.Canvas(
        str(output_file),
        pagesize=LETTER
    )

    # TITLE PAGE

    draw_title_page(
        pdf,
        fields
    )

    # SCREENPLAY STARTS ON PAGE 1

    pdf.showPage()

    draw_screenplay(
        pdf,
        screenplay_lines
    )

    pdf.save()

    return output_file


# ============================================================
# FLET APPLICATION
# ============================================================

def main(page: ft.Page):

    page.title = "Fountain to PDF"

    status = ft.Text(
        "Choose a Fountain file."
    )

    file_picker = ft.FilePicker()

    async def choose_file(e):

        files = await file_picker.pick_files(
            allowed_extensions=["fountain"],
            allow_multiple=False
        )

        if not files:
            return

        file_path = files[0].path

        try:

            output_file = create_pdf(
                file_path
            )

            status.value = (
                "PDF created successfully!\n\n"
                f"{output_file}"
            )

        except Exception as error:

            status.value = (
                "Something went wrong:\n\n"
                f"{error}"
            )

        page.update()

    page.add(
        ft.Column(
            [
                ft.Text(
                    "Fountain → PDF",
                    size=26
                ),

                ft.Text(
                    "Import a Fountain screenplay "
                    "and create a PDF."
                ),

                ft.Button(
                    "Import Fountain File",
                    on_click=choose_file
                ),

                status
            ]
        )
    )


ft.run(main)
