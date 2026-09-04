from app.services import item_service


def test_get_item_returns_none_when_missing(clean_db, db_session):
    # base fraîche (clean_db) → un id inexistant renvoie None, SANS aucun HTTP
    assert item_service.get_item(db_session, 999999) is None
