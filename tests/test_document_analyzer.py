import pytest
from unittest.mock import patch, MagicMock
from agents.document_analyzer import analyze_energy_bill


@patch("agents.document_analyzer.analyze_energy_bill_language")
@patch("agents.document_analyzer.extract_energy_bill")
def test_analyze_energy_bill_success(mock_extract, mock_language):
    mock_extract.return_value = {
        "vendor_name": "ENEL SP",
        "customer_name": "Silas Luiz",
        "invoice_date": "2026-06-01",
        "total_amount": "350.00",
        "raw_fields": {}
    }
    mock_language.return_value = {
        "detected_language": "Portuguese",
        "entities": [{"text": "ENEL SP", "category": "Organization", "confidence": 0.95}],
        "quality_status": "ok",
        "issues": []
    }

    result = analyze_energy_bill(pdf_url="https://example.com/fatura.pdf")

    assert result["status"] == "success"
    assert result["data"]["vendor_name"] == "ENEL SP"
    assert result["language_analysis"]["detected_language"] == "Portuguese"
    assert result["language_analysis"]["quality_status"] == "ok"


@patch("agents.document_analyzer.analyze_energy_bill_language")
@patch("agents.document_analyzer.extract_energy_bill")
def test_analyze_energy_bill_missing_data(mock_extract, mock_language):
    mock_extract.return_value = {
        "vendor_name": None,
        "customer_name": None,
        "invoice_date": None,
        "total_amount": None,
        "raw_fields": {}
    }
    mock_language.return_value = {
        "detected_language": None,
        "entities": [],
        "quality_status": "missing_data",
        "issues": ["Nenhum texto disponível para análise de linguagem."]
    }

    result = analyze_energy_bill(pdf_url="https://example.com/fatura.pdf")

    assert result["status"] == "success"
    assert result["language_analysis"]["quality_status"] == "missing_data"
    assert len(result["language_analysis"]["issues"]) > 0