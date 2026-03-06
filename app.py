from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import os
from database import get_db_connection, init_bids_table
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, 
            template_folder='.',
            static_folder='.')
app.secret_key = 'ipl_auction_secret_key' # Required for sessions

# Ensure database is ready
init_bids_table()

@app.context_processor
def inject_user():
    return dict(user_logged_in='user_id' in session, current_user=session.get('username'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        try:
            hashed_pw = generate_password_hash(password)
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Username already exists!", 400
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            return "Invalid username or password!", 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def get_highest_bid_data(player_id):
    conn = get_db_connection()
    bid = conn.execute(
        "SELECT bid_amount, bidder_name FROM bids WHERE player_id = ? ORDER BY bid_amount DESC LIMIT 1", 
        (player_id,)
    ).fetchone()
    conn.close()
    if bid:
        return {"amount": bid["bid_amount"], "bidder": bid["bidder_name"]}
    # If no bids exist, return base price (10,000)
    return {"amount": 10000, "bidder": "Starting Price"}

@app.route('/')
def index():
    conn = get_db_connection()
    players = conn.execute("SELECT * FROM players").fetchall()
    
    players_list = []
    for p in players:
        p_dict = dict(p)
        bid_info = get_highest_bid_data(p_dict['id'])
        p_dict['current_bid'] = bid_info['amount']
        p_dict['highest_bidder'] = bid_info['bidder']
        players_list.append(p_dict)
    
    conn.close()
    return render_template('index.html', players=players_list)

@app.route('/player/<int:player_id>')
def player_profile(player_id):
    conn = get_db_connection()
    player = conn.execute("SELECT * FROM players WHERE id = ?", (player_id,)).fetchone()
    conn.close()
    
    if not player:
        return "Player not found", 404
        
    p_dict = dict(player)
    bid_info = get_highest_bid_data(player_id)
    p_dict['current_bid'] = bid_info['amount']
    p_dict['highest_bidder'] = bid_info['bidder']
    
    return render_template('player.html', player=p_dict)

@app.route('/api/players')
def get_players_api():
    conn = get_db_connection()
    players = conn.execute("SELECT * FROM players").fetchall()
    
    players_list = []
    for p in players:
        p_dict = dict(p)
        bid_info = get_highest_bid_data(p_dict['id'])
        p_dict['current_bid'] = bid_info['amount']
        p_dict['highest_bidder'] = bid_info['bidder']
        players_list.append(p_dict)
    
    conn.close()
    return jsonify(players_list)

@app.route('/api/player/<int:player_id>')
def get_player_api(player_id):
    conn = get_db_connection()
    player = conn.execute("SELECT * FROM players WHERE id = ?", (player_id,)).fetchone()
    conn.close()
    
    if not player:
        return jsonify({"error": "Player not found"}), 404
        
    p_dict = dict(player)
    bid_info = get_highest_bid_data(player_id)
    p_dict['current_bid'] = bid_info['amount']
    p_dict['highest_bidder'] = bid_info['bidder']
    
    return jsonify(p_dict)

@app.route('/bid', methods=['POST'])
def place_bid():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "Please login to place a bid."}), 401
        
    data = request.json
    player_id = data.get('player_id')
    bidder_name = session.get('username') # Use the logged-in username
    bid_amount = data.get('bid_amount')
    
    if not all([player_id, bidder_name, bid_amount]):
        return jsonify({"success": False, "message": "Missing required fields"}), 400
    
    try:
        bid_amount = int(bid_amount)
    except ValueError:
        return jsonify({"success": False, "message": "Invalid bid amount"}), 400

    current_bid_info = get_highest_bid_data(player_id)
    
    if bid_amount <= current_bid_info['amount']:
        return jsonify({"success": False, "message": "Bid must be higher than the current bid."}), 400
        
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO bids (player_id, bid_amount, bidder_name) VALUES (?, ?, ?)",
            (player_id, bid_amount, bidder_name)
        )
        conn.commit()
        return jsonify({"success": True, "message": "Bid placed successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
