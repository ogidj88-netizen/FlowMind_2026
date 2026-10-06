from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


PROVIDER_NAME = "flowmind_deterministic"
PROVIDER_VERSION = "1.0.0"
SUPPORTED_ASSET_TYPES = {
    "simple_motion_text",
    "chart_or_bill_visual",
    "screen_style_visual",
}
CANVAS_SIZE = (1920, 1080)
BACKGROUND = (18, 22, 28)
PANEL = (31, 38, 48)
TEXT = (245, 247, 250)
MUTED = (174, 183, 194)
ACCENT = (79, 156, 249)
SUCCESS = (87, 201, 122)
FONT_CANDIDATES = (
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
)


class DeterministicVisualProviderError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DeterministicVisualProviderError(f"{name} must be a non-empty string")
    return value.strip()


def _slug(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "_", value.strip()).strip("._-") or "asset"


def _sidecar(media_path: Path) -> Path:
    return media_path.with_suffix(media_path.suffix + ".license.json")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    temp.replace(path)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = list(FONT_CANDIDATES)
    if bold:
        candidates.insert(0, "/System/Library/Fonts/Supplemental/Arial Bold.ttf")
    for candidate in candidates:
        path = Path(candidate)
        if not path.is_file():
            continue
        try:
            return ImageFont.truetype(str(path), size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def _headline(draw: ImageDraw.ImageDraw, query: str) -> None:
    font = _font(72, bold=True)
    lines = _wrap(draw, query, font, 1540)[:4]
    y = 120
    for line in lines:
        draw.text((190, y), line, font=font, fill=TEXT)
        y += 88


def _render_simple_motion_text(draw: ImageDraw.ImageDraw, query: str) -> None:
    _headline(draw, query)
    draw.rounded_rectangle((190, 650, 1730, 850), radius=34, fill=PANEL)
    draw.rectangle((190, 650, 214, 850), fill=ACCENT)
    draw.text((270, 705), "KEY IDEA", font=_font(34, bold=True), fill=ACCENT)
    draw.text((270, 765), "Focus on the mechanism, not the assumption.", font=_font(44), fill=TEXT)


def _render_chart(draw: ImageDraw.ImageDraw, query: str) -> None:
    _headline(draw, query)
    left, top, right, bottom = 220, 560, 1700, 900
    draw.line((left, bottom, right, bottom), fill=MUTED, width=4)
    draw.line((left, top, left, bottom), fill=MUTED, width=4)
    labels = (("Usage", 0.48), ("Rate", 0.72), ("Fixed", 0.36), ("Timing", 0.58))
    bar_width = 210
    gap = 115
    x = left + 110
    for label, ratio in labels:
        height = int((bottom - top - 60) * ratio)
        y = bottom - height
        draw.rounded_rectangle((x, y, x + bar_width, bottom), radius=18, fill=ACCENT)
        draw.text((x, bottom + 28), label, font=_font(30, bold=True), fill=TEXT)
        x += bar_width + gap


def _render_screen(draw: ImageDraw.ImageDraw, query: str) -> None:
    _headline(draw, query)
    draw.rounded_rectangle((210, 520, 1710, 930), radius=36, fill=PANEL)
    items = ("Compare usage", "Check the rate", "Review fixed charges", "Check billing period")
    y = 585
    for item in items:
        draw.rounded_rectangle((275, y, 325, y + 50), radius=12, fill=SUCCESS)
        draw.line((288, y + 26, 300, y + 38, 316, y + 13), fill=BACKGROUND, width=6)
        draw.text((365, y - 2), item, font=_font(40), fill=TEXT)
        y += 82


def _render(asset_type: str, query: str, destination: Path) -> None:
    image = Image.new("RGB", CANVAS_SIZE, BACKGROUND)
    draw = ImageDraw.Draw(image)
    if asset_type == "simple_motion_text":
        _render_simple_motion_text(draw, query)
    elif asset_type == "chart_or_bill_visual":
        _render_chart(draw, query)
    elif asset_type == "screen_style_visual":
        _render_screen(draw, query)
    else:
        raise DeterministicVisualProviderError(f"unsupported asset_type: {asset_type}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temp = destination.with_name(destination.stem + ".tmp" + destination.suffix)
    try:
        image.save(temp, format="PNG", optimize=True)
        if not temp.is_file() or temp.stat().st_size <= 0:
            raise DeterministicVisualProviderError("generated visual file is empty")
        temp.replace(destination)
    finally:
        image.close()
        if temp.exists():
            temp.unlink()


def _cached(output_dir: Path, asset_id: str, asset_type: str, asset_query: str) -> dict[str, Any] | None:
    if not output_dir.exists():
        return None
    for metadata_path in sorted(output_dir.glob("*.license.json")):
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(metadata, dict):
            continue
        if metadata.get("source_provider") != PROVIDER_NAME or metadata.get("license_status") != "cleared":
            continue
        identity = (metadata.get("asset_id"), metadata.get("asset_type"), metadata.get("asset_query"))
        if identity != (asset_id, asset_type, asset_query):
            continue
        media_path = Path(str(metadata_path)[:-len(".license.json")])
        if not media_path.is_file() or media_path.stat().st_size <= 0:
            continue
        license_note = metadata.get("license_note")
        provider_asset_key = metadata.get("provider_asset_key")
        if not isinstance(license_note, str) or not license_note.strip():
            continue
        if not isinstance(provider_asset_key, str) or not provider_asset_key.strip():
            continue
        return {
            "provider_asset_key": provider_asset_key.strip(),
            "provider_asset_id": asset_id,
            "source_provider": PROVIDER_NAME,
            "source_url": None,
            "local_path": media_path,
            "license_note": license_note.strip(),
            "attribution_text": "Generated by FlowMind",
            "attribution_url": None,
            "cache_hit": True,
        }
    return None


def resolve_visual_asset(*, asset_id: str, asset_type: str, asset_query: str, output_dir: Path) -> dict[str, Any] | None:
    asset_id = _text(asset_id, "asset_id")
    asset_type = _text(asset_type, "asset_type")
    asset_query = _text(asset_query, "asset_query")
    if asset_type not in SUPPORTED_ASSET_TYPES:
        return None

    cached = _cached(output_dir, asset_id, asset_type, asset_query)
    if cached is not None:
        return cached

    provider_asset_key = f"{PROVIDER_NAME}:{asset_type}:{_slug(asset_id)}"
    media_path = output_dir / f"{_slug(asset_id)}__{PROVIDER_NAME}.png"
    _render(asset_type, asset_query, media_path)

    license_note = (
        "Visual generated deterministically by FlowMind from project-owned text and geometric primitives; "
        "no third-party media asset is embedded by this provider."
    )
    metadata = {
        "asset_id": asset_id,
        "asset_type": asset_type,
        "asset_query": asset_query,
        "source_provider": PROVIDER_NAME,
        "provider_version": PROVIDER_VERSION,
        "provider_asset_key": provider_asset_key,
        "provider_asset_id": asset_id,
        "source_url": None,
        "license_status": "cleared",
        "license_name": "FlowMind generated visual",
        "license_url": None,
        "license_note": license_note,
        "third_party_rights_review": "not_applicable",
        "attribution_text": "Generated by FlowMind",
        "attribution_url": None,
        "generated_at": _now(),
        "generated_size_bytes": media_path.stat().st_size,
        "canvas_width": CANVAS_SIZE[0],
        "canvas_height": CANVAS_SIZE[1],
    }
    _write_json(_sidecar(media_path), metadata)

    return {
        "provider_asset_key": provider_asset_key,
        "provider_asset_id": asset_id,
        "source_provider": PROVIDER_NAME,
        "source_url": None,
        "local_path": media_path,
        "license_note": license_note,
        "attribution_text": "Generated by FlowMind",
        "attribution_url": None,
        "cache_hit": False,
    }
