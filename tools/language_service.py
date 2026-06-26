import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


def get_language_client() -> TextAnalyticsClient:
    endpoint = os.environ["AZURE_AI_SERVICES_ENDPOINT"]
    credential = DefaultAzureCredential()
    return TextAnalyticsClient(endpoint=endpoint, credential=credential)


def analyze_energy_bill_language(extracted: dict) -> dict:
    client = get_language_client()

    texts_to_analyze = []

    if extracted.get("vendor_name"):
        texts_to_analyze.append(extracted["vendor_name"])
    if extracted.get("customer_name"):
        texts_to_analyze.append(extracted["customer_name"])

    result = {
        "detected_language": None,
        "entities": [],
        "quality_status": "ok",
        "issues": []
    }

    if not texts_to_analyze:
        result["quality_status"] = "missing_data"
        result["issues"].append("Nenhum texto disponível para análise de linguagem.")
        return result

    # detect_language
    language_response = client.detect_language(documents=texts_to_analyze)
    for doc in language_response:
        if not doc.is_error:
            result["detected_language"] = doc.primary_language.name
            break

    # recognize_entities
    entity_response = client.recognize_entities(documents=texts_to_analyze)
    for doc in entity_response:
        if not doc.is_error:
            for entity in doc.entities:
                result["entities"].append({
                    "text": entity.text,
                    "category": entity.category,
                    "confidence": round(entity.confidence_score, 2)
                })

    if not result["detected_language"]:
        result["quality_status"] = "warning"
        result["issues"].append("Idioma não detectado.")

    return result