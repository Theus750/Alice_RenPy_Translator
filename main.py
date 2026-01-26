from extractor import extract_from_folder
from translator import translate_text, load_cache, save_cache
from generator import generate_strings_rpy


texts = extract_from_folder("game")
cache = load_cache()

total = len(texts)
done = len(cache)

print(f"{total} textos encontrados")
print(f"{done} já traduzidos (cache)\n")

MAX_PER_RUN = 20
count = 0

for text in texts:
    if text in cache:
        continue  # já foi, não toca

    current = len(cache) + 1
    print(f"[{current}/{total}] Traduzindo: {text}")

    try:
        pt = translate_text(text, cache=cache)
        print(" ->", pt)
        count += 1
    except Exception as e:
        print(" ERRO:", e)
        break  # para no 429, sem insistir

    if count >= MAX_PER_RUN:
        print("\n⏸ Limite desta execução atingido.")
        break

save_cache(cache)

print(f"\n✅ Progresso atual: {len(cache)}/{total}")
