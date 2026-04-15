from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
BRAND_DIR = ROOT / "assets" / "brand"

BG = "#f5f0e7"
PAPER = "#fbf8f2"
INK = "#121826"
INK_SOFT = "#495261"
ACCENT = "#8ad161"
ACCENT_DEEP = "#1f3b31"
RULE = "#d8d0c2"

AVENIR = "/System/Library/Fonts/Avenir Next.ttc"
AVENIR_CONDENSED = "/System/Library/Fonts/Avenir Next Condensed.ttc"
GEORGIA = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
MENLO = "/System/Library/Fonts/Menlo.ttc"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def draw_grid(draw: ImageDraw.ImageDraw, width: int, height: int, step: int) -> None:
    for x in range(0, width + 1, step):
      draw.line((x, 0, x, height), fill="#ebe4d7", width=1)
    for y in range(0, height + 1, step):
      draw.line((0, y, width, y), fill="#ebe4d7", width=1)


def rounded_panel(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], radius: int) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=PAPER, outline=RULE, width=2)


def draw_mark(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], width: int = 10) -> None:
    left, top, right, bottom = box
    draw.rounded_rectangle(box, radius=int((right - left) * 0.18), fill=INK)
    inner = 8
    draw.rounded_rectangle(
        (left + inner, top + inner, right - inner, bottom - inner),
        radius=int((right - left) * 0.14),
        outline=(138, 209, 97, 60),
        width=2,
    )
    draw.line(
        (left + 30, top + 36, left + 56, top + 58, left + 30, top + 80),
        fill=PAPER,
        width=width,
        joint="curve",
    )
    draw.line((left + 68, top + 80, left + 92, top + 80), fill=ACCENT, width=width)


def make_brand_canvas() -> None:
    image = Image.new("RGB", (1600, 1200), BG)
    draw = ImageDraw.Draw(image)
    draw_grid(draw, 1600, 1200, 48)

    rounded_panel(draw, (72, 72, 1528, 1128), 42)
    draw.ellipse((1070, 96, 1510, 536), fill="#e3f3d4")
    draw.ellipse((1130, 156, 1450, 476), outline=ACCENT_DEEP, width=3)

    draw_mark(draw, (144, 154, 288, 298), width=12)
    draw.text((340, 166), "LEARN", fill=INK_SOFT, font=font(AVENIR_CONDENSED, 34))
    draw.text((340, 210), "Claude Code", fill=INK, font=font(GEORGIA, 86))
    draw.text(
        (146, 374),
        "A practical site for developers who want a repeatable terminal workflow.",
        fill=INK_SOFT,
        font=font(AVENIR, 34),
    )

    manifesto = [
        "Inspect first",
        "Prompt with constraints",
        "Edit narrowly",
        "Verify visibly",
    ]
    x = 146
    for item in manifesto:
        draw.rounded_rectangle((x, 484, x + 295, 564), radius=24, outline=RULE, fill="#f8f3eb", width=2)
        draw.text((x + 24, 510), item, fill=INK, font=font(AVENIR, 24))
        x += 318

    draw.rounded_rectangle((146, 636, 736, 1032), radius=34, fill=INK, outline="#1c2538", width=2)
    for idx, line in enumerate(
        [
            '$ codex ask "Inspect this repo first."',
            "1. discover entry points",
            "2. clarify the scope",
            "3. implement the narrow change",
            "4. run the checks",
        ]
    ):
        color = PAPER if idx == 0 else "#bec7d4"
        draw.text((182, 696 + idx * 58), line, fill=color, font=font(MENLO, 26))

    draw.rounded_rectangle((790, 636, 1454, 1032), radius=34, fill="#f7f1e7", outline=RULE, width=2)
    draw.text((836, 702), "Signal Ledger", fill=INK, font=font(GEORGIA, 56))
    draw.text(
        (836, 790),
        "Warm paper tones, terminal geometry,\nand one measured signal green.\nEditorial calm over startup noise.",
        fill=INK_SOFT,
        font=font(AVENIR, 28),
        spacing=12,
    )
    draw.line((836, 948, 1400, 948), fill=INK, width=3)
    draw.text((836, 972), "learn-claude-code.lol", fill=INK, font=font(MENLO, 24))

    image.save(BRAND_DIR / "brand-canvas.png")


def make_og_card() -> None:
    image = Image.new("RGB", (1200, 630), BG)
    draw = ImageDraw.Draw(image)
    draw_grid(draw, 1200, 630, 42)
    rounded_panel(draw, (36, 36, 1164, 594), 34)
    draw_mark(draw, (84, 92, 216, 224), width=10)
    draw.text((254, 100), "LEARN", fill=INK_SOFT, font=font(AVENIR_CONDENSED, 26))
    draw.text((254, 136), "Claude Code", fill=INK, font=font(GEORGIA, 64))
    draw.text(
        (88, 304),
        "A practical developer guide for setup,\nworkflow habits, safe edits, and real project loops.",
        fill=INK_SOFT,
        font=font(AVENIR, 28),
        spacing=10,
    )
    draw.rounded_rectangle((88, 448, 436, 526), radius=22, fill=INK)
    draw.text((124, 471), "learn-claude-code.lol", fill=PAPER, font=font(MENLO, 24))
    image.save(BRAND_DIR / "og-card.png")


def make_app_icons() -> None:
    for size, path in [
        (512, BRAND_DIR / "favicon-512.png"),
        (192, BRAND_DIR / "favicon-192.png"),
        (180, ROOT / "apple-touch-icon.png"),
        (32, BRAND_DIR / "favicon-32.png"),
    ]:
        image = Image.new("RGBA", (size, size), BG)
        draw = ImageDraw.Draw(image)
        inset = max(8, size // 16)
        draw.rounded_rectangle(
            (inset, inset, size - inset, size - inset),
            radius=size // 4,
            fill=INK,
        )
        draw.rounded_rectangle(
            (inset + 8, inset + 8, size - inset - 8, size - inset - 8),
            radius=size // 5,
            outline=(138, 209, 97, 60),
            width=max(2, size // 64),
        )
        scale = size / 128
        draw.line(
            (
                inset + 30 * scale,
                inset + 36 * scale,
                inset + 54 * scale,
                inset + 56 * scale,
                inset + 30 * scale,
                inset + 78 * scale,
            ),
            fill=PAPER,
            width=max(4, int(8 * scale)),
            joint="curve",
        )
        draw.line(
            (inset + 64 * scale, inset + 78 * scale, inset + 88 * scale, inset + 78 * scale),
            fill=ACCENT,
            width=max(4, int(8 * scale)),
        )
        image.save(path)

    favicon_source = Image.open(BRAND_DIR / "favicon-512.png")
    favicon_source.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])


def main() -> None:
    BRAND_DIR.mkdir(parents=True, exist_ok=True)
    make_brand_canvas()
    make_og_card()
    make_app_icons()


if __name__ == "__main__":
    main()
