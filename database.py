import sqlite3
import os

DB_NAME = "ipl_players.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_bids_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create bids table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER NOT NULL,
            bid_amount INTEGER NOT NULL,
            bidder_name TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES players (id)
        )
    ''')

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_bids_table()
    print("Bids table initialized in ipl_players.db")
