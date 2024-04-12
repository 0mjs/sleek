from httpx import AsyncClient
import pytest
import logging

logging.basicConfig(level=logging.DEBUG)

from app import app

# Method testing


@pytest.mark.asyncio
async def test_get_route():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.get("/get-route")
        assert response.status_code == 200
        assert response.json() == {"method": "GET"}


@pytest.mark.asyncio
async def test_post_route():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.post("/post-route", json={"key": "value"})
        assert response.status_code == 200
        assert response.json() == {"method": "POST", "data": {"key": "value"}}


@pytest.mark.asyncio
async def test_put_route():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.put("/put-route", json={"key": "value"})
        assert response.status_code == 200
        assert response.json() == {"method": "PUT", "data": {"key": "value"}}


@pytest.mark.asyncio
async def test_delete_route():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.delete("/delete-route")
        assert response.status_code == 200
        assert response.json() == {"method": "DELETE"}


@pytest.mark.asyncio
async def test_create_item():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.post(
            "/create-item", json={"name": "Sample Item", "price": 150}
        )
        assert response.status_code == 200
        assert response.json() == {
            "item": {"name": "Sample Item", "price": 150},
            "message": "Item created successfully",
        }


# In Depth Usage-focused testing


@pytest.mark.asyncio
async def test_basic_get():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.get("/hello")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello world!"}


@pytest.mark.asyncio
async def test_basic_get_query_params():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.get("/hello-name?name=Matt")
        assert response.status_code == 200
        assert "Hello, Matt!" in response.json()["message"]


@pytest.mark.asyncio
async def test_basic_get_path_params():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.get("/hello/1500")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello, 1500!"}


@pytest.mark.asyncio
async def test_basic_get_request():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.get("/hello-request")
        assert response.status_code == 200
        assert "Hello world!" in response.json()["message"]


@pytest.mark.asyncio
async def test_hello_scope_with_id():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.get("/hello-request/3000")
        assert response.status_code == 200
        assert "Hello, 3000!" in response.json()["message"]
