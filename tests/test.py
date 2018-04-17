
"""Tests for `dublinbikesgroup20` package."""

import sys
sys.path.append(".")
from flaskapp.app.GMAPviews import *

def test_connectDB():
    engine = connectDB()
    conn = engine.connect()
    assert conn != None

def test_scraper_timestamp():
    pass

def test_csv():
    pass

def test_RDS():
    pass