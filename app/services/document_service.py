from app.models.document import Document
from app.models.revision import Revision
from app.services import search_service


def get_document_with_content(slug):
    document = Document.get_by_slug(slug)
    if document is None:
        return None, None
    return document, document.current_revision


def save_new_document(title, slug, content, editor_id):
    document = Document.create(title, slug)
    revision = Revision.create(document.id, content, editor_id, "최초 작성")
    document.set_current_revision(revision.id)
    search_service.index_document(document, revision)
    return document, revision


def save_edit(document, content, editor_id, edit_comment=""):
    revision = Revision.create(document.id, content, editor_id, edit_comment)
    document.set_current_revision(revision.id)
    search_service.index_document(document, revision)
    return revision


def delete_document(document):
    search_service.delete_document(document.id)
    document.delete()


def delete_revision(document, revision_id):
    revisions = Revision.list_by_document(document.id)
    if len(revisions) <= 1:
        raise ValueError("마지막 남은 리비전은 삭제할 수 없습니다.")

    if document.current_revision_id == revision_id:
        new_current = next(r for r in revisions if r.id != revision_id)
        document.set_current_revision(new_current.id)
        Revision.delete(revision_id)
        search_service.index_document(document, new_current)
    else:
        Revision.delete(revision_id)
