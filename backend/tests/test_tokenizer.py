import json
from app.utilts import tokenizer

def test_tokenize_text():
    assert tokenizer.tokenize_text('The café\nsearch-engine is useful.') == ['café', 'search', 'engine', 'useful']

def test_tokenize_docs(tmp_path, monkeypatch):
    source = tmp_path / 'doc.json'
    source.write_text(json.dumps({'id': 'a', 'url': 'https://example.org', 'title': 'Example', 'text': 'A small test'}))
    monkeypatch.setattr(tokenizer, 'DATA_DIR', str(tmp_path / 'tokens'))
    result = tokenizer.tokenize_docs([str(source)])
    assert result[0]['text'] == ['small', 'test']
    assert json.loads((tmp_path / 'tokens/a.json').read_text()) == result[0]
