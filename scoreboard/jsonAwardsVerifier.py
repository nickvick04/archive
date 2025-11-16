import json
import sys
from pathlib import Path

REQUIRED_KEYS = {"id", "citation", "team_ids"}

def validate_team_ids(value, award_id):
    errors = []

    # Case 1: team_ids is a list of integers
    if isinstance(value, list):
        for v in value:
            if not isinstance(v, int):
                errors.append(
                    f"Award id='{award_id}' -> team_ids list contains non-integer value '{v}'"
                )
        return errors

    # Case 2: team_ids is a dict mapping {problem_index: team_id}
    if isinstance(value, dict):
        for k, v in value.items():
            if not isinstance(v, int):
                errors.append(
                    f"Award id='{award_id}' -> team_ids dict has non-int value '{v}' for key '{k}'"
                )
        return errors

    # Invalid type
    errors.append(
        f"Award id='{award_id}' -> 'team_ids' must be list[int] or dict[str,int], got: {type(value).__name__}"
    )
    return errors


def verify_award_entry(entry):
    errors = []

    award_id = entry.get("id", "?")

    if not isinstance(entry, dict):
        return [f"Award id='{award_id}' is not a JSON object"]

    # Required keys
    missing = REQUIRED_KEYS - entry.keys()
    if missing:
        errors.append(f"Award id='{award_id}' missing keys: {', '.join(missing)}")

    # Unexpected keys
    unexpected = set(entry.keys()) - REQUIRED_KEYS
    if unexpected:
        errors.append(f"Award id='{award_id}' has unexpected keys: {', '.join(unexpected)}")

    # Validate types
    if "id" in entry and not isinstance(entry["id"], str):
        errors.append(f"Award id='{award_id}' -> 'id' must be a string")

    if "citation" in entry and not isinstance(entry["citation"], str):
        errors.append(f"Award id='{award_id}' -> 'citation' must be a string")

    if "id" in entry and entry["id"].strip() == "":
        errors.append(f"Award has empty id field")

    if "citation" in entry and entry["citation"].strip() == "":
        errors.append(f"Award id='{award_id}' has empty citation")

    # Validate team_ids
    if "team_ids" in entry:
        errors.extend(validate_team_ids(entry["team_ids"], award_id))

    return errors


def verify_awards_json(filepath: Path):
    try:
        data = json.loads(Path(filepath).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Failed to load JSON: {e}")
        return False

    if not isinstance(data, list):
        print("❌ Root must be a list.")
        return False

    errors = []
    for entry in data:
        errors.extend(verify_award_entry(entry))

    if errors:
        print("❌ Validation errors found:")
        for err in errors:
            print("  -", err)
        return False

    print("✅ awards.json is valid!")
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify_awards_json.py awards.json")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    ok = verify_awards_json(filepath)
    sys.exit(0 if ok else 1)
