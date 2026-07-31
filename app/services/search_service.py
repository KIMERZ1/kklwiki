from elasticsearch import NotFoundError

from app import extensions
from app.services.markup_service import to_plain_text

INDEX_NAME = "wiki_pages"


def index_document(document, revision):
    extensions.es.index(
        index=INDEX_NAME,
        id=document.id,
        document={
            "page_id": document.id,
            "title": document.title,
            "slug": document.slug,
            "content": to_plain_text(revision.content),
            "updated_at": document.updated_at.isoformat() if document.updated_at else None,
        },
    )


def delete_document(document_id):
    try:
        extensions.es.delete(index=INDEX_NAME, id=document_id)
    except NotFoundError:
        pass


def search(query, size=20):
    if not query:
        return []
    result = extensions.es.search(
        index=INDEX_NAME,
        query={"multi_match": {"query": query, "fields": ["title^3", "content"]}},
        highlight={"fields": {"content": {}}},
        size=size,
    )
    return result["hits"]["hits"]
