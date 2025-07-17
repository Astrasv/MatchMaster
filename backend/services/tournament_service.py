import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from Structures.Graph import Graph
from Structures.Scheduler import Scheduler
from Structures.PointsTable import PointTable
from Structures.Stack import Stack
from Structures.Dequeue import Deque
from sqlalchemy.orm import Session
from models import Tournament, Team, Match, PointsTableEntry
from schemas import MatchUpdate
from typing import List, Dict, Any
import uuid

class TournamentService:
    def __init__(self):
        pass
    
    def schedule_tournament_matches(self, tournament_id: str, teams: List[Team], db: Session) -> Dict[str, Any]:
        """
        Use existing Scheduler.py with Pair Table Algorithm to schedule matches
        """
        if len(teams) < 2:
            raise ValueError("Need at least 2 teams")
        
        # Initialize scheduler with existing algorithm
        scheduler = Scheduler(len(teams))
        scheduler.generate()
        
        # Clear existing matches for this tournament
        db.query(Match).filter(Match.tournament_id == tournament_id).delete()
        
        # Create matches based on scheduler output
        match_count = 1
        scheduled_matches = []
        
        for round_idx in range(scheduler.rows * 2):
            for match_idx in range(scheduler.cols):
                i = scheduler.merged_table[round_idx][match_idx][0]
                j = scheduler.merged_table[round_idx][match_idx][1]
                
                if i == "bye" or j == "bye":
                    continue
                
                team1 = teams[i - 1]
                team2 = teams[j - 1]
                
                # Create match in database
                db_match = Match(
                    tournament_id=tournament_id,
                    team1_id=team1.id,
                    team2_id=team2.id,
                    venue=team1.home_ground,  # Home ground advantage
                    status="scheduled"
                )
                db.add(db_match)
                scheduled_matches.append({
                    "match_number": match_count,
                    "team1": team1.name,
                    "team2": team2.name,
                    "venue": team1.home_ground
                })
                match_count += 1
        
        db.commit()
        
        return {
            "total_matches": scheduler.totalmatches,
            "scheduled_matches": scheduled_matches,
            "message": f"Successfully scheduled {len(scheduled_matches)} matches using Pair Table Algorithm"
        }
    
    def update_match_result(self, match_id: str, match_update: MatchUpdate, db: Session) -> Match:
        """
        Update match result and recalculate points table using existing logic
        """
        match = db.query(Match).filter(Match.id == match_id).first()
        if not match:
            raise ValueError("Match not found")
        
        # Update match
        if match_update.winner_id:
            match.winner_id = match_update.winner_id
            match.status = "completed"
        
        db.commit()
        db.refresh(match)
        
        # Recalculate points table using existing PointsTable logic
        self._update_points_table(match.tournament_id, db)
        
        return match
    
    def get_points_table(self, tournament_id: str, db: Session) -> Dict[str, Any]:
        """
        Get points table using existing PointsTable.py logic
        """
        # Get all teams and matches for this tournament
        teams = db.query(Team).filter(Team.tournament_id == tournament_id).all()
        matches = db.query(Match).filter(
            Match.tournament_id == tournament_id,
            Match.status == "completed"
        ).all()
        
        # Initialize existing PointTable class
        point_table = PointTable()
        
        # Create team objects compatible with existing logic
        team_objects = {}
        for team in teams:
            # Create a simple team object that matches existing structure
            team_obj = type('Team', (), {
                'name': team.name,
                'points': 0,
                'wins': 0,
                'loses': 0,
                'matches': 0,
                'last_five_matches': Stack()
            })()
            team_objects[str(team.id)] = team_obj
            point_table.add_team(team_obj)
        
        # Process matches to update points
        for match in matches:
            if match.winner_id:
                winner_obj = team_objects[str(match.winner_id)]
                loser_id = str(match.team1_id) if str(match.winner_id) == str(match.team2_id) else str(match.team2_id)
                loser_obj = team_objects[loser_id]
                
                # Update statistics
                winner_obj.points += 2
                winner_obj.wins += 1
                winner_obj.matches += 1
                loser_obj.loses += 1
                loser_obj.matches += 1
        
        # Sort using existing quicksort algorithm
        if len(point_table.table) > 1:
            point_table.sort_by_points(point_table.table, 0, len(point_table.table) - 1)
        
        # Format response
        table_data = []
        for team_obj in point_table.table:
            table_data.append({
                "team_name": team_obj.name,
                "matches_played": team_obj.matches,
                "wins": team_obj.wins,
                "losses": team_obj.loses,
                "points": team_obj.points
            })
        
        return {
            "tournament_id": tournament_id,
            "points_table": table_data,
            "last_updated": "now"
        }
    
    def _update_points_table(self, tournament_id: str, db: Session):
        """
        Internal method to update points table in database
        """
        # Clear existing points table entries
        db.query(PointsTableEntry).filter(PointsTableEntry.tournament_id == tournament_id).delete()
        
        # Get updated points table
        points_data = self.get_points_table(tournament_id, db)
        
        # Create new points table entries
        teams = db.query(Team).filter(Team.tournament_id == tournament_id).all()
        team_name_to_id = {team.name: team.id for team in teams}
        
        for entry in points_data["points_table"]:
            team_id = team_name_to_id.get(entry["team_name"])
            if team_id:
                points_entry = PointsTableEntry(
                    tournament_id=tournament_id,
                    team_id=team_id,
                    points=entry["points"],
                    matches_played=entry["matches_played"],
                    wins=entry["wins"],
                    losses=entry["losses"]
                )
                db.add(points_entry)
        
        db.commit()