# backend/app/models.py
from __future__ import annotations
from datetime import date, datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


# ------------------------------------------------------------------
# 1) טבלת ליבה – Player  (+ PlayerStats – 1-to-1)
# ------------------------------------------------------------------
class Player(SQLModel, table=True):
    id: int = Field(primary_key=True, alias="player_id")
    full_name: str = Field(index=True, alias="name")
    birth_date: date = Field(alias="date_of_birth")
    nationality: str = Field(alias="country_of_citizenship")
    natural_position: str = Field(alias="sub_position")
    preferred_foot: Optional[str] = Field(alias="foot", default=None)
    height_cm: Optional[int] = Field(alias="height_in_cm", default=None)
    current_club_name: Optional[str] = None
    club_id: Optional[int] = Field(default=None, foreign_key="club.id")

    # ── relationships ─────────────────────────────────────────────
    stats:  PlayerStats = Relationship(back_populates="player",
                                       sa_relationship_kwargs={"uselist": False})
    appearances: List["Appearance"] = Relationship(back_populates="player")
    valuations:  List["PlayerValuation"] = Relationship(back_populates="player")


class PlayerStats(SQLModel, table=True):
    """
    עמודות פיצ'רים מתוך players_joined_clean.csv
    (עמודות עם רווחים → קו תחתי + alias).
    """
    player_id: int = Field(primary_key=True, foreign_key="player.id")

    # --- כספים ---
    market_value_eur: Optional[int] = None
    highest_market_value_eur: Optional[int] = None

    # --- Overall ---
    OVR: Optional[int] = None
    PAC: Optional[int] = None
    SHO: Optional[int] = None
    PAS: Optional[int] = None
    DRI: Optional[int] = None
    DEF: Optional[int] = None
    PHY: Optional[int] = None

    # --- Attributes ---
    Acceleration: Optional[int] = None
    Sprint_Speed: Optional[int] = Field(default=None, alias="Sprint Speed")
    Positioning: Optional[int] = None
    Finishing: Optional[int] = None
    Shot_Power: Optional[int] = Field(default=None, alias="Shot Power")
    Long_Shots: Optional[int] = Field(default=None, alias="Long Shots")
    Volleys: Optional[int] = None
    Penalties: Optional[int] = None
    Vision: Optional[int] = None
    Crossing: Optional[int] = None
    Free_Kick_Accuracy: Optional[int] = Field(default=None, alias="Free Kick Accuracy")
    Short_Passing: Optional[int] = Field(default=None, alias="Short Passing")
    Long_Passing: Optional[int] = Field(default=None, alias="Long Passing")
    Curve: Optional[int] = None
    Dribbling: Optional[int] = None
    Agility: Optional[int] = None
    Balance: Optional[int] = None
    Reactions: Optional[int] = None
    Ball_Control: Optional[int] = Field(default=None, alias="Ball Control")
    Composure: Optional[int] = None
    Interceptions: Optional[int] = None
    Heading_Accuracy: Optional[int] = Field(default=None, alias="Heading Accuracy")
    Def_Awareness: Optional[int] = Field(default=None, alias="Def Awareness")
    Standing_Tackle: Optional[int] = Field(default=None, alias="Standing Tackle")
    Sliding_Tackle: Optional[int] = Field(default=None, alias="Sliding Tackle")
    Jumping: Optional[int] = None
    Stamina: Optional[int] = None
    Strength: Optional[int] = None
    Aggression: Optional[int] = None
    Weak_foot: Optional[int] = Field(default=None, alias="Weak foot")
    Skill_moves: Optional[int] = Field(default=None, alias="Skill moves")
    Preferred_foot_stat: Optional[str] = Field(default=None, alias="Preferred foot")
    Alternative_positions: Optional[str] = Field(default=None, alias="Alternative positions")
    Play_style: Optional[str] = Field(default=None, alias="play style")
    GK_Diving: Optional[int] = Field(default=None, alias="GK Diving")
    GK_Handling: Optional[int] = Field(default=None, alias="GK Handling")
    GK_Kicking: Optional[int] = Field(default=None, alias="GK Kicking")
    GK_Positioning: Optional[int] = Field(default=None, alias="GK Positioning")
    GK_Reflexes: Optional[int] = Field(default=None, alias="GK Reflexes")

    League: Optional[str] = None
    Team: Optional[str] = None
    Weight: Optional[str] = None

    # ── relationship ──────────────────────────────────────────────
    player: Player = Relationship(back_populates="stats")


# ------------------------------------------------------------------
# 2) ישויות סביבת משחק (Club, Competition, Game …)
# ------------------------------------------------------------------
class Club(SQLModel, table=True):
    id: int = Field(primary_key=True, alias="club_id")
    name: str
    country: Optional[str] = None

    players: List[Player] = Relationship(back_populates="club",
                                         sa_relationship_kwargs={"foreign_keys": "[Player.club_id]"})
    appearances: List["Appearance"] = Relationship(back_populates="club")
    home_games: List["Game"] = Relationship(back_populates="home_club",
                                            sa_relationship_kwargs={"foreign_keys": "[Game.home_club_id]"})
    away_games: List["Game"] = Relationship(back_populates="away_club",
                                            sa_relationship_kwargs={"foreign_keys": "[Game.away_club_id]"})


class Competition(SQLModel, table=True):
    id: int = Field(primary_key=True, alias="competition_id")
    name: str
    country: Optional[str] = None
    level: Optional[int] = None

    games: List["Game"] = Relationship(back_populates="competition")


class Game(SQLModel, table=True):
    id: int = Field(primary_key=True, alias="game_id")
    date: datetime
    competition_id: int = Field(foreign_key="competition.id")
    home_club_id: int = Field(foreign_key="club.id")
    away_club_id: int = Field(foreign_key="club.id")

    competition: Competition = Relationship(back_populates="games")
    home_club: Club = Relationship(back_populates="home_games",
                                   sa_relationship_kwargs={"foreign_keys": "[Game.home_club_id]"})
    away_club: Club = Relationship(back_populates="away_games",
                                   sa_relationship_kwargs={"foreign_keys": "[Game.away_club_id]"})
    appearances: List["Appearance"] = Relationship(back_populates="game")
    events: List["GameEvent"] = Relationship(back_populates="game")


class Appearance(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    player_id: int = Field(foreign_key="player.id")
    club_id: int = Field(foreign_key="club.id")
    minutes_played: int
    position: Optional[str] = None

    game: Game = Relationship(back_populates="appearances")
    player: Player = Relationship(back_populates="appearances")
    club: Club = Relationship(back_populates="appearances")


class GameEvent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    minute: int
    type: str                          # 'goal', 'card', …
    player_id: Optional[int] = Field(default=None, foreign_key="player.id")

    game: Game = Relationship(back_populates="events")


# ------------------------------------------------------------------
# 3) Market-value היסטורי (Transfermarkt למשל)
# ------------------------------------------------------------------
class PlayerValuation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    player_id: int = Field(foreign_key="player.id")
    date: date
    market_value_eur: int

    player: Player = Relationship(back_populates="valuations")
