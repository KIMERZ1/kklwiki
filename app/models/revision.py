from app.extensions import get_db


class Revision:
    def __init__(self, id, document_id, content, editor_id, edit_comment, created_at=None):
        self.id = id
        self.document_id = document_id
        self.content = content
        self.editor_id = editor_id
        self.edit_comment = edit_comment
        self.created_at = created_at

    @staticmethod
    def _from_row(row):
        if row is None:
            return None
        return Revision(**row)

    @staticmethod
    def get_by_id(revision_id):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM revisions WHERE id = %s", (revision_id,))
            row = cursor.fetchone()
        return Revision._from_row(row)

    @staticmethod
    def list_by_document(document_id):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM revisions WHERE document_id = %s ORDER BY created_at DESC",
                (document_id,),
            )
            rows = cursor.fetchall()
        return [Revision._from_row(row) for row in rows]

    @staticmethod
    def delete(revision_id):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM revisions WHERE id = %s", (revision_id,))
        conn.commit()

    @staticmethod
    def create(document_id, content, editor_id, edit_comment=""):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO revisions (document_id, content, editor_id, edit_comment) VALUES (%s, %s, %s, %s)",
                (document_id, content, editor_id, edit_comment),
            )
            new_id = cursor.lastrowid
        conn.commit()
        return Revision.get_by_id(new_id)
