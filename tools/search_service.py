import os
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME", "solar-regulations")


def get_search_index_client() -> SearchIndexClient:
    endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    credential = DefaultAzureCredential()
    return SearchIndexClient(endpoint=endpoint, credential=credential)


def get_search_client() -> SearchClient:
    endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    credential = DefaultAzureCredential()
    return SearchClient(
        endpoint=endpoint,
        index_name=INDEX_NAME,
        credential=credential
    )


def create_index_if_not_exists():
    client = get_search_index_client()
    existing = [idx.name for idx in client.list_indexes()]
    if INDEX_NAME in existing:
        print(f"[SearchService] Índice '{INDEX_NAME}' já existe.")
        return

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SimpleField(name="source", type=SearchFieldDataType.String, filterable=True),
        SimpleField(name="title", type=SearchFieldDataType.String, filterable=True),
    ]

    index = SearchIndex(name=INDEX_NAME, fields=fields)
    client.create_index(index)
    print(f"[SearchService] Índice '{INDEX_NAME}' criado com sucesso.")


def index_documents(documents: list[dict]):
    client = get_search_client()
    result = client.upload_documents(documents=documents)
    print(f"[SearchService] {len(documents)} documentos indexados.")
    return result


def search_regulations(query: str, top: int = 3) -> list[dict]:
    client = get_search_client()
    results = client.search(
        search_text=query,
        top=top,
        select=["id", "title", "content", "source"]
    )
    return [
        {
            "id": r["id"],
            "title": r["title"],
            "content": r["content"],
            "source": r["source"]
        }
        for r in results
    ]


def load_and_index_regulations():
    create_index_if_not_exists()

    regulations_dir = os.path.join(
        os.path.dirname(__file__), "..", "data", "regulations"
    )

    documents = []
    for i, filename in enumerate(os.listdir(regulations_dir)):
        if filename.endswith(".txt"):
            filepath = os.path.join(regulations_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            documents.append({
                "id": str(i + 1),
                "title": filename.replace(".txt", "").replace("_", " ").upper(),
                "content": content,
                "source": filename
            })

    if documents:
        index_documents(documents)
        print(f"[SearchService] {len(documents)} regulações indexadas.")