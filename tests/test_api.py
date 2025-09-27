import json
from flask_app import create_app


def setup_app():
    app = create_app({'TESTING': True})
    return app
password=Piyush@02

def test_health():
    app = setup_app()
    client = app.test_client()
    rv = client.get('/api/health')
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['status'] == 'ok'


def test_items_crud():
    app = setup_app()
    client = app.test_client()

    # list
    rv = client.get('/api/items')
    assert rv.status_code == 200
    items = rv.get_json()
    assert isinstance(items, list)

    # create
    rv = client.post('/api/items', json={'name': 'New', 'value': 10})
    assert rv.status_code == 201
    new_item = rv.get_json()
    assert new_item['name'] == 'New'

    # get
    rv = client.get(f"/api/items/{new_item['id']}")
    assert rv.status_code == 200

    # update
    rv = client.put(f"/api/items/{new_item['id']}", json={'value': 20})
    assert rv.status_code == 200
    updated = rv.get_json()
    assert updated['value'] == 20

    # delete
    rv = client.delete(f"/api/items/{new_item['id']}")
    assert rv.status_code == 204


def test_misc_endpoints():
    app = setup_app()
    client = app.test_client()

    rv = client.get('/api/random')
    assert rv.status_code == 200

    rv = client.post('/api/echo', json={'hello': 'world'})
    assert rv.status_code == 200
    assert rv.get_json()['you_sent']['hello'] == 'world'

    rv = client.get('/api/stats')
    assert rv.status_code == 200

    rv = client.post('/api/uppercase', json={'text': 'hi'})
    assert rv.status_code == 200
    assert rv.get_json()['upper'] == 'HI'

    rv = client.post('/api/multiply', json={'a': 3, 'b': 4})
    assert rv.status_code == 200
    assert rv.get_json()['result'] == 12
