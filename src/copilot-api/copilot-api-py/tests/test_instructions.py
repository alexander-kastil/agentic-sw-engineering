from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_all_returns_three_instructions():
    response = client.get("/api/instructions")

    assert response.status_code == 200
    assert response.json() == [
        {"name": "Coding", "description": "Get assistance with code generation and debugging"},
        {"name": "Documentation", "description": "Generate clear and concise documentation"},
        {"name": "Testing", "description": "Help with test case creation and validation"},
    ]


def test_get_by_name_returns_instruction():
    response = client.get("/api/instructions/Coding")

    assert response.status_code == 200
    assert response.json() == {
        "name": "Coding",
        "description": "Get assistance with code generation and debugging",
    }


def test_get_by_name_returns_404_for_unknown_name():
    response = client.get("/api/instructions/Unknown")

    assert response.status_code == 404
