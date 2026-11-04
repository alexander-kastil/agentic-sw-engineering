from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_renders_heading_text():
    response = client.get("/")

    assert response.status_code == 200
    assert "<h1>Python Food Shop</h1>" in response.text


def test_renders_greeting():
    response = client.get("/")

    assert "<h5>Hello Development Environment</h5>" in response.text


def test_renders_image_with_correct_src():
    response = client.get("/")

    assert '<img src="food.png"' in response.text


def test_increments_count_on_button_click():
    response = client.get("/")

    assert "Button clicked 0 times" in response.text
    assert '<input type="hidden" name="count" value="1">' in response.text

    response = client.get("/", params={"count": 1})

    assert "Button clicked 1 times" in response.text
    assert '<input type="hidden" name="count" value="2">' in response.text


def test_rejects_non_numeric_count():
    response = client.get("/", params={"count": "abc"})

    assert response.status_code == 422


def test_serves_food_image():
    response = client.get("/food.png")

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


def test_serves_stylesheet():
    response = client.get("/styles.css")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/css")


def test_returns_404_for_unknown_path():
    response = client.get("/unknown")

    assert response.status_code == 404
