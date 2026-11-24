from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class TranslationSettings:
    selected_engine: str = "libretranslate"
    api_url: str = "http://localhost:5000/translate"
    source_language: str = "en"
    target_language: str = "pt-BR"
    max_batch_size: int = 100
    max_retries: int = 3
    timeout: int = 60
    enable_runtime_hook: bool = True


@dataclass
class ProjectSettings:
    project_path: str = ""
    extracted_entries_path: str = "extracted_entries.json"
    cache_path: str = "cache.json"
    dialogue_output_path: str = ""
    strings_output_path: str = ""


@dataclass
class UISettings:
    theme: str = "system"
    locale: str = "pt-BR"
    last_opened_project: str = ""


@dataclass
class AppConfig:
    project: ProjectSettings = field(default_factory=ProjectSettings)
    translation: TranslationSettings = field(default_factory=TranslationSettings)
    ui: UISettings = field(default_factory=UISettings)

    def to_dict(self) -> dict[str, dict[str, Any]]:
        return {
            "project": asdict(self.project),
            "translation": asdict(self.translation),
            "ui": asdict(self.ui),
        }


class ConfigManager:
    def __init__(self, config_path: str | Path = "config.json") -> None:
        self.config_path = Path(config_path)

    def load(self) -> AppConfig:
        if not self.config_path.exists():
            return AppConfig()

        data = json.loads(self.config_path.read_text(encoding="utf-8"))
        return self._from_dict(data)

    def save(self, config: AppConfig) -> Path:
        self._validate(config)
        self.config_path.write_text(json.dumps(config.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return self.config_path

    def sections(self) -> dict[str, dict[str, Any]]:
        config = self.load()
        return config.to_dict()

    def update_section(self, section_name: str, values: dict[str, Any]) -> AppConfig:
        config = self.load()
        target = self._section_object(config, section_name)
        if target is None:
            raise KeyError(f"Unknown config section: {section_name}")

        for key, value in values.items():
            if hasattr(target, key):
                setattr(target, key, value)

        self.save(config)
        return config

    def load_ui_texts(self, locale: str | None = None) -> dict[str, Any]:
        locale_name = locale or self.load().ui.locale
        locales_dir = self.config_path.parent / "locales"
        locale_file = locales_dir / f"{locale_name}.json"
        if not locale_file.exists():
            return {}
        return json.loads(locale_file.read_text(encoding="utf-8"))

    def load_glossary(self, glossary_path: str | Path | None = None) -> dict[str, str]:
        path = Path(glossary_path) if glossary_path is not None else self.config_path.parent / "glossary.json"
        if not path.exists():
            return {}
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return {str(key): str(value) for key, value in data.items()}
        return {}

    def save_glossary(self, glossary: dict[str, str], glossary_path: str | Path | None = None) -> Path:
        path = Path(glossary_path) if glossary_path is not None else self.config_path.parent / "glossary.json"
        path.write_text(
            json.dumps(glossary, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return path

    def _from_dict(self, data: dict[str, Any]) -> AppConfig:
        project_data = self._section(data, "project", ["project_path", "extracted_entries_path", "cache_path", "dialogue_output_path", "strings_output_path"])
        translation_data = self._section(data, "translation", ["selected_engine", "api_url", "source_language", "target_language", "max_batch_size", "max_retries", "timeout", "enable_runtime_hook"])
        ui_data = self._section(data, "ui", ["theme", "locale", "last_opened_project"])

        return AppConfig(
            project=ProjectSettings(**project_data),
            translation=TranslationSettings(**translation_data),
            ui=UISettings(**ui_data),
        )

    def _section(self, data: dict[str, Any], section_name: str, fallback_keys: list[str]) -> dict[str, Any]:
        section = data.get(section_name, {}) if isinstance(data, dict) else {}
        if not isinstance(section, dict):
            section = {}

        values = {key: section.get(key) for key in fallback_keys if key in section}

        for key in fallback_keys:
            if key in values:
                continue
            if isinstance(data, dict) and key in data:
                values[key] = data[key]

        defaults = asdict(self._default_section(section_name))
        defaults.update({key: value for key, value in values.items() if value is not None})
        return defaults

    def _default_section(self, section_name: str) -> Any:
        if section_name == "project":
            return ProjectSettings()
        if section_name == "translation":
            return TranslationSettings()
        return UISettings()

    def _section_object(self, config: AppConfig, section_name: str) -> Any | None:
        if section_name == "project":
            return config.project
        if section_name == "translation":
            return config.translation
        if section_name == "ui":
            return config.ui
        return None

    def _validate(self, config: AppConfig) -> None:
        if config.translation.max_batch_size < 1:
            raise ValueError("max_batch_size must be greater than zero")
        if config.translation.max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        if config.translation.timeout < 1:
            raise ValueError("timeout must be greater than zero")
