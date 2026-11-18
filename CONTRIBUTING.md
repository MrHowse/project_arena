# How we work

## The five rules

1. **`main` always works.** Anyone can pull `main` at any time and play.
2. **One job, one branch.** Nobody commits straight to `main`.
3. **Small commits with clear messages.** A message finishes the sentence "This commit will ..."
4. **Nobody merges their own work unreviewed.** One classmate approves first.
5. **Review the code, not the person.** Be specific, be kind, ask questions.

## The loop

Every job, large or small, goes around the same loop.

1. Pick an issue on GitHub and assign it to yourself. No issue for your idea? Write one.
2. Get the latest `main`, then make a branch:

       git switch main
       git pull
       git switch -c enemy/sand-wraith

3. Do the work. Commit each time something new works:

       git status
       git add enemies/sand_wraith.py
       git commit -m "Add Sand Wraith that circles the hero"

4. Check it:

       python3 sandbox.py enemies/sand_wraith.py
       python3 -m unittest

5. Push the branch and open a pull request on GitHub:

       git push -u origin enemy/sand-wraith

6. Ask a classmate to review it. Fix what they find, commit and push again.
7. When it has an approval and a green tick, merge it and delete the branch.
8. Back on your Mac:

       git switch main
       git pull

## Branch names

`kind/short-description`, in lowercase with hyphens.

| Kind | Used for | Example |
|---|---|---|
| `enemy/` `hero/` `weapon/` `pickup/` | A new class | `weapon/trident` |
| `core/` | A change to the engine | `core/pause-screen` |
| `tune/` | A change to `settings.py` | `tune/slower-wave-growth` |
| `fix/` | A bug fix | `fix/archer-stuck-in-corner` |
| `docs/` | Words only | `docs/credits-north-gate` |

## What a reviewer checks

- I pulled the branch and played it. It runs, and it is fun or at least fair.
- The pull request changes only the files it should.
- NAME and AUTHOR are filled in, and the stats fit the budget.
- I can follow the code. If I cannot, I ask. The author must be able to explain every line.
- The tests have a green tick.

## Who can approve what

| Change | Needs an approval from |
|---|---|
| A file in `enemies/`, `heroes/`, `weapons/` or `pickups/` | Any classmate who did not write it |
| `CREDITS.md` and other words | Any classmate who did not write it |
| `settings.py`, `core/`, `tests/`, `main.py`, `sandbox.py` | A maintainer |

## Using AI

AI is your navigator, not your driver. Ask it to explain an error message or a
line of the engine. Do not paste in code you cannot explain: your reviewer will
ask you what each line does, and "the AI wrote it" is not an answer.
