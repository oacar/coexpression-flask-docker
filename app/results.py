from app.db import get_db
from flask_restful import Resource


class orf(Resource):
    def get(self, orf_name):
        from app.results import get_result_from_database

        result = get_result_from_database(orf_name)
        if result is None:
            error = "Incorrect orf name or ORF doesn't exists."
            return {"error": error}
        return dict(result)


def get_result_from_database(orf_name):
    db = get_db()
    cur = db.execute("SELECT * FROM orf WHERE orf_name = ?", (orf_name,))
    rv = cur.fetchall()
    cur.close()
    return rv[0] if rv else None
