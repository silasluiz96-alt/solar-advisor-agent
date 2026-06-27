import pytest
from unittest.mock import patch, MagicMock
from tools.search_service import search_regulations, create_index_if_not_exists


@patch("tools.search_service.get_search_client")
def test_search_regulations_returns_results(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client

    mock_client.search.return_value = [
        {
            "id": "1",
            "title": "RN482 RESUMO",
            "content": "Microgeração distribuída permite compensação de energia.",
            "source": "rn482_resumo.txt"
        }
    ]

    results = search_regulations("microgeração solar")

    assert len(results) == 1
    assert results[0]["title"] == "RN482 RESUMO"
    assert "compensação" in results[0]["content"]


@patch("tools.search_service.get_search_client")
def test_search_regulations_empty(mock_get_client):
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.search.return_value = []

    results = search_regulations("termo inexistente")

    assert results == []