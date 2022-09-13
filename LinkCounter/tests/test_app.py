import time
import pytest


POST_URL = 'http://127.0.0.1:8000/visited_links'
GET_URL = 'http://127.0.0.1:8000/visited_domains'



def test_1(client):
    json = {
        "links": [
            "https://ya.ru",
            "https://ya.ru?q=123",
            "funbox.ru",
            "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
        ]
    }
    response = client.post(POST_URL, json, content_type='application/json')
    assert response.status_code == 201


def test_2(client):
    response = client.get("http://127.0.0.1:8000/visited_domains?from=1663057817&to=1663057917")
    assert response.status_code == 200