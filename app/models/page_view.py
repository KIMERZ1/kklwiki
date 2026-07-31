from app.extensions import get_db


class PageView:
    @staticmethod
    def record(document_id):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO page_views (document_id) VALUES (%s)", (document_id,))
        conn.commit()

    @staticmethod
    def top_documents(limit=5, days=30):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT d.id, d.title, d.slug, COUNT(pv.id) AS view_count
                FROM page_views pv
                JOIN documents d ON d.id = pv.document_id
                WHERE pv.viewed_at >= NOW() - INTERVAL %s DAY
                GROUP BY d.id, d.title, d.slug
                ORDER BY view_count DESC
                LIMIT %s
                """,
                (days, limit),
            )
            return cursor.fetchall()
