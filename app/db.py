import sqlite3
import pandas as pd

import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import table


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        print(current_app.config["DATABASE"])
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def import_test_csvs(tablename, db):
    with current_app.open_resource("test_data/" + tablename + ".csv") as f:
        df = pd.read_csv(f)
        df.to_sql(tablename, db, if_exists="replace", index=False)


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
    # for tablename in [
    #     "orf",
    #     "coexpression",
    #     "coexpression_network",
    #     "coexpression_cluster",
    #     "gene_ontology",
    # ]:
    #     import_test_csvs(tablename, db)


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(push_csv_to_sqlite)


@click.command("push-test-data")
@click.argument("csv_file")
@with_appcontext
def push_csv_to_sqlite(csv_file):
    import csv, sqlite3

    con = (
        get_db()
    )  # sqlite3.connect(":memory:") # change to 'sqlite:///your_filename.db'
    cur = con.cursor()
    #    cur.execute("CREATE TABLE t (col1, col2);") # use your column names here

    with open(csv_file, "r") as fin:  # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # comma is default delimiter

        to_db = [
            (
                i["orf_id"],
                i["orf_name"],
                i["orf_sequence"],
                i["orf_start"],
                i["orf_end"],
                i["orf_strand"],
                i["orf_length"],
                i["orf_gc_content"],
                i["orf_riboseq_qvalue"],
                i["orf_riboseq_reads"],
                i["orf_upstream_neighbor"],
                i["orf_downstream_neighbor"],
                i["orf_upstream_neighbor_distance"],
                i["orf_downstream_neighbor_distance"],
                i["orf_upstream_neighbor_strand"],
                i["orf_downstream_neighbor_strand"],
                i["orf_upstream_neighbor_length"],
                i["orf_downstream_neighbor_length"],
            )
            for i in dr
        ]

    cur.executemany(
        """INSERT INTO orf ( "orf_id",
  "orf_name",
  "orf_sequence",
  "orf_start",
  "orf_end",
  "orf_strand",
  "orf_length",
  "orf_gc_content",
  "orf_riboseq_qvalue",
  "orf_riboseq_reads",
  "orf_upstream_neighbor",
  "orf_downstream_neighbor",
  "orf_upstream_neighbor_distance",
  "orf_downstream_neighbor_distance",
  "orf_upstream_neighbor_strand",
  "orf_downstream_neighbor_strand",
  "orf_upstream_neighbor_length",
  "orf_downstream_neighbor_length") VALUES (?, ?,?, ?,?, ?,?, ?,?, ?,?, ?,?, ?,?, ?,?, ?);""",
        to_db,
    )
    con.commit()
    con.close()
    click.echo(f"Pushed {csv_file} to sqlite3 database.")
