# Unit tests for file parsing
import pytest
from app.services.file_parser import FileParser

def test_parse_csv():
    df = FileParser.parse_file("data/sample.csv")
    assert not df.empty
