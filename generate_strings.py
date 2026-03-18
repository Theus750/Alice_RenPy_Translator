from pathlib import Path
import json

CACHE_FILE = Path("cache.json")
TL_DIR = Path("game/tl/portuguese")
TL_DIR.mkdir(parents=True, exist_ok=True)

def load_cache():
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    return {}

def save_strings_rpy(cache):
    strings_file = TL_DIR / "strings.rpy"

    # Usar set pra evitar duplicatas
    written = set()

    with strings_file.open("w", encoding="utf-8") as f:
        f.write("# Auto-gerado pelo tradutor\n\n")
        for original, translated in cache.items():
            if original in written:
                continue
            written.add(original)
            # Escapar aspas
            o = original.replace('"', r'\"')
            t = translated.replace('"', r'\"')
            f.write(f'translate portuguese auto_{hash(original)}:\n')
            f.write(f'    old "{o}"\n')
            f.write(f'    new "{t}"\n\n')

    print(f"Arquivo strings.rpy gerado em: {strings_file}")

# Exemplo de uso
if __name__ == "__main__":
    cache = load_cache()
    save_strings_rpy(cache)
