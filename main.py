from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from typing import Dict, List
from datetime import datetime
from collections import deque

app = FastAPI()

# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store recent votes in a deque (limited to last 50 votes)
recent_votes = deque(maxlen=50)

# Initial countries with their flags
leaderboard = [
    {"country": "Turkey", "percentage": 0, "flag": "🇹🇷", "votes": random.randint(10, 100)},
    {"country": "India", "percentage": 0, "flag": "🇮🇳", "votes": random.randint(10, 100)},
    {"country": "Philippines", "percentage": 0, "flag": "🇵🇭", "votes": random.randint(10, 100)},
    {"country": "Mexico", "percentage": 0, "flag": "🇲🇽", "votes": random.randint(10, 100)},
    {"country": "Vietnam", "percentage": 0, "flag": "🇻🇳", "votes": random.randint(10, 100)},
    {"country": "Indonesia", "percentage": 0, "flag": "🇮🇩", "votes": random.randint(10, 100)},
]

# Additional countries with their flags
countries_data = [
    ("United States", "🇺🇸"), ("China", "🇨🇳"), ("Brazil", "🇧🇷"), ("Russia", "🇷🇺"),
    ("United Kingdom", "🇬🇧"), ("Germany", "🇩🇪"), ("France", "🇫🇷"), ("Italy", "🇮🇹"),
    ("Canada", "🇨🇦"), ("Spain", "🇪🇸"), ("Japan", "🇯🇵"), ("South Korea", "🇰🇷"),
    ("Australia", "🇦🇺"), ("Netherlands", "🇳🇱"), ("Sweden", "🇸🇪"), ("Switzerland", "🇨🇭"),
    ("Norway", "🇳🇴"), ("Denmark", "🇩🇰"), ("Belgium", "🇧🇪"), ("Finland", "🇫🇮"),
    ("Ireland", "🇮🇪"), ("Singapore", "🇸🇬"), ("Malaysia", "🇲🇾"), ("Thailand", "🇹🇭"),
    ("New Zealand", "🇳🇿"), ("Saudi Arabia", "🇸🇦"), ("Argentina", "🇦🇷"),
    ("Colombia", "🇨🇴"), ("Chile", "🇨🇱"), ("South Africa", "🇿🇦"), ("Nigeria", "🇳🇬"),
    ("Egypt", "🇪🇬"), ("Pakistan", "🇵🇰"), ("Bangladesh", "🇧🇩"), ("Israel", "🇮🇱"),
    ("Greece", "🇬🇷"), ("Portugal", "🇵🇹"), ("Czechia", "🇨🇿"), ("Poland", "🇵🇱"),
    ("Hungary", "🇭🇺"), ("Austria", "🇦🇹"), ("Romania", "🇷🇴"), ("Bulgaria", "🇧🇬"),
    ("Slovakia", "🇸🇰"), ("Croatia", "🇭🇷"), ("Serbia", "🇷🇸"), ("Albania", "🇦🇱"),
    ("Slovenia", "🇸🇮"), ("Estonia", "🇪🇪"), ("Latvia", "🇱🇻"), ("Lithuania", "🇱🇹"),
    ("Iceland", "🇮🇸"), ("Ukraine", "🇺🇦"), ("Belarus", "🇧🇾"), ("Georgia", "🇬🇪"),
    ("Kazakhstan", "🇰🇿"), ("Uzbekistan", "🇺🇿"), ("Kyrgyzstan", "🇰🇬"), ("Mongolia", "🇲🇳"),
    ("Myanmar", "🇲🇲"), ("Laos", "🇱🇦"), ("Cambodia", "🇰🇭"), ("Nepal", "🇳🇵"),
    ("Bhutan", "🇧🇹"), ("Sri Lanka", "🇱🇰"), ("Maldives", "🇲🇻"), ("Afghanistan", "🇦🇫"),
    ("Iran", "🇮🇷"), ("Iraq", "🇮🇶"), ("Syria", "🇸🇾"), ("Lebanon", "🇱🇧"),
    ("Jordan", "🇯🇴"), ("Palestine", "🇵🇸"), ("Oman", "🇴🇲"), ("Yemen", "🇾🇪"),
    ("Qatar", "🇶🇦"), ("Kuwait", "🇰🇼"), ("Bahrain", "🇧🇭"), ("UAE", "🇦🇪"),
    ("Morocco", "🇲🇦"), ("Algeria", "🇩🇿"), ("Tunisia", "🇹🇳"), ("Libya", "🇱🇾"),
    ("Sudan", "🇸🇩"), ("Ethiopia", "🇪🇹"), ("Kenya", "🇰🇪"), ("Tanzania", "🇹🇿"),
    ("Uganda", "🇺🇬"), ("Rwanda", "🇷🇼"), ("Zambia", "🇿🇲"), ("Zimbabwe", "🇿🇼"),
    ("Botswana", "🇧🇼"), ("Namibia", "🇳🇦"), ("Angola", "🇦🇴"), ("Mozambique", "🇲🇿"),
    ("Madagascar", "🇲🇬")
]

# Add additional countries to the leaderboard
for country, flag in countries_data:
    if not any(entry["country"] == country for entry in leaderboard):
        leaderboard.append({
            "country": country,
            "percentage": 0,
            "flag": flag,
            "votes": random.randint(10, 100)
        })

# Store IP votes with timestamp
ip_votes: Dict[str, Dict[str, datetime]] = {}

class Vote(BaseModel):
    country: str

@app.get("/leaderboard")
async def get_leaderboard():
    """
    Retrieve the leaderboard sorted by votes.
    """
    sorted_leaderboard = sorted(leaderboard, key=lambda x: x["votes"], reverse=True)
    total_votes = sum(entry["votes"] for entry in sorted_leaderboard)
    
    for entry in sorted_leaderboard:
        entry["percentage"] = round((entry["votes"] / total_votes) * 100, 2) if total_votes > 0 else 0
    
    return {
        "leaderboard": sorted_leaderboard,
        "total_votes": total_votes
    }

@app.get("/recent-votes")
async def get_recent_votes():
    """
    Get the most recent votes without IP information
    """
    return {"recent_votes": list(recent_votes)}

@app.get("/my-votes")
async def get_my_votes(request: Request):
    """
    Get all votes made by the current IP address
    """
    client_ip = request.client.host
    if client_ip in ip_votes:
        return {
            "votes": [
                {
                    "country": country,
                    "timestamp": timestamp
                }
                for country, timestamp in ip_votes[client_ip].items()
            ]
        }
    return {"votes": []}

@app.get("/stats")
async def get_stats():
    """
    Get voting statistics
    """
    total_unique_voters = len(ip_votes)
    total_votes = sum(len(votes) for votes in ip_votes.values())
    
    return {
        "unique_voters": total_unique_voters,
        "total_votes": total_votes,
        "votes_per_ip_average": round(total_votes / total_unique_voters, 2) if total_unique_voters > 0 else 0
    }

@app.post("/vote")
async def vote(vote: Vote, request: Request):
    """
    Record a vote and add it to recent votes
    """
    client_ip = request.client.host
    
    # Initialize IP record if it doesn't exist
    if client_ip not in ip_votes:
        ip_votes[client_ip] = {}
    
    # Find country and its flag
    country_flag = None
    country_exists = False
    for entry in leaderboard:
        if entry["country"].lower() == vote.country.lower():
            country_exists = True
            country_flag = entry["flag"]
            ip_votes[client_ip][vote.country] = datetime.now()
            entry["votes"] += 1
            break
    
    if not country_exists:
        raise HTTPException(status_code=404, detail="Country not found")
    
    # Add to recent votes
    recent_votes.appendleft({
        "country": vote.country,
        "flag": country_flag,
        "timestamp": datetime.now().isoformat()
    })
    
    # Get updated leaderboard
    current_leaderboard = await get_leaderboard()
    # Get user's voting history
    user_votes = await get_my_votes(request)
    # Get updated stats
    stats = await get_stats()
    
    return {
        **current_leaderboard,
        "user_votes": user_votes,
        "recent_votes": list(recent_votes),
        "stats": stats
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)