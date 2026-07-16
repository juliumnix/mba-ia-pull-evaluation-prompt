# Evidência de Avaliação — Aprovado

Execução local de `python src/evaluate.py` com:

- Provider: `openai`
- Modelo principal: `gpt-4o`
- Modelo de avaliação: `gpt-4o`
- Prompt: `juliumnix/bug_to_user_story_v2`
- Dataset: 15 exemplos (`bug-to-user-story-prompt-evaluation-eval`)

## Métricas finais

| Métrica | Score | Status |
|---|---:|---|
| Helpfulness | 0.90 | ✓ |
| Correctness | 0.85 | ✓ |
| F1-Score | 0.83 | ✓ |
| Clarity | 0.92 | ✓ |
| Precision | 0.88 | ✓ |
| Média geral | 0.8776 | ✓ |

**STATUS: APROVADO — Todas as métricas >= 0.8**

## Links

- Prompt público: https://smith.langchain.com/hub/juliumnix/bug_to_user_story_v2
- Projeto (tracing): https://smith.langchain.com/o/83778d5a-f8b4-4c09-93d0-4cbfe72172ad/projects/p/d61be2df-3c16-45fe-b87f-8b6779a760d1
- Dataset (15 exemplos): https://smith.langchain.com/o/83778d5a-f8b4-4c09-93d0-4cbfe72172ad/datasets/085305ac-bc6e-45a0-896a-bcd7eeab7a2e

## Screenshots manuais (recomendado)

Se a entrega pedir imagens, capture no dashboard:

1. Página do prompt público no Hub
2. Projeto com a execução da avaliação
3. Tracing de pelo menos 3 exemplos
4. Terminal com o bloco `STATUS: APROVADO`

Salve as imagens em `docs/screenshots/` (ex.: `01-hub.png`, `02-projeto.png`, `03-tracing.png`, `04-terminal.png`).
