import pytest
from pydantic import ValidationError

from src.schemas import AssumptionEntry

BASE_ENTRY = {
    "parameter": "example_placeholder_param",
    "value_or_range": {"min": 1.0, "mid": 2.0, "max": 3.0},
    "distribution_type": "uniform",
    "tier": 3,
    "source": "placeholder — no confirmed source",
    "date_retrieved": "2026-08-06",
    "rationale": "placeholder Tier 3 example for schema validation test",
}


def test_tier3_requires_confirmation_enforced():
    with pytest.raises(ValidationError):
        AssumptionEntry(**BASE_ENTRY, requires_confirmation=False)

    AssumptionEntry(**BASE_ENTRY, requires_confirmation=True)
