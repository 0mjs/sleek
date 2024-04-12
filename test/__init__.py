from httpx import AsyncClient
import pytest

from app import app


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
async def test_secure_post():
    async with AsyncClient(app=app, base_url="http://sleekify-test") as ac:
        response = await ac.post("/secure-post")
        assert response.status_code == 200
        assert response.json()["session"]["user"] == "Matt"


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
