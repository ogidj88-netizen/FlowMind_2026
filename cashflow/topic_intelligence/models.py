from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, HttpUrl


class SeedSource(str, Enum):
    SOCIAL_SIGNAL = "SOCIAL_SIGNAL"
    FACT_SIGNAL = "FACT_SIGNAL"


class GapStatus(str, Enum):
    GAP_DETECTED = "GAP_DETECTED"
    INSTRUCTIONAL_COVERAGE_EXISTS = "INSTRUCTIONAL_COVERAGE_EXISTS"
    UNKNOWN = "UNKNOWN"


class Verdict(str, Enum):
    PRIORITY = "PRIORITY"
    BACKLOG = "BACKLOG"
    KILL = "KILL"


class ValidatedTopic(BaseModel):
    entity: str = Field(..., min_length=1, max_length=120)
    seed_source: SeedSource
    seed: str = Field(..., min_length=1, max_length=300)
    anchor_demand: str = Field(..., min_length=1, max_length=200)
    utility: str = Field(..., min_length=1, max_length=300)
    gap_status: GapStatus
    pain_evidence: str = Field(..., min_length=1, max_length=5000)
    source_link: HttpUrl | None = None
    source_type: str = Field(default="unknown", min_length=1, max_length=50)
    source_label: str = Field(default="unknown", min_length=1, max_length=120)
    verdict: Verdict

    class Config:
        frozen = True
