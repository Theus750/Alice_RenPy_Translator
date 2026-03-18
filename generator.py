from pathlib import Path


def escape_renpy(text: str) -> str:
    # Escapa barras
    text = text.replace("\\", "\\\\")

    # Remove aspas finais soltas (causam erro fatal no Ren'Py)
    while text.endswith('"'):
        text = text[:-1]

    # Escapa aspas internas
    text = text.replace('"', '\\"')

    return text



def generate_strings_rpy(translations: dict, language="portuguese"):
    base_path = Path("game") / "tl" / language
    base_path.mkdir(parents=True, exist_ok=True)

    output_file = base_path / "strings.rpy"

    seen = set()
    lines = []
    lines.append(f"translate {language} strings:\n")

    for original, translated in translations.items():
        if not original or original in seen:
            continue

        seen.add(original)

        old = escape_renpy(original)
        new = escape_renpy(translated)

        lines.append(f'    old "{old}"')
        lines.append(f'    new "{new}"\n')

    output_file.write_text(
        "\n".join(lines).rstrip() + "\n",
        encoding="utf-8"
    )

    print(f"✅ strings.rpy gerado com sucesso em: {output_file}")
    return output_file
