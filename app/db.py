import sqlite3
import csv
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


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("create-test-db")
@with_appcontext
def create_test_data():
    """Create test database."""
    init_db()
    con = get_db()
    push_orf_table(con, "tests/data/orf.csv")
    con.commit()
    push_coexpression_table(con, "tests/data/coexpression.csv")
    con.commit()
    push_coexpression_network_table(con, "tests/data/coexpression_network.csv")
    con.commit()
    con.close()


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
    app.cli.add_command(create_test_data)


@click.command("push-test-data")
@click.argument("csv_file")
@click.argument("table_name")
@with_appcontext
def push_csv_to_sqlite(csv_file, table_name):

    con = (
        get_db()
    )  # sqlite3.connect(":memory:") # change to 'sqlite:///your_filename.db'
    if table_name == "orf":
        push_orf_table(con, csv_file)
    elif table_name == "coexpression":
        push_coexpression_table(con, csv_file)
    elif table_name == "coexpression_network":
        push_coexpression_network_table(con, csv_file)
    elif table_name == "coexpression_cluster":
        push_coexpression_cluster_table(con, csv_file)
    elif table_name == "gene_ontology":
        push_gene_ontology_table(con, csv_file)
    else:
        print("Table not found")
    con.commit()
    con.close()
    click.echo(f"Pushed {csv_file} to sqlite3 database.")


def push_orf_table(con, csv_file):
    cur = con.cursor()

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


def push_coexpression_table(con, csv_file):
    cur = con.cursor()

    with open(csv_file, "r") as fin:  # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # comma is default delimiter
        to_db = [
            (
                i["orf_id"],
                i["coexpressed_orf_id"],
                i["rho"],
                i["pairwise_observations"],
                i["pearson_r"],
                i["spearman_r"],
                i["coexpression_id"],
            )
            for i in dr
        ]
    cur.executemany(
        """INSERT INTO coexpression ( "orf_id",
  "coexpressed_orf_id",
  "rho",
  "pairwise_observations",
  "pearson_r",
  "spearman_r",
  "coexpression_id") VALUES (?, ?,?, ?,?, ?,?);""",
        to_db,
    )


def push_coexpression_network_table(con, csv_file):
    cur = con.cursor()

    with open(csv_file, "r") as fin:  # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # comma is default delimiter
        to_db = [
            (
                i["orf_id"],
                i["cluster_id"],
                i["degree"],
            )
            for i in dr
        ]
    cur.executemany(
        """INSERT INTO coexpression_network ( "orf_id",
  "cluster_id",
  "degree" ) VALUES (?, ?,?);""",
        to_db,
    )


def push_gene_ontology_table(con, csv_file):
    cur = con.cursor()

    with open(csv_file, "r") as fin:  # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # comma is default delimiter
        to_db = [
            (
                i["gene_ontology_table_id"],
                i["go_name"],
                i["go_id"],
                i["go_definition"],
                i["study_count"],
                i["study_ratio"],
                i["population_count"],
                i["population_ratio"],
                i["cluster_id"],
                i["study_orfs_id"],
            )
            for i in dr
        ]
    cur.executemany(
        """INSERT INTO gene_ontology ( "gene_ontology_table_id",
  "go_name",
  "go_id",
  "go_definition",
  "study_count",
  "study_ratio",
  "population_count",
  "population_ratio",
  "cluster_id",
  "study_orfs_id") VALUES (?, ?,?, ?,?, ?,?, ?,?, ?);""",
        to_db,
    )


def push_coexpression_cluster_table(con, csv_file):
    cur = con.cursor()

    with open(csv_file, "r") as fin:  # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin)  # comma is default delimiter
        to_db = [
            (
                i["cluster_id"],
                i["cluster_name"],
                i["cluster_size"],
                i["transient_ratio"],
                i["conserved_ratio"],
                i["nei_ratio"],
                i["transient_count"],
                i["conserved_count"],
                i["nei_count"],
                i["bp_count"],
                i["cc_count"],
                i["mf_count"],
                i["tf_count"],
            )
            for i in dr
        ]
    cur.executemany(
        """INSERT INTO coexpression_cluster ( "cluster_id",
  "cluster_name",
  "cluster_size",
  "transient_ratio",
  "conserved_ratio",
  "nei_ratio",
  "transient_count",
  "conserved_count",
  "nei_count",
  "bp_count",
  "cc_count",
  "mf_count",
  "tf_count") VALUES (?, ?,?, ?,?, ?,?, ?,?, ?,?, ?,?);""",
        to_db,
    )
