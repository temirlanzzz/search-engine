from app.utilts.tokenizer import tokenize_text, tokenize_docs
def test_tokenize_text():
    text = "Hello, world! This is a test sentence. Runinng should be run"
    expected = ["hello", "world", "test", "sentenc", "runinng", "run"]
    result = tokenize_text(text)
    assert result == expected

def test_tokenize_docs():
    list_of_docs = ['../../../data/docs/0.json', '../../../data/docs/1.json', '../../../data/docs/2.json']
    tokens = tokenize_docs(list_of_docs)
    assert len(tokens) == 3
    assert tokens[1]['id'] == 1
    assert tokens[1]['url'] == 'https://web-scraping.dev/blocked'
    assert tokens[1]['title'] == 'web-scraping.dev - You\'ve been blocked'
    assert tokens[1]['text'] == ["webscrapingdev","","youv","block","webscrapingdev","youv","block","","weve","detect","unusu","connect","ip","address","10011236","refer","id","8l0ck1ng15l4m3","unblock","block","persist","continu","brows","webscrapingdev","","enabl","persist","block","persist","flag","mock","page","your","actual","block","scrapfli","academi","v130","made","scrapfli"
  ]
    