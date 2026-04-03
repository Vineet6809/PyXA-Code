from __future__ import annotations

import importlib


def dhash_hex_from_bytes(image_bytes: bytes) -> str:
    """Compute a perceptual dHash from image bytes using Pillow + imagehash."""

    pillow_image_module = importlib.import_module("PIL.Image")
    imagehash = importlib.import_module("imagehash")
    io = importlib.import_module("io")

    image = pillow_image_module.open(io.BytesIO(image_bytes)).convert("RGB")
    return str(imagehash.dhash(image))


def hamming_distance(hash_a: str, hash_b: str) -> int:
    if len(hash_a) != len(hash_b):
        raise ValueError("Hash lengths must match for Hamming distance")
    return sum(ch1 != ch2 for ch1, ch2 in zip(hash_a, hash_b))


def screen_changed(hash_before: str, hash_after: str, threshold: int = 8) -> bool:
    return hamming_distance(hash_before, hash_after) >= threshold
