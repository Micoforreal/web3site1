from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database for countries and their rankings
leaderboard = [
    {"country": "Turkey", "percentage": 0, "flag": "🇹🇷", "votes": random.randint(10, 100)},
    {"country": "India", "percentage": 0, "flag": "🇮🇳", "votes": random.randint(10, 100)},
    {"country": "Philippines", "percentage": 0, "flag": "🇵🇭", "votes": random.randint(10, 100)},
    {"country": "Mexico", "percentage": 0, "flag": "🇲🇽", "votes": random.randint(10, 100)},
    {"country": "Vietnam", "percentage": 0, "flag": "🇻🇳", "votes": random.randint(10, 100)},
    {"country": "Indonesia", "percentage": 0, "flag": "🇮🇩", "votes": random.randint(10, 100)},
]

# Add 94 more countries with random flags and vote counts
countries_data = [
    ("United States", "🇺🇸"), ("China", "🇨🇳"), ("Brazil", "🇧🇷"), ("Russia", "🇷🇺"),
    ("United Kingdom", "🇬🇧"), ("Germany", "🇩🇪"), ("France", "🇫🇷"), ("Italy", "🇮🇹"),
    ("Canada", "🇨🇦"), ("Spain", "🇪🇸"), ("Japan", "🇯🇵"), ("South Korea", "🇰🇷"),
    ("Australia", "🇦🇺"), ("Netherlands", "🇳🇱"), ("Sweden", "🇸🇪"), ("Switzerland", "🇨🇭"),
    ("Norway", "🇳🇴"), ("Denmark", "🇩🇰"), ("Belgium", "🇧🇪"), ("Finland", "🇫🇮"),
    ("Ireland", "🇮🇪"), ("Singapore", "🇸🇬"), ("Malaysia", "🇲🇾"), ("Thailand", "🇹🇭"),
    ("New Zealand", "🇳🇿"), ("Saudi Arabia", "🇸🇦"), ("Argentina", "🇦🇷"),
    ("Colombia", "🇨🇴"), ("Chile", "🇨🇱"), ("South Africa", "🇿🇦"), ("Nigeria", "🇳🇬"),
    ("Egypt", "🇪🇬"), ("Pakistan", "🇵🇰"), ("Bangladesh", "🇧🇩"), ("Turkey", "🇹🇷"),
    ("Israel", "🇮🇱"), ("Greece", "🇬🇷"), ("Portugal", "🇵🇹"), ("Czechia", "🇨🇿"),
    ("Poland", "🇵🇱"), ("Hungary", "🇭🇺"), ("Austria", "🇦🇹"), ("Romania", "🇷🇴"),
    ("Bulgaria", "🇧🇬"), ("Slovakia", "🇸🇰"), ("Croatia", "🇭🇷"), ("Serbia", "🇷🇸"),
    ("Albania", "🇦🇱"), ("Slovenia", "🇸🇮"), ("Estonia", "🇪🇪"), ("Latvia", "🇱🇻"),
    ("Lithuania", "🇱🇹"), ("Iceland", "🇮🇸"), ("Ukraine", "🇺🇦"), ("Belarus", "🇧🇾"),
    ("Georgia", "🇬🇪"), ("Kazakhstan", "🇰🇿"), ("Uzbekistan", "🇺🇿"), ("Kyrgyzstan", "🇰🇬"),
    ("Mongolia", "🇲🇳"), ("Myanmar", "🇲🇲"), ("Laos", "🇱🇦"), ("Cambodia", "🇰🇭"),
    ("Nepal", "🇳🇵"), ("Bhutan", "🇧🇹"), ("Sri Lanka", "🇱🇰"), ("Maldives", "🇲🇻"),
    ("Afghanistan", "🇦🇫"), ("Iran", "🇮🇷"), ("Iraq", "🇮🇶"), ("Syria", "🇸🇾"),
    ("Lebanon", "🇱🇧"), ("Jordan", "🇯🇴"), ("Palestine", "🇵🇸"), ("Oman", "🇴🇲"),
    ("Yemen", "🇾🇪"), ("Qatar", "🇶🇦"), ("Kuwait", "🇰🇼"), ("Bahrain", "🇧🇭"),
    ("UAE", "🇦🇪"), ("Morocco", "🇲🇦"), ("Algeria", "🇩🇿"), ("Tunisia", "🇹🇳"),
    ("Libya", "🇱🇾"), ("Sudan", "🇸🇩"), ("Ethiopia", "🇪🇹"), ("Kenya", "🇰🇪"),
    ("Tanzania", "🇹🇿"), ("Uganda", "🇺🇬"), ("Rwanda", "🇷🇼"), ("Zambia", "🇿🇲"),
    ("Zimbabwe", "🇿🇼"), ("Botswana", "🇧🇼"), ("Namibia", "🇳🇦"), ("Angola", "🇦🇴"),
    ("Mozambique", "🇲🇿"), ("Madagascar", "🇲🇬")
]

for country, flag in countries_data:
    leaderboard.append({"country": country, "percentage": 0, "flag": flag, "votes": random.randint(10, 100)})

# Data model for incoming vote request
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
    return {"leaderboard": sorted_leaderboard}

@app.post("/vote")
async def vote(vote: Vote):
    """
    Record a vote for a given country.
    """
    for entry in leaderboard:
        if entry["country"].lower() == vote.country.lower():
            entry["votes"] += 1
            return await get_leaderboard()
    raise HTTPException(status_code=404, detail="Country not found")
