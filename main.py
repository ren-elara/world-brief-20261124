"""Write the day's original, pre-rendered news illustration without a network."""

import os
from pathlib import Path


def publish_image():
    artwork = Path(__file__).resolve().with_name("entry.png").read_bytes()
    if not artwork.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("The committed artwork must be a PNG")
    if len(artwork) > 1_048_576:
        raise ValueError("The artwork exceeds the competition's image limit")
    destination = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination.mkdir(parents=True, exist_ok=True)
    destination.chmod(0o755)
    target = destination / "entry.png"
    target.write_bytes(artwork)
    target.chmod(0o644)


if __name__ == "__main__":
    publish_image()
