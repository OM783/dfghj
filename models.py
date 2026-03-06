from database import get_db_connection

class PlayerModel:
    @staticmethod
    def get_all_players(filters=None):
        conn = get_db_connection()
        query = "SELECT p.*, (SELECT MAX(bid_amount) FROM bids WHERE player_id = p.id) as current_bid FROM players p WHERE 1=1"
        params = []
        
        if filters:
            if 'name' in filters:
                query += " AND name LIKE ?"
                params.append(f"%{filters['name']}%")
            if 'team' in filters:
                query += " AND team = ?"
                params.append(filters['team'])
            if 'role' in filters:
                query += " AND role = ?"
                params.append(filters['role'])
            if 'nationality' in filters:
                query += " AND nationality = ?"
                params.append(filters['nationality'])

        players = conn.execute(query, params).fetchall()
        conn.close()
        return [dict(p) for p in players]

    @staticmethod
    def get_player_by_id(player_id):
        conn = get_db_connection()
        player = conn.execute("SELECT * FROM players WHERE id = ?", (player_id,)).fetchone()
        if not player:
            conn.close()
            return None
        
        # Get highest bid and bidder
        bid = conn.execute("SELECT bid_amount, bidder_name FROM bids WHERE player_id = ? ORDER BY bid_amount DESC LIMIT 1", (player_id,)).fetchone()
        
        player_dict = dict(player)
        player_dict['current_bid'] = bid['bid_amount'] if bid else player_dict['base_price']
        player_dict['highest_bidder'] = bid['bidder_name'] if bid else "None"
        
        conn.close()
        return player_dict

class BidModel:
    @staticmethod
    def get_highest_bid(player_id):
        conn = get_db_connection()
        bid = conn.execute("SELECT MAX(bid_amount) as max_bid FROM bids WHERE player_id = ?", (player_id,)).fetchone()
        conn.close()
        return bid['max_bid'] if bid['max_bid'] else 0

    @staticmethod
    def place_bid(player_id, bidder_name, amount):
        current_highest = BidModel.get_highest_bid(player_id)
        
        # Also check base price
        conn = get_db_connection()
        player = conn.execute("SELECT base_price FROM players WHERE id = ?", (player_id,)).fetchone()
        
        if not player:
            conn.close()
            return {"success": False, "message": "Player not found"}
        
        min_required = max(current_highest, player['base_price'])
        
        if amount > min_required:
            conn.execute("INSERT INTO bids (player_id, bid_amount, bidder_name) VALUES (?, ?, ?)", 
                         (player_id, amount, bidder_name))
            conn.commit()
            conn.close()
            return {"success": True, "message": "Bid placed successfully!"}
        
        conn.close()
        return {"success": False, "message": "Bid must be higher than the current bid and base price."}

    @staticmethod
    def get_bids_for_player(player_id):
        conn = get_db_connection()
        bids = conn.execute("SELECT * FROM bids WHERE player_id = ? ORDER BY timestamp DESC", (player_id,)).fetchall()
        conn.close()
        return [dict(b) for b in bids]
