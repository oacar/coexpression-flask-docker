import os
import sqlite3
import tempfile

import pytest

from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_orf_not_exists(client):
    """test there is no orf table in empty db"""

    # with pytest.raises(sqlite3.OperationalError):
    rv = client.get("/orf_name/foo")
    assert rv.get_json() == {"error": "Incorrect orf name or ORF doesn't exists."}


def test_orf_exists(client):
    """test successful orf lookup"""

    # with pytest.raises(sqlite3.OperationalError):
    rv = client.get("/orf_name/YBR196C-A")
    assert "2" in rv.text


def test_database_exists(app):
    """test database exists"""

    assert os.path.exists(app.config["DATABASE"])
