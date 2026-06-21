from pathlib import Path


def escape_renpy(text: str) -> str:
    """
    Escapa caracteres que quebram o Ren'Py:
    - Aspas duplas internas
    - Barras invertidas
    """
    return text.replace('\\', '\\\\').replace('"', '\\"')


def generate_dialogue_rpy(dialogues: dict, translations: dict, language="portuguese"):
    """
    Gera o arquivo dialogue.rpy com blocos de tradução por label.

    dialogues: dict[label] = list of (personagem, texto original)
    translations: dict[text_original] = texto traduzido
    """
    # Cria pasta game/tl/portuguese se não existir
    base_path = Path("game/tl") / language
    base_path.mkdir(parents=True, exist_ok=True)

    output_file = base_path / "dialogue.rpy"

    lines = []
    lines.append("# Arquivo de tradução de diálogos")
    lines.append("# Gerado automaticamente\n")

    for label, items in dialogues.items():
        lines.append(f"translate {language} {label}:")
        lines.append("")

        if not items:
            # Evita erro de parsing no Ren'Py para blocos vazios
            lines.append("    pass")
        else:
            for who, original in items:
                translated = translations.get(original, original)
                translated = escape_renpy(translated)
                lines.append(f'    {who} "{translated}"')

        lines.append("")  # linha em branco entre labels

    output_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ dialogue.rpy gerado em: {output_file}")
    return output_file
