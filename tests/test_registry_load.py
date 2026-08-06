from pathlib import Path

from src.schemas import load_assumptions_registry

REGISTRY_PATH = (
    Path(__file__).resolve().parent.parent / "config" / "assumptions_registry.json"
)


def test_registry_loads_all_entries_valid():
    entries = load_assumptions_registry(REGISTRY_PATH)

    assert len(entries) == 14
    for entry in entries:
        if entry.tier == 3:
            assert entry.requires_confirmation is True
