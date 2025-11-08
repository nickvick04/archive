import json
import sys
from pathlib import Path

REQUIRED_KEYS = {"id", "icpc_id", "name", "label", "organization_id", "group_ids"}

def verify_team_entry(entry):
    errors = []

    # Identify team for better error messages
    team_id = entry.get("id", "?")

    # Check that entry is a dictionary
    if not isinstance(entry, dict):
        errors.append(f"Team with id={team_id} is not a JSON object.")
        return errors

    # Check required keys
    missing_keys = REQUIRED_KEYS - entry.keys()
    if missing_keys:
        errors.append(f"Team id={team_id} missing keys: {', '.join(missing_keys)}")

    # Unexpected keys
    unexpected_keys = set(entry.keys()) - REQUIRED_KEYS
    if unexpected_keys:
        errors.append(f"Team id={team_id} has unexpected keys: {', '.join(unexpected_keys)}")

    # Type validation
    if "id" in entry and not isinstance(entry["id"], str):
        errors.append(f"Team id={team_id} -> 'id' should be a string.")
    if "icpc_id" in entry and not isinstance(entry["icpc_id"], str):
        errors.append(f"Team id={team_id} -> 'icpc_id' should be a string.")
    if "label" in entry and not isinstance(entry["label"], str):
        errors.append(f"Team id={team_id} -> 'label' should be a string.")
    if "organization_id" in entry and not isinstance(entry["organization_id"], str):
        errors.append(f"Team id={team_id} -> 'organization_id' should be a string.")
    if "name" in entry and not isinstance(entry["name"], str):
        errors.append(f"Team id={team_id} -> 'name' should be a string.")
    if "group_ids" in entry and not isinstance(entry["group_ids"], list):
        errors.append(f"Team id={team_id} -> 'group_ids' should be a list.")

    # Value checks
    for field in ["id", "icpc_id", "label"]:
        if field in entry and not entry[field].isdigit():
            errors.append(f"Team id={team_id} -> '{field}' should be a numeric string (got '{entry[field]}').")

    if "organization_id" in entry and entry["organization_id"].strip() == "":
        errors.append(f"Team id={team_id} has an empty organization_id.")
    if "name" in entry and entry["name"].strip() == "":
        errors.append(f"Team id={team_id} has an empty name.")

    return errors


def verify_teams_json(filepath: Path):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format: {e}")
        return False
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return False

    if not isinstance(data, list):
        print("Root element must be a list.")
        return False

    all_errors = []
    for entry in data:
        all_errors.extend(verify_team_entry(entry))

    if all_errors:
        print("Validation errors found:")
        for err in all_errors:
            print("  -", err)
        return False
    else:
        print("teams.json is valid!")
        return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify_teams_json.py <path_to_teams.json>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    valid = verify_teams_json(filepath)
    sys.exit(0 if valid else 1)