import json
import sys

def verify_scoreboard(filename):
    with open(filename, "r") as f:
        data = json.load(f)

    errors = []

    # Validate top-level required keys 
    required_top = {
        "type", "title", "time", "contest_time",
        "state", "rows"
    }
    missing_top = required_top - data.keys()
    if missing_top:
        errors.append(f"Missing top-level fields: {missing_top}")

    # Validate 'state' object 
    required_state = {
        "started", "ended", "frozen",
        "thawed", "finalized", "end_of_updates"
    }
    if "state" in data:
        missing_state = required_state - data["state"].keys()
        if missing_state:
            errors.append(f"State missing fields: {missing_state}")
    else:
        errors.append("Missing 'state' object.")

    # Validate rows
    if "rows" in data:
        for i, row in enumerate(data["rows"]):
            required_row = {"rank", "team_id", "score", "problems"}
            missing_row = required_row - row.keys()
            if missing_row:
                errors.append(f"Row {i}: Missing row fields {missing_row}")
                continue

            team_id = row["team_id"]
            if not team_id or team_id.strip() == "":
                errors.append(f"Row {i}: EMPTY team_id")

            required_score = {"num_solved", "total_time", "time"}
            missing_score = required_score - row["score"].keys()
            if missing_score:
                errors.append(f"Row {i} (team_id={team_id}): missing score fields {missing_score}")

            for p, problem in enumerate(row["problems"]):
                required_problem = {"problem_id", "num_judged", "num_pending", "solved"}
                missing_prob = required_problem - problem.keys()
                if missing_prob:
                    errors.append(
                        f"Row {i} (team_id={team_id}), Problem {p}: Missing fields {missing_prob}"
                    )

                if problem.get("solved") == "True" and "time" not in problem:
                    errors.append(
                        f"Row {i} (team_id={team_id}), Problem {p}: Missing time for solved=True"
                    )

    if not errors:
        print("Scoreboard JSON is valid!")
        return 0
    else:
        print("Errors found:")
        for e in errors:
            print(" -", e)
        return 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python verify_scoreboard.py <Scoreboard.json>")
        sys.exit(1)

    filename = sys.argv[1]
    result = verify_scoreboard(filename)
    sys.exit(result)
