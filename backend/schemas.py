from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
import uuid

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "viewer"

class UserResponse(UserBase):
    id: uuid.UUID
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Tournament schemas
class TournamentBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class TournamentCreate(TournamentBase):
    pass

class TournamentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class TournamentResponse(TournamentBase):
    id: uuid.UUID
    creator_id: uuid.UUID
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Team schemas
class TeamBase(BaseModel):
    name: str
    home_ground: str
    description: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: uuid.UUID
    tournament_id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

# Match schemas
class MatchBase(BaseModel):
    scheduled_date: Optional[date] = None
    venue: Optional[str] = None

class MatchCreate(MatchBase):
    team1_id: uuid.UUID
    team2_id: uuid.UUID

class MatchUpdate(BaseModel):
    status: Optional[str] = None
    winner_id: Optional[uuid.UUID] = None

class MatchResponse(MatchBase):
    id: uuid.UUID
    tournament_id: uuid.UUID
    team1_id: uuid.UUID
    team2_id: uuid.UUID
    status: str
    winner_id: Optional[uuid.UUID] = None
    created_at: datetime
    
    class Config:
        from_attributes = True