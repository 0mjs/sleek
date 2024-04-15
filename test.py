from httpx import AsyncClient
import pytest

from app import app

# Method testing


@pytest.mark.asyncio
async def test__methods_GET():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.get("/get-route")
        assert response.status_code == 200
        assert response.json() == {"method": "GET"}


@pytest.mark.asyncio
async def test__methods_POST():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.post("/post-route", json={"key": "value"})
        assert response.status_code == 200
        assert response.json() == {"method": "POST", "data": {"key": "value"}}


@pytest.mark.asyncio
async def test__methods_PUT():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.put("/put-route", json={"key": "value"})
        assert response.status_code == 200
        assert response.json() == {"method": "PUT", "data": {"key": "value"}}


@pytest.mark.asyncio
async def test__methods_DELETE():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.delete("/delete-route")
        assert response.status_code == 200
        assert response.json() == {"method": "DELETE"}


# Pydantic model testing


@pytest.mark.asyncio
async def test__pydantic_model_POST():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.post(
            "/create-item", json={"name": "Sample Item", "price": 150}
        )
        assert response.status_code == 200
        assert response.json() == {
            "message": "Item created.",
            "item": {"name": "Sample Item", "price": 150},
        }


# Smoke testing


@pytest.mark.asyncio
async def test__example_GET():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello world"}


@pytest.mark.asyncio
async def test__example_GET_path_params():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.get("/items/1")
        assert response.status_code == 200
        assert response.json() == {"item_id": "1"}


@pytest.mark.asyncio
async def test__example_GET_nested_path_params():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.get("/items/1/batch/10")
        assert response.status_code == 200
        assert response.json() == {"item_id": "1", "batch_id": "10"}


@pytest.mark.asyncio
async def test__hello_GET_query_params():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.get("/hello-name?name=Matt")
        assert response.status_code == 200
        assert "Hello, Matt!" in response.json()["message"]
