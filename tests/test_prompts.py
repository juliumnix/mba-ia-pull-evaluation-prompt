"""
Testes automatizados para validação de prompts.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"


def load_prompt() -> dict:
    with PROMPT_PATH.open(encoding="utf-8") as file:
        data = yaml.safe_load(file)
    assert isinstance(data, dict)
    assert PROMPT_KEY in data, f"Chave {PROMPT_KEY} não encontrada no YAML"
    return data[PROMPT_KEY]


def combined_text(prompt: dict) -> str:
    return "\n".join(str(prompt.get(key, "")) for key in ("system_prompt", "user_prompt"))


def test_prompt_has_system_prompt():
    prompt = load_prompt()
    assert prompt.get("system_prompt", "").strip()


def test_prompt_has_role_definition():
    text = combined_text(load_prompt()).lower()
    assert any(
        role in text
        for role in ["você é", "product manager", "agile coach", "persona"]
    )


def test_prompt_mentions_format():
    text = combined_text(load_prompt()).lower()
    assert "user story" in text or "como um" in text
    assert (
        "dado" in text
        or "quando" in text
        or "então" in text
        or "markdown" in text
        or "como um [" in text
        or "como um..., eu quero" in text
    )


def test_prompt_has_few_shot_examples():
    text = combined_text(load_prompt()).lower()
    assert "few-shot" in text or "exemplo 1" in text
    assert text.count("entrada:") >= 2
    assert text.count("saída:") >= 2


def test_prompt_no_todos():
    text = combined_text(load_prompt()).lower()
    assert "[todo]" not in text
    assert "todo:" not in text


def test_minimum_techniques():
    prompt = load_prompt()
    techniques = prompt.get("techniques_applied") or prompt.get("metadata", {}).get("techniques", [])
    assert isinstance(techniques, list)
    assert len(techniques) >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
