from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article

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

    return {'message': '200: Successfully cleared session data'}, 200

@app.route('/articles')
def index_articles():
    articles = [article.to_dict() for article in Article.query.all()]
    return make_response(jsonify(articles), 200)

@app.route('/articles/<int:id>', methods=['GET'])
def view_article(id):
    session['page_views'] = session.get('page_views', 0)
    session['page_views'] += 1
    if session['page_views'] <= 3:
        article_data = {
            'id': id,
            'title': f'Article {id}',
            'content': f'Content of Article {id}',
        }
        return jsonify(article_data), 200
    else:
        error_message = {'message': 'Maximum pageview limit reached'}
        return jsonify(error_message), 401
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)