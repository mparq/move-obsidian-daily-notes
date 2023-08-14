import subprocess
from typing import List


VAULT_PATH = "/Users/mparq/Documents/notes-personal-2"
CURRENT_GREP_PATTERN = "daily_notes"


def main():
    files_to_rename = list_notes()
    to_rename_list = note_str_to_list(files_to_rename)
    obs_move_files(to_rename_list)


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


def obs_move_files(to_move_list: List[str], dry_run=True):
    # hardcoded file move logic
    for to_move in to_move_list:
        new_name = update_filename(to_move)
        if dry_run:
            print(f"DRY mv {to_move} {new_name}")


def update_filename(to_move: str):
    # assumes to_move=YYYYMMDD....md
    year = to_move[:4]
    month = to_move[4:6]
    date = to_move[6:8]
    return f"{year}-{month}-{date}.md"


if __name__ == "__main__":
    main()

