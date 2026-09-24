from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


PROVIDER_NAME = "pexels"
PROVIDER_VERSION = "1.0.0"
API_BASE = "https://api.pexels.com/v1"
API_KEY_ENV = "PEXELS_API_KEY"
LICENSE_URL = "https://www.pexels.com/license/"
API_DOCS_URL = "https://www.pexels.com/api/documentation/"

SEARCH_PER_PAGE = 12
HTTP_TIMEOUT_SEC = 25
MAX_IMAGE_BYTES = 20 * 1024 * 1024
MAX_VIDEO_BYTES = 80 * 1024 * 1024
CHUNK_BYTES = 1024 * 1024
SUPPORTED_ASSET_TYPES = {"stock_image", "stock_video"}


class PexelsProviderError(RuntimeError):
    pass


def _now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PexelsProviderError(f"{name} must be a non-empty string")
    return value.strip()


def _slug(value: str) -> str:
    return (
        re.sub(r"[^a-zA-Z0-9._-]+", "_", value.strip())
        .strip("._-")
        or "asset"
    )


def _sidecar(media_path: Path) -> Path:
    return media_path.with_suffix(media_path.suffix + ".license.json")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    temp.replace(path)


def is_configured() -> bool:
    return bool(os.getenv(API_KEY_ENV, "").strip())


def _api_get(
    endpoint: str,
    params: dict[str, str | int],
) -> tuple[dict[str, Any], str | None]:
    key = os.getenv(API_KEY_ENV, "").strip()

    if not key:
        raise PexelsProviderError(f"{API_KEY_ENV} is not set")

    request = Request(
        f"{API_BASE}{endpoint}?{urlencode(params)}",
        headers={
            "Authorization": key,
            "Accept": "application/json",
            "User-Agent": "FlowMind/1.0",
        },
    )

    try:
        with urlopen(
            request,
            timeout=HTTP_TIMEOUT_SEC,
        ) as response:
            payload = json.loads(
                response.read().decode("utf-8")
            )

            if not isinstance(payload, dict):
                raise PexelsProviderError(
                    "Pexels API returned non-object JSON"
                )

            return (
                payload,
                response.headers.get(
                    "X-Ratelimit-Remaining"
                ),
            )

    except HTTPError as exc:
        if exc.code == 429:
            raise PexelsProviderError(
                "Pexels API rate limit exceeded"
            ) from exc

        raise PexelsProviderError(
            f"Pexels API HTTP {exc.code}"
        ) from exc

    except URLError as exc:
        raise PexelsProviderError(
            f"Pexels API network error: {exc.reason}"
        ) from exc

    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        raise PexelsProviderError(
            "Pexels API returned invalid JSON"
        ) from exc

    except TimeoutError as exc:
        raise PexelsProviderError(
            "Pexels API request timed out"
        ) from exc


def _download(
    url: str,
    destination: Path,
    max_bytes: int,
) -> int:
    request = Request(
        url,
        headers={
            "User-Agent": "FlowMind/1.0",
        },
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temp = destination.with_suffix(
        destination.suffix + ".part"
    )

    if temp.exists():
        temp.unlink()

    written = 0

    try:
        with urlopen(
            request,
            timeout=HTTP_TIMEOUT_SEC,
        ) as response:
            declared = response.headers.get(
                "Content-Length"
            )

            if declared:
                try:
                    declared_size = int(declared)
                except ValueError:
                    declared_size = 0

                if declared_size > max_bytes:
                    raise PexelsProviderError(
                        "provider media too large: "
                        f"{declared_size} > {max_bytes}"
                    )

            with temp.open("wb") as handle:
                while True:
                    chunk = response.read(
                        CHUNK_BYTES
                    )

                    if not chunk:
                        break

                    written += len(chunk)

                    if written > max_bytes:
                        raise PexelsProviderError(
                            "provider media exceeded "
                            "size limit: "
                            f"{written} > {max_bytes}"
                        )

                    handle.write(chunk)

        if written <= 0:
            raise PexelsProviderError(
                "provider media download was empty"
            )

        temp.replace(destination)
        return written

    except HTTPError as exc:
        raise PexelsProviderError(
            f"media download HTTP {exc.code}"
        ) from exc

    except URLError as exc:
        raise PexelsProviderError(
            "media download network error: "
            f"{exc.reason}"
        ) from exc

    except TimeoutError as exc:
        raise PexelsProviderError(
            "media download timed out"
        ) from exc

    finally:
        if temp.exists():
            temp.unlink()


def _cached(
    output_dir: Path,
    asset_id: str,
    asset_type: str,
    asset_query: str,
) -> dict[str, Any] | None:
    if not output_dir.exists():
        return None

    for metadata_path in sorted(
        output_dir.glob("*.license.json")
    ):
        try:
            metadata = json.loads(
                metadata_path.read_text(
                    encoding="utf-8"
                )
            )
        except (
            OSError,
            json.JSONDecodeError,
        ):
            continue

        if not isinstance(metadata, dict):
            continue

        if (
            metadata.get("source_provider")
            != PROVIDER_NAME
        ):
            continue

        if (
            metadata.get("license_status")
            != "cleared"
        ):
            continue

        identity = (
            metadata.get("asset_id"),
            metadata.get("asset_type"),
            metadata.get("asset_query"),
        )

        if identity != (
            asset_id,
            asset_type,
            asset_query,
        ):
            continue

        media_path = Path(
            str(metadata_path)[
                : -len(".license.json")
            ]
        )

        if (
            not media_path.is_file()
            or media_path.stat().st_size <= 0
        ):
            continue

        key = metadata.get(
            "provider_asset_key"
        )
        source_url = metadata.get(
            "source_url"
        )
        license_note = metadata.get(
            "license_note"
        )

        values = (
            key,
            source_url,
            license_note,
        )

        if not all(
            isinstance(value, str)
            and value.strip()
            for value in values
        ):
            continue

        return {
            "provider_asset_key": key.strip(),
            "provider_asset_id": str(
                metadata.get(
                    "provider_asset_id",
                    "",
                )
            ).strip(),
            "source_provider": PROVIDER_NAME,
            "source_url": source_url.strip(),
            "local_path": media_path,
            "license_note": license_note.strip(),
            "attribution_text": str(
                metadata.get(
                    "attribution_text",
                    "",
                )
            ).strip(),
            "attribution_url": str(
                metadata.get(
                    "attribution_url",
                    "",
                )
            ).strip(),
            "cache_hit": True,
            "rate_limit_remaining": None,
        }

    return None


def _video_file(
    files: Any,
) -> dict[str, Any] | None:
    if not isinstance(files, list):
        return None

    ranked: list[
        tuple[
            tuple[int, int],
            dict[str, Any],
        ]
    ] = []

    for item in files:
        if (
            not isinstance(item, dict)
            or item.get("file_type")
            != "video/mp4"
        ):
            continue

        width = item.get("width")
        height = item.get("height")
        link = item.get("link")

        if (
            not isinstance(width, int)
            or width <= 0
        ):
            continue

        if (
            not isinstance(height, int)
            or height <= 0
        ):
            continue

        if (
            not isinstance(link, str)
            or not link.strip()
        ):
            continue

        area = width * height

        if (
            width <= 1920
            and height <= 1080
        ):
            rank = (0, -area)
        else:
            rank = (1, area)

        ranked.append(
            (rank, item)
        )

    if not ranked:
        return None

    ranked.sort(
        key=lambda pair: pair[0]
    )

    return ranked[0][1]


def _select_image(
    payload: dict[str, Any],
    used_ids: set[str],
) -> dict[str, str] | None:
    photos = payload.get("photos")

    if not isinstance(photos, list):
        raise PexelsProviderError(
            "Pexels photo response missing photos"
        )

    for photo in photos:
        if (
            not isinstance(photo, dict)
            or not isinstance(
                photo.get("id"),
                int,
            )
        ):
            continue

        provider_id = str(photo["id"])
        key = (
            f"pexels:photo:{provider_id}"
        )

        if key in used_ids:
            continue

        src = photo.get("src")

        if not isinstance(src, dict):
            continue

        download_url = src.get("original")
        source_url = photo.get("url")
        creator_name = photo.get(
            "photographer"
        )
        creator_url = photo.get(
            "photographer_url"
        )

        values = (
            download_url,
            source_url,
            creator_name,
            creator_url,
        )

        if not all(
            isinstance(value, str)
            and value.strip()
            for value in values
        ):
            continue

        suffix = Path(
            urlparse(
                download_url
            ).path
        ).suffix.lower()

        if suffix in {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        }:
            extension = suffix
        else:
            extension = ".jpg"

        return {
            "provider_asset_key": key,
            "provider_asset_id": provider_id,
            "download_url": download_url.strip(),
            "source_url": source_url.strip(),
            "creator_name": creator_name.strip(),
            "creator_url": creator_url.strip(),
            "extension": extension,
            "media_label": "Photo",
        }

    return None


def _select_video(
    payload: dict[str, Any],
    used_ids: set[str],
) -> dict[str, str] | None:
    videos = payload.get("videos")

    if not isinstance(videos, list):
        raise PexelsProviderError(
            "Pexels video response missing videos"
        )

    for video in videos:
        if (
            not isinstance(video, dict)
            or not isinstance(
                video.get("id"),
                int,
            )
        ):
            continue

        provider_id = str(video["id"])
        key = (
            f"pexels:video:{provider_id}"
        )

        if key in used_ids:
            continue

        user = video.get("user")
        selected_file = _video_file(
            video.get("video_files")
        )
        source_url = video.get("url")

        if (
            not isinstance(user, dict)
            or selected_file is None
        ):
            continue

        creator_name = user.get("name")
        creator_url = user.get("url")
        download_url = selected_file.get(
            "link"
        )

        values = (
            source_url,
            creator_name,
            creator_url,
            download_url,
        )

        if not all(
            isinstance(value, str)
            and value.strip()
            for value in values
        ):
            continue

        return {
            "provider_asset_key": key,
            "provider_asset_id": provider_id,
            "download_url": download_url.strip(),
            "source_url": source_url.strip(),
            "creator_name": creator_name.strip(),
            "creator_url": creator_url.strip(),
            "extension": ".mp4",
            "media_label": "Video",
        }

    return None


def resolve_stock_asset(
    *,
    asset_id: str,
    asset_type: str,
    asset_query: str,
    output_dir: Path,
    used_provider_ids: set[str],
) -> dict[str, Any] | None:
    asset_id = _text(
        asset_id,
        "asset_id",
    )
    asset_type = _text(
        asset_type,
        "asset_type",
    )
    asset_query = _text(
        asset_query,
        "asset_query",
    )

    if (
        asset_type
        not in SUPPORTED_ASSET_TYPES
    ):
        return None

    cached = _cached(
        output_dir,
        asset_id,
        asset_type,
        asset_query,
    )

    if (
        cached is not None
        and cached["provider_asset_key"]
        not in used_provider_ids
    ):
        return cached

    if asset_type == "stock_image":
        endpoint = "/search"
        max_bytes = MAX_IMAGE_BYTES
        selector = _select_image
    else:
        endpoint = "/videos/search"
        max_bytes = MAX_VIDEO_BYTES
        selector = _select_video

    payload, remaining = _api_get(
        endpoint,
        {
            "query": asset_query,
            "locale": "en-US",
            "per_page": SEARCH_PER_PAGE,
            "page": 1,
        },
    )

    selected = selector(
        payload,
        used_provider_ids,
    )

    if selected is None:
        return None

    media_path = output_dir / (
        f"{_slug(asset_id)}"
        f"__pexels_"
        f"{_slug(selected['provider_asset_id'])}"
        f"{selected['extension']}"
    )

    size_bytes = _download(
        selected["download_url"],
        media_path,
        max_bytes,
    )

    attribution_text = (
        f"{selected['media_label']} by "
        f"{selected['creator_name']} "
        "on Pexels"
    )

    license_note = (
        "Pexels License applies; Pexels permits "
        "free personal and commercial use. "
        "Third-party rights for depicted people, "
        "logos, trademarks, or works are not "
        "evaluated by this adapter and remain "
        "subject to FlowMind compliance review."
    )

    metadata = {
        "asset_id": asset_id,
        "asset_type": asset_type,
        "asset_query": asset_query,
        "source_provider": PROVIDER_NAME,
        "provider_version": PROVIDER_VERSION,
        "provider_asset_key": (
            selected["provider_asset_key"]
        ),
        "provider_asset_id": (
            selected["provider_asset_id"]
        ),
        "source_url": selected["source_url"],
        "creator_name": (
            selected["creator_name"]
        ),
        "creator_url": (
            selected["creator_url"]
        ),
        "license_status": "cleared",
        "license_name": "Pexels License",
        "license_url": LICENSE_URL,
        "license_note": license_note,
        "third_party_rights_review": (
            "not_evaluated"
        ),
        "attribution_text": (
            attribution_text
        ),
        "attribution_url": (
            selected["source_url"]
        ),
        "api_docs_url": API_DOCS_URL,
        "downloaded_at": _now(),
        "download_size_bytes": size_bytes,
    }

    _write_json(
        _sidecar(media_path),
        metadata,
    )

    return {
        "provider_asset_key": (
            selected["provider_asset_key"]
        ),
        "provider_asset_id": (
            selected["provider_asset_id"]
        ),
        "source_provider": PROVIDER_NAME,
        "source_url": (
            selected["source_url"]
        ),
        "local_path": media_path,
        "license_note": license_note,
        "attribution_text": (
            attribution_text
        ),
        "attribution_url": (
            selected["source_url"]
        ),
        "cache_hit": False,
        "rate_limit_remaining": remaining,
    }
