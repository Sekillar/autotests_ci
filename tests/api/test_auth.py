import requests


def test_status():
    resp = requests.get("https://b2b.firstline-dev.com/")
    assert resp.status_code == 200, f"Статус код некорректный, \n{resp.status_code}"
    print("API работает")