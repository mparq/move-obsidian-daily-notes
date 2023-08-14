import subprocess


VAULT_PATH = "/Users/mparq/Documents/notes-personal-2"
CURRENT_GREP_PATTERN = "daily_notes"


def main():
    files_to_rename = list_notes()
    print(files_to_rename)


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


if __name__ == "__main__":
    main()

