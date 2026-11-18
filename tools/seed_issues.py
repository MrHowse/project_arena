"""Create the starting labels and issues on GitHub from tools/issues.json.

For the teacher, once, after the repository exists on GitHub. It uses the
GitHub command line tool (gh), which must be installed and signed in.

    python3 tools/seed_issues.py OWNER/REPO            show what would be created
    python3 tools/seed_issues.py OWNER/REPO --go       create it
"""
import json
import pathlib
import subprocess
import sys

DATA = json.loads((pathlib.Path(__file__).parent / "issues.json").read_text())


def run(command, go):
    print(" ".join(command[:6]), "...")
    if go:
        subprocess.run(command, check=True)


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    repo, go = sys.argv[1], "--go" in sys.argv
    for label in DATA["labels"]:
        run(["gh", "label", "create", label["name"], "--repo", repo, "--force",
             "--color", label["color"], "--description", label["description"]], go)
    for issue in DATA["issues"]:
        command = ["gh", "issue", "create", "--repo", repo,
                   "--title", issue["title"], "--body", issue["body"]]
        for label in issue["labels"]:
            command += ["--label", label]
        run(command, go)
    print(f"\n{len(DATA['labels'])} labels and {len(DATA['issues'])} issues",
          "created." if go else "would be created. Add --go to create them.")


if __name__ == "__main__":
    main()
