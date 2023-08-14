import subprocess
from typing import List


VAULT_NAME = "notes-personal-2"
VAULT_PATH = "/Users/mparq/Documents/notes-personal-2"
CURRENT_GREP_PATTERN = "daily_notes"
IS_DRY_RUN = True


def main():
    files_to_rename = list_notes()
    to_rename_list = note_str_to_list(files_to_rename)
    obs_move_files(to_rename_list, dry_run=IS_DRY_RUN, obs_vault_name=VAULT_NAME)


def list_notes():
    ls_call = subprocess.Popen(["ls", VAULT_PATH],
                               stdout=subprocess.PIPE)
    grep_call = subprocess.Popen(["grep", CURRENT_GREP_PATTERN],
                               stdin=ls_call.stdout,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    ls_call.stdout.close()
    out, err = grep_call.communicate()
    return out.decode()


def note_str_to_list(notes_str: str) -> List[str]:
    return [line for line in notes_str.split('\n') if line.strip() != '']


def obs_move_files(to_move_list: List[str], dry_run=True, obs_vault_name=None):
    assert obs_vault_name is not None
    # hardcoded file move logic
    for i, to_move in enumerate(to_move_list):
        new_name = update_filename(to_move)
        print(f"[{i+1}/{len(to_move_list)}] {'DRY' if dry_run else ''} obs move {to_move} {new_name} --vault \"{obs_vault_name}\"")
        if not dry_run:
            subprocess.run(["obs", "move", to_move, new_name, "--vault", obs_vault_name])


def update_filename(to_move: str):
    # assumes to_move=YYYYMMDD....md
    year = to_move[:4]
    month = to_move[4:6]
    date = to_move[6:8]
    return f"{year}-{month}-{date}.md"


if __name__ == "__main__":
    main()

