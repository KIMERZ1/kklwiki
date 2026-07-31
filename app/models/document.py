from app.extensions import get_db


class Document:
    def __init__(self, id, title, slug, current_revision_id, created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.slug = slug
        self.current_revision_id = current_revision_id
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        return Document(**row)

    @staticmethod
    def get_by_id(document_id):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM documents WHERE id = %s", (document_id,))
            row = cursor.fetchone()
        return Document._from_row(row)

    @staticmethod
    def get_by_slug(slug):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM documents WHERE slug = %s", (slug,))
            row = cursor.fetchone()
        return Document._from_row(row)

    @staticmethod
    def search_by_title(query, limit=8):
        conn = get_db()
        like = f"%{query}%"
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT slug, title FROM documents WHERE title LIKE %s OR slug LIKE %s ORDER BY title LIMIT %s",
                (like, like, limit),
            )
            return cursor.fetchall()

    @staticmethod
    def create(title, slug):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO documents (title, slug) VALUES (%s, %s)",
                (title, slug),
            )
            new_id = cursor.lastrowid
        conn.commit()
        return Document.get_by_id(new_id)

    def set_current_revision(self, revision_id):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE documents SET current_revision_id = %s WHERE id = %s",
                (revision_id, self.id),
            )
        conn.commit()
        self.current_revision_id = revision_id

    def delete(self):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE documents SET current_revision_id = NULL WHERE id = %s", (self.id,))
            cursor.execute("DELETE FROM page_views WHERE document_id = %s", (self.id,))
            cursor.execute("DELETE FROM revisions WHERE document_id = %s", (self.id,))
            cursor.execute("DELETE FROM documents WHERE id = %s", (self.id,))
        conn.commit()

    @property
    def current_revision(self):
        from app.models.revision import Revision

        if self.current_revision_id is None:
            return None
        return Revision.get_by_id(self.current_revision_id)
