import json
import os

from elasticsearch import Elasticsearch

ES_HOST = os.environ.get("ES_HOST", "http://localhost:9200")
INDEX_NAME = "wiki_pages"
MAPPING_FILE = os.path.join(os.path.dirname(__file__), "..", "wiki_pages.json")


def main():
    es = Elasticsearch(ES_HOST)

    if es.indices.exists(index=INDEX_NAME):
        print(f"'{INDEX_NAME}' 인덱스가 이미 존재합니다.")
        return

    with open(MAPPING_FILE, encoding="utf-8") as f:
        mapping = json.load(f)

    es.indices.create(index=INDEX_NAME, mappings=mapping["mappings"])
    print(f"'{INDEX_NAME}' 인덱스 생성 완료")


if __name__ == "__main__":
    main()
