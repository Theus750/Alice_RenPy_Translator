import re
from typing import List, Tuple


PLACEHOLDER_PATTERN = re.compile(
    r"(\\[nrt]|\[[^\]]+\]|\{[^{}\n]+\}|%\([^)]+\)[a-zA-Z]|%[sd])"
)
TOKEN_TEMPLATE = "RENLOCALIZER_PLACEHOLDER_{index}_TOKEN"
BOUNDARY_PUNCTUATION = ",.!?:;…"


def protect_placeholders(text: str) -> Tuple[str, List[str]]:
    placeholders = PLACEHOLDER_PATTERN.findall(text)
    protected = text
    for index, placeholder in enumerate(placeholders):
        protected = protected.replace(placeholder, TOKEN_TEMPLATE.format(index=index), 1)
    return protected, placeholders


def restore_placeholders(text: str, placeholders: List[str]) -> str:
    restored = text
    for index, placeholder in enumerate(placeholders):
        # O tradutor pode remover/adicionar colchetes do marcador protegido.
        # Uma substituição por variantes literais deixava sobras, por exemplo
        # ``[[heroname]``. Reconhecemos o marcador inteiro de uma só vez.
        token_pattern = re.compile(
            rf"(?:RENLOCALIZER_PLACEHOLDER_{index}_TOKEN|"
            rf"\[{{1,3}}PH_{index}\]{{0,3}}|"
            rf"__PH_{index}(?:__|_)|"
            rf"__VAR_?{index}_?__?|"
            rf"PH_{index})"
        )
        restored = token_pattern.sub(lambda _: placeholder, restored)
    return restored


def placeholders_match(original: str, translated: str) -> bool:
    """Confere se a tradução preservou todos os placeholders do original."""
    return sorted(PLACEHOLDER_PATTERN.findall(original)) == sorted(
        PLACEHOLDER_PATTERN.findall(translated)
    )


def placeholder_spacing_matches(original: str, translated: str) -> bool:
    """Confere se os placeholders mantiveram espaços nas mesmas bordas."""
    original_matches = list(PLACEHOLDER_PATTERN.finditer(original))
    translated_matches = list(PLACEHOLDER_PATTERN.finditer(translated))
    if len(original_matches) != len(translated_matches):
        return False

    for source_match, translated_match in zip(original_matches, translated_matches):
        source_before = source_match.start() > 0 and original[source_match.start() - 1].isspace()
        translated_before = (
            translated_match.start() > 0
            and translated[translated_match.start() - 1].isspace()
        )
        source_after = (
            source_match.end() < len(original)
            and original[source_match.end()].isspace()
        )
        translated_after = (
            translated_match.end() < len(translated)
            and translated[translated_match.end()].isspace()
        )
        source_has_english_possessive = original[source_match.end():].startswith(
            ("'s", "’s")
        )
        if source_has_english_possessive:
            if not translated_after:
                return False
            continue
        source_next = original[source_match.end():]
        if source_next and source_next[0] in BOUNDARY_PUNCTUATION:
            translated_next = translated[translated_match.end():]
            if not translated_next.startswith(source_next[0]):
                return False
            if len(source_next) > 1 and source_next[1].isspace():
                if len(translated_next) < 2 or not translated_next[1].isspace():
                    return False
        if (source_before, source_after) != (translated_before, translated_after):
            return False

    return True


def restore_placeholder_spacing(original: str, translated: str) -> str:
    """Restaura espaços removidos pelo motor nas bordas dos placeholders."""
    restored = translated
    offset = 0
    original_matches = list(PLACEHOLDER_PATTERN.finditer(original))
    for source_match in original_matches:
        placeholder = source_match.group(0)
        translated_match = re.search(re.escape(placeholder), restored[offset:])
        if translated_match is None:
            continue

        start = offset + translated_match.start()
        end = offset + translated_match.end()
        source_before = source_match.start() > 0 and original[source_match.start() - 1].isspace()
        source_after = source_match.end() < len(original) and original[source_match.end()].isspace()

        if source_before and (start == 0 or not restored[start - 1].isspace()):
            restored = restored[:start] + " " + restored[start:]
            start += 1
            end += 1
        if source_after and (end == len(restored) or not restored[end].isspace()):
            restored = restored[:end] + " " + restored[end:]
        elif (
            original[source_match.end():].startswith(("'s", "’s"))
            and end < len(restored)
            and restored[end].isalpha()
            and (end == 0 or not restored[end - 1].isspace())
        ):
            restored = restored[:end] + " " + restored[end:]
            end += 1
        else:
            source_suffix = original[source_match.end():]
            if source_suffix and source_suffix[0] in BOUNDARY_PUNCTUATION:
                translated_suffix = restored[end:]
                suffix_was_normalized = False
                if source_suffix.startswith("…") and translated_suffix.startswith("..."):
                    restored = restored[:end] + "…" + translated_suffix[3:]
                    end += 1
                    translated_suffix = restored[end:]
                    suffix_was_normalized = True
                if not suffix_was_normalized and not translated_suffix.startswith(
                    source_suffix[0]
                ):
                    restored = restored[:end] + source_suffix[0] + restored[end:]
                    end += 1
                    translated_suffix = restored[end:]
                if len(source_suffix) > 1 and source_suffix[1].isspace():
                    if translated_suffix.startswith(source_suffix[0]):
                        if len(translated_suffix) < 2 or not translated_suffix[1].isspace():
                            insertion_point = end + 1
                            restored = (
                                restored[:insertion_point]
                                + " "
                                + restored[insertion_point:]
                            )
                    elif not translated_suffix or not translated_suffix[0].isspace():
                        restored = restored[:end] + " " + restored[end:]
                        end += 1

        offset = end

    for source_match in original_matches:
        source_suffix = original[source_match.end():]
        if source_suffix and source_suffix[0] in BOUNDARY_PUNCTUATION:
            restored = re.sub(
                rf"{re.escape(source_match.group(0))}\s+([{re.escape(BOUNDARY_PUNCTUATION)}])",
                lambda match: f"{source_match.group(0)}{match.group(1)}",
                restored,
                count=1,
            )

    return restored
