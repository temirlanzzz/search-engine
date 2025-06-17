import pytest
from app.utilts.tokenizer import tokenize_text
def test_tokenize_text():
    text = "Hello, world! This is a test sentence. Runinng should be run"
    expected = ["hello", "world", "test", "sentenc", "runinng", "run"]
    result = tokenize_text(text)
    assert result == expected
