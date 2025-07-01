#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    pass

@app.route('/articles/<int:id>', methods=['GET'])
def show_article(id):
    # Step 1: Find the article by ID
    article = Article.query.get(id)
    if not article:
        return make_response({'error': 'Article not found'}, 404)

    # Step 2: Initialize session page_views if not already set
    if 'page_views' not in session:
        session['page_views'] = 0

    # Step 3: Increment the page view count
    session['page_views'] += 1

    # Step 4: Check if the user has exceeded the limit
    if session['page_views'] <= 3:
        # They haven't exceeded — return article data
        return jsonify(article.to_dict()), 200
    else:
        # They exceeded the limit — return error and status 401
        return make_response({'message': 'Maximum pageview limit reached'}, 401)


# if __name__ == '__main__':
#     app.run(port=5555)
