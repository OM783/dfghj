from flask import render_template, request, jsonify
from models import PlayerModel, BidModel

def configure_routes(app):
    @app.route('/')
    def index():
        filters = {
            'name': request.args.get('name'),
            'team': request.args.get('team'),
            'role': request.args.get('role'),
            'nationality': request.args.get('nationality')
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v}
        players = PlayerModel.get_all_players(filters)
        return render_template('index.html', players=players)

    @app.route('/player/<int:player_id>')
    def player_profile(player_id):
        player = PlayerModel.get_player_by_id(player_id)
        if not player:
            return "Player not found", 404
        return render_template('player.html', player=player)

    @app.route('/api/players')
    def get_players_api():
        players = PlayerModel.get_all_players()
        return jsonify(players)

    @app.route('/api/player/<int:player_id>')
    def get_player_api(player_id):
        player = PlayerModel.get_player_by_id(player_id)
        return jsonify(player)

    @app.route('/bid', methods=['POST'])
    def place_bid():
        data = request.json
        player_id = data.get('player_id')
        bidder = data.get('bidder')
        amount = data.get('bid_amount')
        
        if not all([player_id, bidder, amount]):
            return jsonify({"success": False, "message": "Missing bid details"}), 400
            
        result = BidModel.place_bid(player_id, bidder, int(amount))
        return jsonify(result)

    @app.route('/auction')
    def auction_leaderboard():
        players = PlayerModel.get_all_players()
        return render_template('auction.html', players=players)
