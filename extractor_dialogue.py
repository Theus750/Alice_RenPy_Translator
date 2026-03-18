import re
from pathlib import Path

LABEL_PATTERN = re.compile(r'^label\s+(\w+):')
DIALOGUE_PATTERN = re.compile(r'^\s*(\w+)\s+"(.+)"')

def extract_dialogues(game_path: str):
    dialogues = {}
    current_label = None

    for file in Path(game_path).rglob("*.rpy"):
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                label_match = LABEL_PATTERN.match(line)
                if label_match:
                    current_label = label_match.group(1)
                    dialogues.setdefault(current_label, [])
                    continue

                if current_label:
                    dlg = DIALOGUE_PATTERN.match(line)
                    if dlg:
                        who, text = dlg.groups()
                        dialogues[current_label].append((who, text))

    return dialogues
