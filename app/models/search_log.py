from app.extensions import get_db


class SearchLog:
    @staticmethod
    def record(query):
        query = (query or "").strip()
        if not query:
            return

        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO search_logs (query) VALUES (%s)", (query,))
        conn.commit()

    @staticmethod
    def top_queries(limit=5, hours=12):
        conn = get_db()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT query, COUNT(*) AS search_count
                FROM search_logs
                WHERE searched_at >= NOW() - INTERVAL %s HOUR
                GROUP BY query
                ORDER BY search_count DESC
                LIMIT %s
                """,
                (hours, limit),
            )
            return cursor.fetchall()
