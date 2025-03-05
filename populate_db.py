import asyncio
import httpx
from typing import Any, Dict

BASE_URL = "http://localhost:8000/api/v1"

async def create_user(client: httpx.AsyncClient, username: str, email: str) -> Dict[str, Any]:
    url = f"{BASE_URL}/users"
    payload = {
        "username": username,
        "email": email,
    }
    response = await client.post(url, json=payload)
    return response.json()

async def create_venue(client: httpx.AsyncClient, name: str, latitude: float, longitude: float) -> Dict[str, Any]:
    url = f"{BASE_URL}/venues"
    payload = {
        "name": name,
        "latitude": latitude,
        "longitude": longitude
    }
    response = await client.post(url, json=payload)
    return response.json()

async def create_event(client: httpx.AsyncClient, name: str, venue_id: int) -> Dict[str, Any]:
    url = f"{BASE_URL}/events"
    payload = {
        "name": name,
        "venue_id": venue_id,
        "description": "Sample event description",
        "starts_at": "2025-03-10T10:00:00Z",
        "duration": 60
    }
    response = await client.post(url, json=payload)
    return response.json()

async def main() -> None:
    async with httpx.AsyncClient() as client:
        # Create users
        user1 = await create_user(client, "user1", "user1@example.com")
        user2 = await create_user(client, "user2", "user2@example.com")

        # Create venues
        venue1 = await create_venue(client, "Venue 1", 40.7128, -74.0060)
        venue2 = await create_venue(client, "Venue 2", 34.0522, -118.2437)

        # Create events
        event1 = await create_event(client, "Event 1 at Venue 1", 1)
        event2 = await create_event(client, "Event 2 at Venue 1", 1)
        event3 = await create_event(client, "Event 1 at Venue 2", 2)
        event4 = await create_event(client, "Event 2 at Venue 2", 2)

        print("Users:", user1, user2)
        print("Venues:", venue1, venue2)
        print("Events:", event1, event2, event3, event4)

if __name__ == "__main__":
    asyncio.run(main())