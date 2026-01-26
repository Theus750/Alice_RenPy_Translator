from pathlib import Path


def escape_renpy(text: str) -> str:
    return (
        text
        .replace("\\", "\\\\")
        .replace('"', '\\"')
    )


def generate_strings_rpy(translations: dict, language="portuguese"):
    base_path = Path("game") / "tl" / language
    base_path.mkdir(parents=True, exist_ok=True)

    output_file = base_path / "strings.rpy"

    lines = []
    lines.append(f"translate {language} strings:\n")

    seen = set()  # 👈 evita duplicatas

    for original, translated in translations.items():
        original = original.strip()
        translated = translated.strip()

        if not original:
            continue

        if original in seen:
            continue  # 👈 ignora repetido

        seen.add(original)

        old = escape_renpy(original)
        new = escape_renpy(translated)

        lines.append(f'    old "{old}"')
        lines.append(f'    new "{new}"\n')

    output_file.write_text("\n".join(lines), encoding="utf-8")

    return output_file
