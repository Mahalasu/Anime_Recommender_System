from flask import Flask, jsonify, request
from rank.service import rank_service
from rank.context import Context

app = Flask('rank-service')


@app.route('/rank')
def get_anime():
    user_id = request.args.get('user_id', type=int)
    context = Context(user_id)
    return jsonify(rank_service.anime_rank(context))
