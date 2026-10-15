import math
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.database import Base, Document, Token, SearchIndex
from app.services.index_service import IndexService

@pytest.fixture
def service():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        for ident, words in [('a', ['rare', 'rare', 'common']), ('b', ['common'])]:
            db.add(Document(id=ident, url=f'https://example.org/{ident}', title=ident))
            db.add_all(Token(document_id=ident, token=word, position=i) for i, word in enumerate(words))
        db.commit()
        yield IndexService(db)

def test_document_frequency_counts_distinct_documents(service):
    index, df = service.build_tfidf_index()
    assert df == {'rare': 1, 'common': 2}
    assert index['rare']['a'] == pytest.approx(2 * math.log(2))
    assert index['common']['a'] == 0
    assert all(score >= 0 for scores in index.values() for score in scores.values())
    assert service.db.query(SearchIndex).filter_by(term='rare').one().document_frequency == 1

def test_and_query_requires_unknown_terms_too(service):
    service.build_tfidf_index()
    assert service.search('rare missing', 'AND') == []
    assert [r['id'] for r in service.search('rare missing', 'OR')] == ['a']

def test_ties_and_duplicate_queries_are_stable(service):
    service.build_tfidf_index()
    assert [r['id'] for r in service.search('common', 'OR')] == ['a', 'b']
    assert service.search('rare rare') == service.search('rare')

def test_empty_query(service):
    service.build_tfidf_index()
    assert service.search('') == []

def test_empty_rebuild_clears_stale_index(service):
    service.build_tfidf_index()
    service.db.query(Token).delete()
    service.db.query(Document).delete()
    service.db.commit()
    assert service.build_tfidf_index() == ({}, {})
    assert service.db.query(SearchIndex).count() == 0
