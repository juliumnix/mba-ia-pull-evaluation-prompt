"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull do prompt leonanluppi/bug_to_user_story_v1
3. Salva localmente em prompts/bug_to_user_story_v1.yml
"""

from __future__ import annotations

import sys
from datetime import date

from dotenv import load_dotenv
from langchain import hub

from utils import check_env_vars, print_section_header, save_yaml

load_dotenv()

PROMPT_REF = "leonanluppi/bug_to_user_story_v1"
OUTPUT_PATH = "prompts/bug_to_user_story_v1.yml"
PROMPT_KEY = "bug_to_user_story_v1"


def _extract_templates(prompt) -> tuple[str, str]:
    system_prompt = ""
    user_prompt = "{bug_report}"

    messages = getattr(prompt, "messages", None) or []
    for message in messages:
        inner = getattr(message, "prompt", message)
        template = getattr(inner, "template", None) or getattr(message, "content", None) or ""
        role = (
            getattr(message, "role", None)
            or getattr(message, "type", None)
            or message.__class__.__name__.replace("MessagePromptTemplate", "").lower()
        )
        role = str(role).lower()

        if "system" in role and not system_prompt:
            system_prompt = str(template)
        if ("human" in role or "user" in role) and template:
            user_prompt = str(template)

    if not system_prompt and hasattr(prompt, "template"):
        system_prompt = str(prompt.template)

    return system_prompt.strip(), user_prompt.strip() or "{bug_report}"


def pull_prompts_from_langsmith() -> bool:
    print(f"Puxando prompt do LangSmith Hub: {PROMPT_REF}")
    try:
        prompt = hub.pull(PROMPT_REF)
        system_prompt, user_prompt = _extract_templates(prompt)

        prompt_data = {
            PROMPT_KEY: {
                "description": "Prompt para converter relatos de bugs em User Stories",
                "system_prompt": system_prompt
                or "Você transforma bugs em user stories.",
                "user_prompt": user_prompt,
                "version": "v1",
                "created_at": date.today().isoformat(),
                "tags": ["bug-analysis", "user-story", "product-management"],
                "metadata": {
                    "source": PROMPT_REF,
                    "quality": "low",
                },
            }
        }

        if save_yaml(prompt_data, OUTPUT_PATH):
            print(f"✓ Prompt salvo em {OUTPUT_PATH}")
            return True

        print(f"❌ Falha ao salvar {OUTPUT_PATH}")
        return False
    except Exception as exc:
        print(f"❌ Erro ao fazer pull do prompt: {exc}")
        return False


def main() -> int:
    print_section_header("PULL DE PROMPTS DO LANGSMITH")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    return 0 if pull_prompts_from_langsmith() else 1


if __name__ == "__main__":
    sys.exit(main())
