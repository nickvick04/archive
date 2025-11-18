import json
import sys
from pathlib import Path

REQUIRED_KEYS = {"problem_id", "name"}

def verify_problem_entry(entry):
    errors = []
    pid = entry.get("problem_id", "?")

    if not isinstance(entry, dict):
        return [f"Problem entry with id='{pid}' is not a JSON object"]

    # Missing keys
    missing = REQUIRED_KEYS - entry.keys()
    if missing:
        errors.append(f"Problem id='{pid}' missing keys: {', '.join(missing)}")

    # Unexpected keys
    unexpected = set(entry.keys()) - REQUIRED_KEYS
    if unexpected:
        errors.append(f"Problem id='{pid}' has unexpected keys: {', '.join(unexpected)}")

    # Type checks
    if "problem_id" in entry and not isinstance(entry["problem_id"], str):
        errors.append(f"Problem id='{pid}' -> 'problem_id' must be a string")

    if "name" in entry and not isinstance(entry["name"], str):
        errors.append(f"Problem id='{pid}' -> 'name' must be a string")

    # Value checks
    if "problem_id" in entry and entry["problem_id"].strip() == "":
        errors.append(f"Problem has empty problem_id")

    if "name" in entry and entry["name"].strip() == "":
        errors.append(f"Problem id='{pid}' has empty name")

    return errors


def verify_problem_json(filepath: Path):
    try:
        data = json.loads(Path(filepath).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Failed to load JSON: {e}")
        return False

    if not isinstance(data, list):
        print("Root must be a list.")
        return False

    errors = []
    for entry in data:
        errors.extend(verify_problem_entry(entry))

    if errors:
        print("Validation errors found:")
        for err in errors:
            print("  -", err)
        return False

    print("problemName.json is valid!")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify_problemName_json.py problemName.json")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    ok = verify_problem_json(filepath)
    sys.exit(0 if ok else 1)
