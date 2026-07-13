import importlib
import os
from string import Template
from typing import Optional


class TemplateParser:

    def __init__(
        self,
        language: Optional[str] = None,
        default_language: str = "en"
    ):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.default_language = default_language
        self.language = default_language

        self.set_language(language)

    def set_language(self, language: Optional[str]) -> None:
        if not language:
            self.language = self.default_language
            return

        language_path = os.path.join(
            self.current_path,
            "locales",
            language
        )

        if os.path.isdir(language_path):
            self.language = language
        else:
            self.language = self.default_language

    def get(
        self,
        group: str,
        key: str,
        variables: Optional[dict] = None
    ) -> str:
        if not group:
            raise ValueError("Template group is required.")

        if not key:
            raise ValueError("Template key is required.")

        variables = variables or {}
        selected_language = self.language

        group_path = os.path.join(
            self.current_path,
            "locales",
            selected_language,
            f"{group}.py"
        )

        if not os.path.isfile(group_path):
            selected_language = self.default_language

            group_path = os.path.join(
                self.current_path,
                "locales",
                selected_language,
                f"{group}.py"
            )

        if not os.path.isfile(group_path):
            raise FileNotFoundError(
                f"Template file does not exist: {group_path}"
            )

        module_path = (
            f"stores.LLM.templates.locales."
            f"{selected_language}.{group}"
        )

        module = importlib.import_module(module_path)

        if not hasattr(module, key):
            raise AttributeError(
                f"'{key}' was not found inside {module_path}"
            )

        key_attribute = getattr(module, key)
        if isinstance(key_attribute, Template):
            return key_attribute.substitute(variables)

        if isinstance(key_attribute, str):
            return key_attribute

        if isinstance(key_attribute, list):
            return "\n".join(str(item) for item in key_attribute)

        raise TypeError(
            f"Unsupported template type: "
            f"{type(key_attribute).__name__}"
        )