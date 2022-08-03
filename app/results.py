from unittest import result
from flask import jsonify
from app.db import get_db
from flask_restful import Resource


class Results(Resource):
    def get(self):
        result = get_orf_table(None)
        return jsonify(result)


class orf(Resource):
    def get(self, orf_name):
        print(orf_name)
        orf_properties = get_orf_table(orf_name)
        orf_id = orf_properties[orf_name]["orf_id"]
        # coexpression = get_coexpression_table(orf_id)
        # if orf_properties is None:
        #     error = "Incorrect orf name or ORF doesn't exists."
        #     return {"error": error}
        # elif coexpression is None:
        #     error = "No coexpression data found."
        #     return {"error": error}
        # network_prop = get_coexpression_network_properties(orf_id)
        # cluster_id = network_prop["cluster_id"]
        # cluster = get_cluster_table(cluster_id)
        # data = []
        # for row in coexpression:
        #     data.append(row["coexpressed_orf_id"])
        print(list(orf_properties))
        return {
            "orf_id": orf_id,
            "orf_properties": (orf_properties[orf_name]),
        }


def sql_to_json(cur, idx_name="orf_id"):
    rv = cur.fetchall()
    row_headers = [x[0] for x in cur.description]  # this will extract row headers
    mydict = {}
    for row in rv:
        mydict[row[idx_name]] = dict(zip(row_headers, row))
    cur.close()

    return mydict


def get_orf_table(orf_name):
    db = get_db()
    if orf_name is None:
        cur = db.execute("SELECT * FROM orf")
    else:
        cur = db.execute("SELECT * FROM orf WHERE orf_name = ?", (orf_name,))
    result = sql_to_json(cur, idx_name="orf_name")
    return result


def get_coexpression_table(orf_id):
    db = get_db()
    cur = db.execute("SELECT * FROM coexpression WHERE orf_id = ?", (orf_id,))
    result = sql_to_json(cur)
    return result  # if rv else None


def get_coexpression_network_properties(orf_id):
    db = get_db()
    cur = db.execute("SELECT * FROM coexpression_network WHERE orf_id = ?", (orf_id,))
    result = sql_to_json(cur)
    return result


def get_cluster_table(cluster_id):
    db = get_db()
    cur = db.execute(
        "SELECT * FROM coexpression_cluster WHERE cluster_id = ?", (cluster_id,)
    )
    result = sql_to_json(cur, idx_name="cluster_id")
    return result


def get_cluster_go(cluster_id):
    db = get_db()
    cur = db.execute("SELECT * FROM gene_ontology WHERE cluster_id = ?", (cluster_id,))
    result = sql_to_json(cur, idx_name="cluster_id")
    return result
