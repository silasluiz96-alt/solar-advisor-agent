import json
import os

import openai
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")


def _configure_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não configurado. Configure a variável de ambiente para usar o Language Service.")

    openai.api_key = api_key
    return DEFAULT_MODEL


def _build_prompt(extracted: dict) -> str:
    return (
        "Você é um assistente que recebe dados extraídos de uma fatura de energia elétrica. "
        "Gere uma resposta no formato JSON com os campos: summary, quality_status e issues. "
        "O campo summary deve conter um breve resumo em português. "
        "O campo quality_status deve ser 'ok', 'warning' ou 'missing_data'. "
        "O campo issues deve ser uma lista de strings indicando problemas ou dados ausentes. "
        "Use estas informações de fatura: \n" + json.dumps(extracted, ensure_ascii=False, indent=2)
    )


def summarize_energy_bill(extracted: dict) -> dict:
    model = _configure_openai()
    prompt = _build_prompt(extracted)

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "Você é um assistente técnico que ajuda a analisar faturas de energia."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=400,
    )

    text = response.choices[0].message.content.strip()

    try:
        payload = json.loads(text)
        return payload
    except json.JSONDecodeError:
        return {
            "summary": text,
            "quality_status": "warning",
            "issues": [
                "Resposta do modelo não pôde ser convertida em JSON. Verifique o conteúdo retornado.",
            ],
        }
