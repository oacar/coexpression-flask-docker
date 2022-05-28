import os
import sqlite3
import pytest

from app.results import *
from .test_app import app


def test_get_orf_table(app):
    """test get_orf_table function"""
    # with pytest.raises(sqlite3.OperationalError):
    with app.app_context():
        result = get_orf_table("YBR196C-A")
        assert result["orf_id"] == 2
        assert result["orf_sequence"] == "ATG"


def test_get_coexpression_table(app):
    with app.app_context():
        result = get_coexpression_table(1)
        assert result[0]["coexpressed_orf_id"] == 2
