from fastapi import FastAPI, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from .db import init_db, get_session
from .models import Player

app = FastAPI(title="RePosition API", version="0.1.0")


# ---------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------

@app.on_event("startup")
async def on_startup() -> None:
    """Create tables (if they don't exist) and prepare the connection pool."""
    await init_db()


# ---------------------------------------------------------------------
# Health‑check
# ---------------------------------------------------------------------

@app.get("/ping", tags=["System"])
async def ping() -> dict[str, str]:
    """Used by Docker compose / k8s to verify the service is alive."""
    return {"msg": "ok"}


# ---------------------------------------------------------------------
# Players – minimal read API (proof‑of‑life for the DB layer)
# ---------------------------------------------------------------------

@app.get("/player/{player_id}", response_model=Player, tags=["Players"])
async def get_player(player_id: int, session: AsyncSession = Depends(get_session)) -> Player:
    """Return a *Player* with the attached **PlayerStats** (if exists)."""
    db_player: Player | None = await session.get(Player, player_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Player not found")

    # Ensure the 1‑to‑1 relationship 'stats' is loaded
    await session.refresh(db_player, attribute_names=["stats"])
    return db_player
