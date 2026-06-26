import json
from tools.document_intelligence import extract_energy_bill

def analyze_energy_bill(pdf_url: str = None, pdf_path: str = None) -> dict:
    print("[DocumentAnalyzer] Iniciando extração da fatura...")

    extracted = extract_energy_bill(pdf_url=pdf_url, pdf_path=pdf_path)

    result = {
        "status": "success",
        "profile": None,
        "data": extracted
    }

    print(f"[DocumentAnalyzer] Extração concluída: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result