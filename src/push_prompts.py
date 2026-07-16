"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)
"""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langsmith import Client

from utils import check_env_vars, load_yaml, print_section_header, validate_prompt_structure

load_dotenv()

PROMPT_FILE = "prompts/bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"


def _resolve_username() -> str | None:
    return os.getenv("USERNAME_LANGSMITH_HUB") or os.getenv("LANGSMITH_PROMPT_OWNER")


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    return validate_prompt_structure(prompt_data)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    username = _resolve_username()
    if not username:
        print("ERRO: USERNAME_LANGSMITH_HUB (ou LANGSMITH_PROMPT_OWNER) nao configurado no .env")
        return False

    # Prefer owner/name when handle exists; fallback to private local name.
    candidates = [f"{username}/{prompt_name}", prompt_name]
    system_template = prompt_data.get("system_prompt", "")
    user_template = prompt_data.get("user_prompt", "{bug_report}")

    if "{bug_report}" not in user_template and "{bug_report}" not in system_template:
        print("ERRO: O prompt deve conter a variavel {bug_report}.")
        return False

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_template),
            ("human", user_template),
        ]
    )

    description = prompt_data.get(
        "description",
        "Prompt otimizado para converter bugs em user stories.",
    )
    tags = prompt_data.get("tags", [])
    techniques = prompt_data.get("techniques_applied", [])
    if techniques:
        tags = list(dict.fromkeys([*tags, *[str(t).lower().replace(" ", "-") for t in techniques]]))

    client = Client()
    last_error = None

    for repo_handle in candidates:
        for is_public in (True, False):
            try:
                url = client.push_prompt(
                    repo_handle,
                    object=prompt,
                    is_public=is_public,
                    description=description,
                    tags=tags,
                )
                visibility = "publico" if is_public else "privado"
                print(f"OK Prompt publicado ({visibility}): {repo_handle}")
                print(f"  URL: {url}")
                if techniques:
                    print(f"  Tecnicas: {', '.join(techniques)}")
                if not is_public:
                    print("  Aviso: publicado como privado. Torne publico no dashboard se necessario.")
                return True
            except TypeError:
                try:
                    url = client.push_prompt(
                        repo_handle,
                        object=prompt,
                        description=description,
                        tags=tags,
                    )
                    print(f"OK Prompt publicado: {repo_handle}")
                    print(f"  URL: {url}")
                    return True
                except Exception as exc:
                    last_error = exc
            except Exception as exc:
                last_error = exc
                continue

    print(f"ERRO ao fazer push do prompt: {last_error}")
    return False


def main() -> int:
    print_section_header("PUSH DE PROMPTS PARA O LANGSMITH")

    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1

    if not _resolve_username():
        print("ERRO: Defina USERNAME_LANGSMITH_HUB no .env")
        return 1

    print(f"Carregando prompt de {PROMPT_FILE}...")
    yaml_data = load_yaml(PROMPT_FILE)
    if not yaml_data:
        return 1

    if PROMPT_KEY not in yaml_data:
        print(f"ERRO: Chave '{PROMPT_KEY}' nao encontrada no YAML.")
        print(f"   Chaves disponiveis: {list(yaml_data.keys())}")
        return 1

    prompt_data = yaml_data[PROMPT_KEY]

    print("Validando estrutura do prompt...")
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("ERRO: Validacao falhou:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("OK Estrutura valida.")

    print(f"Publicando '{PROMPT_KEY}' no LangSmith Hub...")
    success = push_prompt_to_langsmith(PROMPT_KEY, prompt_data)
    if success:
        print("\nProcesso concluído com sucesso.")
        return 0

    print("\nProcesso falhou.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
