"""Build original SVG artwork and rasterize it with local, headless Chromium.

This is a build-time tool. The submitted entry uses only main.py and entry.png.
No photographs, external fonts, downloaded drawings, or remote assets are used.
"""

import argparse
from html import escape
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import zlib


NAVY = "#132f3c"
PAPER = "#f8f3e9"
TEAL = "#176d72"
RED = "#bf4836"
GOLD = "#e7b65f"
GRAY = "#49616a"


def lettering(x, y, words, size, bold=500, color=NAVY, **attributes):
    extras = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attributes.items())
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{bold}" '
            f'fill="{color}" {extras}>{escape(words)}</text>')


def box(x, y, width, height, color, radius=0):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{color}"/>'


def drawing(points, color="none", line=NAVY, thickness=3, **attributes):
    extras = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attributes.items())
    return (f'<path d="{points}" fill="{color}" stroke="{line}" stroke-width="{thickness}" '
            f'stroke-linejoin="round" stroke-linecap="round" {extras}/>')


def dot(x, y, radius, color):
    return f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{color}"/>'


def place(x, y, content, scale=1):
    return f'<g transform="translate({x} {y}) scale({scale})">{content}</g>'


def tanker(x, y, scale=1):
    vessel = box(12, 0, 17, 13, PAPER) + box(17, -11, 7, 11, PAPER)
    vessel += drawing("M0 17H105L88 36H15Z", PAPER, "none")
    vessel += box(34, 9, 56, 8, GOLD)
    vessel += drawing("M7 43Q20 35 33 43T59 43T85 43T111 43", line="#65a6ad", thickness=2)
    return place(x, y, vessel, scale)


def shipping():
    illustration = box(0, 0, 250, 202, "#1d4654", 12)
    illustration += drawing("M0 0H99L81 31 105 52 77 79 83 95 43 116 0 111Z", "#527b7c", "none")
    illustration += drawing("M250 202H154L164 179 132 160 159 133 172 106 214 92 250 105Z", "#527b7c", "none")
    illustration += tanker(111, 26, .72) + tanker(80, 91, .72) + tanker(17, 150, .72)
    for x, y in [(184, 93), (118, 158)]:
        illustration += dot(x, y, 8, GOLD)
        illustration += drawing(f"M{x-13} {y}H{x+13}M{x} {y-13}V{y+13}", line=GOLD, thickness=3)
    return illustration


def verdict():
    icon = box(10, 10, 60, 50, TEAL, 5)
    for y in (21, 32, 43):
        icon += drawing(f"M20 {y}H59", line=PAPER, thickness=2)
    icon += drawing("M84 64L117 24", line=RED, thickness=10)
    icon += drawing("M105 13L130 34M99 20L124 41", line=NAVY, thickness=10)
    icon += box(83, 65, 50, 7, NAVY, 2)
    return icon


def refinery():
    icon = box(0, 39, 58, 32, TEAL, 2) + box(73, 25, 36, 46, GRAY, 2)
    icon += box(14, 18, 9, 21, TEAL) + box(36, 4, 9, 35, TEAL)
    icon += drawing("M-6 73H127M61 71V8L74 0 85 8V23", line=NAVY, thickness=3)
    icon += drawing("M95 18C78 8 93-4 90-15C114 0 121 7 109 18Z", RED, "none")
    icon += drawing("M101 15Q93 6 102 0Q110 10 101 15", GOLD, "none")
    return icon


def retreat():
    icon = drawing("M5 77L41 10 73 35 102 8 147 64 185 77Z", "#b4c8b5", "none")
    icon += drawing("M73 34L101 9 133 55", line=TEAL, thickness=2)
    icon += drawing("M110 58H38L54 43M38 58L54 73", line=TEAL, thickness=7)
    icon += dot(168, 30, 6, NAVY)
    icon += drawing("M168 38V62M168 46L155 54M168 62L157 78M168 62L178 78", line=NAVY, thickness=5)
    icon += lettering(189, 62, "BUNIA", 12, 700, TEAL)
    return icon


def supermarket():
    icon = box(16, 19, 174, 67, "#e7ceaf", 2)
    icon += box(9, 14, 188, 19, RED, 2)
    icon += lettering(103, 28, "MARKET", 13, 800, PAPER, text_anchor="middle")
    icon += box(32, 43, 42, 39, PAPER) + box(86, 43, 42, 39, PAPER) + box(139, 43, 34, 43, NAVY)
    for x in (52, 106):
        icon += dot(x, 54, 5, GRAY) + drawing(f"M{x-8} 76V68Q{x} 58 {x+8} 68V76Z", GRAY, "none")
    icon += drawing("M0 91H210", line=NAVY, thickness=3)
    icon += drawing("M4 88L13 71H31M181 71H200L209 88", line=TEAL, thickness=4)
    return icon


def jet():
    icon = drawing("M12 57L90 43 116 5 130 2 115 39 190 29Q218 28 230 36L222 44 112 60 88 85 76 87 82 64 24 73Z", TEAL, "none")
    icon += drawing("M152 38L205 34M24 84H64", line="#79a8a4", thickness=3)
    icon += lettering(177, 84, "737-8", 16, 800, TEAL)
    return icon


def compose():
    marks = [box(0, 0, 1024, 1024, PAPER)]
    marks += [box(32, 28, 39, 5, RED), lettering(83, 36, "THE WORLD, TODAY", 15, 800, GRAY, letter_spacing=2),
              lettering(29, 111, "WORLD BRIEF", 65, 800, letter_spacing=-3),
              lettering(992, 65, "24 NOVEMBER", 33, 800, text_anchor="end"),
              lettering(992, 108, "TUESDAY / 2026", 23, 600, GRAY, text_anchor="end"),
              drawing("M32 137H992", thickness=3)]

    marks += [box(32, 157, 960, 260, NAVY, 10),
              lettering(56, 190, "01 / MIDDLE EAST · SHIPPING", 16, 800, GOLD, letter_spacing=1),
              lettering(54, 239, "Shipping under threat", 42, 800, PAPER, letter_spacing=-1),
              lettering(56, 280, "Iran says three tankers hit mines", 26, 500, PAPER),
              lettering(56, 314, "in the Strait of Hormuz.", 26, 500, PAPER),
              lettering(56, 354, "Coalition orders Hodeidah evacuation.", 25, 600, GOLD),
              lettering(56, 393, "IRAN WAR / AL JAZEERA", 13, 700, "#a4c4c8"),
              place(720, 181, shipping())]

    marks += [box(32, 433, 472, 243, "#e1e9e2", 8),
              lettering(52, 465, "02 / US–CHINA · JUSTICE", 16, 800, TEAL),
              lettering(51, 509, "Huawei convicted", 34, 800, letter_spacing=-.8),
              lettering(52, 545, "US jury: trade-secrets conspiracy", 22),
              lettering(52, 575, "and fraud; racketeering acquittal.", 22),
              lettering(52, 652, "BBC / BROOKLYN VERDICT", 12, 700, GRAY),
              place(339, 588, verdict(), .94)]

    marks += [box(520, 433, 472, 243, "#eedfd1", 8),
              lettering(540, 465, "03 / RUSSIA–UKRAINE · WAR", 16, 800, RED),
              lettering(539, 509, "Putin vows retaliation", 31, 800, letter_spacing=-.7),
              lettering(540, 545, "After Ukrainian attacks", 23),
              lettering(540, 575, "on Russian oil refineries.", 23),
              lettering(540, 652, "AL JAZEERA / REUTERS", 12, 700, GRAY),
              place(836, 588, refinery(), 1)]

    for x, shade in [(32, "#e4e9d6"), (357, "#f0e4d7"), (682, "#dce9e9")]:
        marks.append(box(x, 692, 310, 272, shade, 8))

    marks += [lettering(50, 725, "04 / DR CONGO", 17, 800, TEAL),
              lettering(49, 766, "Rebels pull back", 29, 800, letter_spacing=-.6),
              lettering(50, 799, "CRP halts its advance", 22),
              lettering(50, 828, "towards Bunia.", 22),
              place(53, 843, retreat(), 1.04),
              lettering(50, 949, "AL JAZEERA / ANADOLU", 12, 700, GRAY)]

    marks += [lettering(375, 725, "05 / COLOMBIA", 17, 800, RED),
              lettering(374, 766, "Hostages in store", 28, 800, letter_spacing=-.7),
              lettering(375, 799, "Cartagena: about 25", 22),
              lettering(375, 828, "held, president says.", 22),
              place(405, 840, supermarket(), .94),
              lettering(375, 949, "AL JAZEERA / REUTERS", 12, 700, GRAY)]

    marks += [lettering(700, 725, "06 / CHINA–US · TRADE", 16, 800, TEAL),
              lettering(699, 766, "50 Boeing jets", 31, 800, letter_spacing=-.7),
              lettering(700, 799, "Xiamen signs a deal", 22),
              lettering(700, 828, "for 737-8 aircraft.", 22),
              place(714, 849, jet(), 1.03),
              lettering(700, 949, "AL JAZEERA / REUTERS", 12, 700, GRAY)]

    marks += [drawing("M32 982H992", line="#aeb7af", thickness=1),
              lettering(32, 1006, "24 NOV 2026 / SIX STORIES / ORIGINAL EDITORIAL ILLUSTRATIONS", 13, 700, GRAY),
              lettering(992, 1006, "ONE DAY. ONE FRAME.", 13, 800, TEAL, text_anchor="end")]
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">'
            '<title>World Brief — 24 November 2026</title>'
            '<desc>Six news stories: Hormuz and Hodeidah, Huawei, Russian energy strikes, '
            'DR Congo, Cartagena hostages, and Xiamen aircraft order. All illustrations are symbolic.</desc>'
            '<g font-family="DejaVu Sans, sans-serif">' + "".join(marks) + '</g></svg>')


def crop_render(path):
    """Keep the top 1024 rows of a taller browser capture, losslessly.

    Chromium can reserve space for its window chrome even in headless mode.
    A taller viewport ensures that the complete SVG is painted before cropping.
    PNG scanline filters remain valid because only trailing rows are removed.
    """
    image = path.read_bytes()
    if image[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Chromium did not produce a PNG")
    offset, compressed = 8, bytearray()
    while offset < len(image):
        length = struct.unpack(">I", image[offset:offset + 4])[0]
        kind = image[offset + 4:offset + 8]
        data = image[offset + 8:offset + 8 + length]
        if kind == b"IHDR":
            header = data
        elif kind == b"IDAT":
            compressed.extend(data)
        offset += length + 12
    width, height, depth, color, compression, filtering, interlace = struct.unpack(">IIBBBBB", header)
    if width != 1024 or height < 1024 or depth != 8 or color not in (2, 6) or interlace:
        raise ValueError("Unexpected browser PNG format")
    pixels = zlib.decompress(compressed)
    stride = 1 + width * (3 if color == 2 else 4)
    if len(pixels) != stride * height:
        raise ValueError("Incomplete browser PNG")

    def chunk(kind, data):
        return (struct.pack(">I", len(data)) + kind + data
                + struct.pack(">I", zlib.crc32(kind + data)))

    header = struct.pack(">IIBBBBB", width, 1024, depth, color, compression, filtering, interlace)
    path.write_bytes(image[:8] + chunk(b"IHDR", header)
                     + chunk(b"IDAT", zlib.compress(pixels[:stride * 1024], 9))
                     + chunk(b"IEND", b""))


def build():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--svg-only", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    source = root / "entry.svg"
    source.write_text(compose(), encoding="utf-8")
    if args.svg_only:
        return
    chromium = shutil.which("chromium") or shutil.which("chromium-browser")
    if chromium is None:
        raise SystemExit("Install a local Chromium browser to rebuild the PNG")
    with tempfile.TemporaryDirectory(prefix="news24-render-") as profile:
        subprocess.run([chromium, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        "--disable-dev-shm-usage", "--no-first-run", "--no-default-browser-check",
                        f"--user-data-dir={profile}", "--force-device-scale-factor=1", "--window-size=1024,1200",
                        f"--screenshot={root / 'entry.png'}", source.as_uri()], check=True, timeout=45)
    crop_render(root / "entry.png")
    print(f"Rendered {root / 'entry.png'}")


if __name__ == "__main__":
    build()
