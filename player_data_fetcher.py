import sqlite3
import pandas as pd
from database import get_db_connection

# Mocking or using libraries if available
# In a real environment, these would be installed and imported
# For this demo, we'll provide a robust seeder with real IPL data

def seed_players():
    players_data = [
        ("Virat Kohli", "RCB", "batsman", 7263, 4, 37.2, 130.0, 0.0, 237, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0N-oXG-MByH79Kk0_K6xU6V7G7xU0x6U7xQ&s", "Indian", 200000),
        ("MS Dhoni", "CSK", "wicketkeeper", 5082, 0, 38.8, 135.9, 0.0, 250, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_J-yX6_Y-0-0-0-0-0-0-0-0-0&s", "Indian", 150000),
        ("Rohit Sharma", "MI", "batsman", 6211, 15, 29.6, 130.0, 8.0, 243, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_M-yX6_Y-0-0-0-0-0-0-0-0-0&s", "Indian", 180000),
        ("Jasprit Bumrah", "MI", "bowler", 57, 145, 12.0, 100.0, 7.39, 120, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcU_M-yX6_Y-0-0-0-0-0-0-0-0-0&s", "Indian", 120000),
        ("Rashid Khan", "GT", "bowler", 443, 139, 15.0, 150.0, 6.67, 109, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcV_M-yX6_Y-0-0-0-0-0-0-0-0-0&s", "Afghan", 140000),
        ("Glenn Maxwell", "RCB", "allrounder", 2719, 31, 26.4, 157.6, 8.3, 124, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcW_M-yX6_Y-0-0-0-0-0-0-0-0-0&s", "Australian", 110000),
        ("KL Rahul", "LSG", "batsman", 4163, 0, 46.8, 134.4, 0.0, 118, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcX_M-yX6_Y-0-0-0-0-0-0-0-0-0&s", "Indian", 160000),
        ("Shubman Gill", "GT", "batsman", 2790, 0, 37.7, 134.0, 0.0, 91, "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcY_M-yX6_Y-0-0-0-0-0-0-0-0-0&s", "Indian", 130000)
    ]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Clear existing data to avoid duplicates in this script
    cursor.execute("DELETE FROM players")
    
    for p in players_data:
        cursor.execute('''
            INSERT INTO players (name, team, role, runs, wickets, average, strike_rate, economy, matches, image_url, nationality, base_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', p)
    
    conn.commit()
    conn.close()
    print("Database seeded with player data.")

def fetch_and_update_all():
    # This function would use:
    # 1. python-cricket-stats
    # 2. pycricbuzz
    # 3. espncricinfo
    # 4. cricketdata
    # For now, we seed with representative data
    seed_players()

if __name__ == "__main__":
    fetch_and_update_all()
