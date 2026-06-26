import pytest
from unittest.mock import patch, MagicMock
from agents.document_analyzer import analyze_energy_bill

def make_mock_field(value: str):
    field = MagicMock()
    field.value_string = value
    field.value_number = None
    field.value_date = None
    field.content = value
    return field

@patch("agents.document_analyzer.summarize_energy_bill")
@patch("agents.document_analyzer.extract_energy_bill")
def test_analyze_energy_bill_success(mock_extract, mock_summarize):
    mock_extract.return_value = {
        "vendor_name": "ENEL SP",
        "customer_name": "Silas Luiz",
        "invoice_date": "2026-06-01",
        "total_amount": "350.00",
        "raw_fields": {}
    }
    mock_summarize.return_value = {
        "summary": "Fatura de energia elétrica analisada com sucesso.",
        "quality_status": "ok",
        "issues": []
    }

    result = analyze_energy_bill(pdf_url="https://example.com/fatura.pdf")

    assert result["status"] == "success"
    assert result["data"]["vendor_name"] == "ENEL SP"
    assert result["data"]["total_amount"] == "350.00"
    assert result["language_analysis"]["quality_status"] == "ok"

@patch("agents.document_analyzer.summarize_energy_bill")
@patch("agents.document_analyzer.extract_energy_bill")
def test_analyze_energy_bill_empty(mock_extract, mock_summarize):
    mock_extract.return_value = {
        "vendor_name": None,
        "customer_name": None,
        "invoice_date": None,
        "total_amount": None,
        "raw_fields": {}
    }
    mock_summarize.return_value = {
        "summary": "Dados insuficientes para análise.",
        "quality_status": "missing_data",
        "issues": ["Campos principais não preenchidos."]
    }

    result = analyze_energy_bill(pdf_url="https://example.com/fatura.pdf")

    assert result["status"] == "success"
    assert result["data"]["vendor_name"] is None
    assert result["language_analysis"]["quality_status"] == "missing_data"
