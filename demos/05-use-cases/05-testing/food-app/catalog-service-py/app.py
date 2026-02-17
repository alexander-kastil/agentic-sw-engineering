import os
import sys
import json
from datetime import datetime, timezone
from decimal import Decimal
from flask import Flask, request, jsonify
from models import db, CatalogItem
from config import Config
from database import init_db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def serialize_response(data):
    return json.loads(json.dumps(data, default=decimal_default))

@app.before_request
def before_request():
    pass

@app.route('/food', methods=['GET'])
def get_food():
    items = CatalogItem.query.all()
    result = [item.to_dict() for item in items]
    return jsonify(result), 200

@app.route('/food/<int:id>', methods=['GET'])
def get_food_by_id(id):
    item = CatalogItem.query.filter_by(id=id).first()
    if item:
        return jsonify(item.to_dict()), 200
    return jsonify(None), 200

@app.route('/food', methods=['POST'])
def create_food():
    data = request.get_json()
    
    item = CatalogItem()
    item.name = data.get('name')
    item.price = Decimal(str(data.get('price', 0)))
    item.in_stock = data.get('inStock', 0)
    item.picture_url = data.get('pictureUrl')
    item.description = data.get('description')
    
    db.session.add(item)
    db.session.commit()
    
    return jsonify(item.to_dict()), 201

@app.route('/food', methods=['PUT'])
def update_food():
    data = request.get_json()
    
    item_id = data.get('id')
    item = CatalogItem.query.filter_by(id=item_id).first()
    
    if item:
        if 'name' in data:
            item.name = data['name']
        if 'price' in data:
            item.price = Decimal(str(data['price']))
        if 'inStock' in data:
            item.in_stock = data['inStock']
        if 'pictureUrl' in data:
            item.picture_url = data['pictureUrl']
        if 'description' in data:
            item.description = data['description']
        
        db.session.commit()
    
    return jsonify(item.to_dict() if item else None), 200

@app.route('/food/<int:id>', methods=['DELETE'])
def delete_food(id):
    item = CatalogItem.query.filter_by(id=id).first()
    
    if item:
        db.session.delete(item)
        db.session.commit()
    
    return jsonify({}), 200

@app.route('/config', methods=['GET'])
def get_config():
    config_data = {
        'title': 'Catalog Service',
        'app': {
            'authEnabled': Config.AUTH_ENABLED,
            'useAppConfig': False,
            'useSQLite': Config.USE_SQLITE,
            'connectionStrings': {
                'sqliteDbConnection': 'Data Source=./food.db',
                'sqlServerConnection': ''
            }
        },
        'logging': {
            'logLevel': {
                'default': 'Information',
                'microsoft': 'Warning'
            }
        }
    }
    return jsonify(config_data), 200

@app.route('/config/getEnvVars', methods=['GET'])
def get_env_vars():
    env_vars = dict(os.environ)
    return jsonify(env_vars), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    init_db(app)
    
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
