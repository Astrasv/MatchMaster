from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Import existing tournament structures
import sys
sys.path.append('../')
from Structures.Graph import Graph
from Structures.Scheduler import Scheduler
from Structures.PointsTable import PointTable
from Structures.Stack import Stack
from Structures.Dequeue import Deque

# Import new modules
from database import get_db, engine
from models import Base, User, Tournament, Team, Match, PointsTableEntry
from schemas import (
    UserCreate, UserResponse, UserLogin, TokenResponse,
    TournamentCreate, TournamentResponse, TournamentUpdate,
    TeamCreate, TeamResponse, MatchCreate, MatchResponse, MatchUpdate
)
from auth import (
    create_access_token, verify_token, get_password_hash, verify_password,
    get_current_user, get_current_active_user
)
from services.tournament_service import TournamentService

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MatchMaster API",
    description="Tournament Management Platform API",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()
tournament_service = TournamentService()

# Authentication endpoints
@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role=user.role or "viewer"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/auth/login", response_model=TokenResponse)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    return current_user

# Tournament endpoints
@app.get("/tournaments", response_model=List[TournamentResponse])
async def get_tournaments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    tournaments = db.query(Tournament).all()
    return tournaments

@app.post("/tournaments", response_model=TournamentResponse)
async def create_tournament(
    tournament: TournamentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_tournament = Tournament(
        name=tournament.name,
        description=tournament.description,
        creator_id=current_user.id,
        start_date=tournament.start_date,
        end_date=tournament.end_date
    )
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

@app.get("/tournaments/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(
    tournament_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    return tournament

@app.put("/tournaments/{tournament_id}", response_model=TournamentResponse)
async def update_tournament(
    tournament_id: str,
    tournament_update: TournamentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    for field, value in tournament_update.dict(exclude_unset=True).items():
        setattr(tournament, field, value)
    
    db.commit()
    db.refresh(tournament)
    return tournament

# Team endpoints
@app.post("/tournaments/{tournament_id}/teams", response_model=TeamResponse)
async def create_team(
    tournament_id: str,
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    db_team = Team(
        name=team.name,
        home_ground=team.home_ground,
        tournament_id=tournament_id,
        description=team.description
    )
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@app.get("/tournaments/{tournament_id}/teams", response_model=List[TeamResponse])
async def get_teams(
    tournament_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    teams = db.query(Team).filter(Team.tournament_id == tournament_id).all()
    return teams

# Match scheduling using existing Scheduler.py
@app.post("/tournaments/{tournament_id}/schedule")
async def schedule_matches(
    tournament_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    teams = db.query(Team).filter(Team.tournament_id == tournament_id).all()
    if len(teams) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 teams")
    
    # Use existing Scheduler with Pair Table Algorithm
    result = tournament_service.schedule_tournament_matches(tournament_id, teams, db)
    return result

@app.get("/tournaments/{tournament_id}/matches", response_model=List[MatchResponse])
async def get_matches(
    tournament_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    matches = db.query(Match).filter(Match.tournament_id == tournament_id).all()
    return matches

@app.put("/matches/{match_id}", response_model=MatchResponse)
async def update_match_result(
    match_id: str,
    match_update: MatchUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    # Update match result and recalculate points table
    result = tournament_service.update_match_result(match_id, match_update, db)
    return result

# Points table using existing PointsTable.py
@app.get("/tournaments/{tournament_id}/points-table")
async def get_points_table(
    tournament_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return tournament_service.get_points_table(tournament_id, db)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)