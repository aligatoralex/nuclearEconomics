import json
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, model_validator


class ValueRange(BaseModel):
    min: float
    mid: float | None = None
    max: float


class AssumptionEntry(BaseModel):
    parameter: str
    value_or_range: ValueRange
    distribution_type: Literal["uniform", "triangular", "normal", "lognormal", "beta"]
    tier: Literal[1, 2, 3]
    source: str
    date_retrieved: date
    rationale: str
    requires_confirmation: bool

    @model_validator(mode="after")
    def tier3_requires_confirmation(self) -> "AssumptionEntry":
        if self.tier == 3 and self.requires_confirmation is not True:
            raise ValueError(
                "Tier 3 assumptions (unsourced working assumptions) must have "
                "requires_confirmation=True"
            )
        return self


def load_assumptions_registry(path: Path) -> list[AssumptionEntry]:
    """Loads and validates every entry of the assumptions registry JSON."""
    with open(path) as f:
        raw_entries = json.load(f)
    return [AssumptionEntry(**entry) for entry in raw_entries]
