from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_shop_page_lists_every_food_item():
    response = client.get("/")

    assert response.status_code == 200
    for name in ["Butter Chicken", "Curry Wurst", "Blini with Salmon"]:
        assert name in response.text


def test_food_api_returns_the_catalog():
    response = client.get("/api/food")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_shop_page_renders_the_fresh_food_fast_heading():
    response = client.get("/")

    assert "<h1>Fresh Food, Fast</h1>" in response.text
