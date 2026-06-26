import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

def get_document_intelligence_client() -> DocumentIntelligenceClient:
    endpoint = os.environ["AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"]
    credential = DefaultAzureCredential()
    return DocumentIntelligenceClient(endpoint=endpoint, credential=credential)

def extract_energy_bill(pdf_url: str = None, pdf_path: str = None) -> dict:
    client = get_document_intelligence_client()

    if pdf_url:
        poller = client.begin_analyze_document(
            "prebuilt-invoice",
            AnalyzeDocumentRequest(url_source=pdf_url)
        )
    elif pdf_path:
        with open(pdf_path, "rb") as f:
            poller = client.begin_analyze_document(
                "prebuilt-invoice",
                f,
                content_type="application/pdf"
            )
    else:
        raise ValueError("Informe pdf_url ou pdf_path")

    result = poller.result()

    extracted = {
        "vendor_name": None,
        "customer_name": None,
        "invoice_date": None,
        "total_amount": None,
        "raw_fields": {}
    }

    if result.documents:
        doc = result.documents[0]
        fields = doc.fields or {}

        extracted["vendor_name"] = _get_field_value(fields, "VendorName")
        extracted["customer_name"] = _get_field_value(fields, "CustomerName")
        extracted["invoice_date"] = _get_field_value(fields, "InvoiceDate")
        extracted["total_amount"] = _get_field_value(fields, "InvoiceTotal")

        extracted["raw_fields"] = {
            key: _get_field_value(fields, key)
            for key in fields
        }

    return extracted

def _get_field_value(fields: dict, key: str):
    field = fields.get(key)
    if not field:
        return None
    if hasattr(field, "value_string"):
        return field.value_string
    if hasattr(field, "value_number"):
        return field.value_number
    if hasattr(field, "value_date"):
        return str(field.value_date)
    if hasattr(field, "content"):
        return field.content
    return None