from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from datetime import datetime
from app.models.schemas import FavoriteEvent

router = APIRouter()

_favorites: Dict[str, dict] = {}

_EVENTS_CATALOG = [
    {"id": "1", "magnitude": 4.2, "depth": 12.5, "origin_time": "2025-01-15T08:23:41Z", "location": "四川雅安"},
    {"id": "2", "magnitude": 3.8, "depth": 8.3, "origin_time": "2025-01-14T14:12:05Z", "location": "云南大理"},
    {"id": "3", "magnitude": 5.1, "depth": 25.0, "origin_time": "2025-01-13T02:45:33Z", "location": "台湾花莲"},
]


@router.post("/favorites", response_model=dict)
def add_favorite(body: FavoriteEvent):
    if body.event_id in _favorites:
        raise HTTPException(status_code=409, detail="Already favorited")
    if not any(e["id"] == body.event_id for e in _EVENTS_CATALOG):
        raise HTTPException(status_code=404, detail="Event not found")
    _favorites[body.event_id] = {
        "event_id": body.event_id,
        "note": body.note or "",
        "created_at": datetime.utcnow().isoformat(),
    }
    return _favorites[body.event_id]


@router.delete("/favorites/{event_id}")
def remove_favorite(event_id: str):
    if event_id not in _favorites:
        raise HTTPException(status_code=404, detail="Not favorited")
    del _favorites[event_id]
    return {"detail": "Removed"}


@router.get("/favorites", response_model=List[dict])
def list_favorites():
    result = []
    for fav in _favorites.values():
        event = next((e for e in _EVENTS_CATALOG if e["id"] == fav["event_id"]), None)
        if event:
            result.append({**event, "note": fav["note"], "favorited_at": fav["created_at"]})
    return result


@router.get("/favorites/{event_id}/status")
def check_favorite(event_id: str):
    return {"favorited": event_id in _favorites}
