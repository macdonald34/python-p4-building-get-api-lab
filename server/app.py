#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries', methods=['GET'])
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    response = make_response(jsonify(bakeries))
    return response

@app.route('/bakeries/<int:id>', methods=['GET'])
def bakery_by_id(id):
    try:
        bakery = Bakery.query.filter(Bakery.id==id).first()
        if not bakery:
            raise  ValueError(f"No bakery with id {id}")
        else:    
            bakery_dict = bakery.to_dict()    
            response = make_response(jsonify(bakery_dict), 200)
            return response
    except Exception as e:
        return jsonify({"error":"No bakery with that ID", "message": str(e)}), 404

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    try:
        goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
        baked_goods = [good.to_dict() for good in goods]
        response = make_response(jsonify(baked_goods),200)
        return response
    except  Exception as e:
        return jsonify({'error': 'Failed to retrieve data','message':str(e)}),500
    
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    try:
        most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
        if most_expensive_good:
            baked_good_dict = most_expensive_good.to_dict()
            response = make_response(jsonify(baked_good_dict), 200)
            return response
        else:
            return jsonify({'error':'There are no baked goods on record.'}), 404        
    except  Exception as e:
        return jsonify({'error': 'Failed to retrieve data','message':str(e)}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)