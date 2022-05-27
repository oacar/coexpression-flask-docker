from app.db import get_db
from flask_restful import Resource


class orf(Resource):
    def get(self, orf_name):
        print(orf_name)
        result = get_orf_table(orf_name)
        if result is None:
            error = "Incorrect orf name or ORF doesn't exists."
            return {"error": error}
        orf_id = result["orf_id"]
        # coexpression = get_coexpression_table(orf_id)
        # network_prop = get_coexpression_network_properties(orf_id)
        # cluster_id = network_prop["cluster_id"]
        # cluster = get_cluster_table(cluster_id)
        # data = []
        # for row in coexpression:
        #     data.append(row["coexpressed_orf_id"])
        return orf_id


def get_orf_table(orf_name):
    db = get_db()
    cur = db.execute("SELECT * FROM orf WHERE orf_name = ?", (orf_name,))
    rv = cur.fetchall()
    cur.close()
    return rv[0] if rv else None


def get_coexpression_table(orf_id):
    db = get_db()
    cur = db.execute("SELECT * FROM coexpression WHERE orf_id = ?", (orf_id,))
    rv = cur.fetchall()
    cur.close()
    return rv if rv else None


def get_coexpression_network_properties(orf_id):
    db = get_db()
    cur = db.execute("SELECT * FROM coexpression_network WHERE orf_id = ?", (orf_id,))
    rv = cur.fetchall()
    cur.close()
    return rv[0] if rv else None


def get_cluster_table(cluster_id):
    db = get_db()
    cur = db.execute(
        "SELECT * FROM coexpression_cluster WHERE cluster_id = ?", (cluster_id,)
    )
    rv = cur.fetchall()
    cur.close()
    return rv[0] if rv else None


def get_cluster_go(cluster_id):
    db = get_db()
    cur = db.execute("SELECT * FROM gene_ontology WHERE cluster_id = ?", (cluster_id,))
    rv = cur.fetchall()
    cur.close()
    return rv[0] if rv else None
