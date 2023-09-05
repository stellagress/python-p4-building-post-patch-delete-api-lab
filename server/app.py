#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

# @app.route('/bakeries/<int:id>')
# def bakery_by_id(id):

#     bakery = Bakery.query.filter_by(id=id).first()
#     bakery_serialized = bakery.to_dict()

#     response = make_response(
#         bakery_serialized,
#         200
#     )
#     return response




@app.route('/bakeries/<int:id>', methods = ['GET', 'PATCH'])
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()

    if request.method == 'GET':
        bakery_serialized = bakery.to_dict()

        response = make_response(
            bakery_serialized,
            200
        )
        return response
    
    elif request.method == 'PATCH':
        bakery = Bakery.query.filter(Bakery.id == id).first()

        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))

        db.session.add(bakery)
        db.session.commit()

        bakery_dict = bakery.to_dict()

        response = make_response(
            bakery_dict,
            200
        )

        return response





@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response


@app.route('/baked_goods', methods = ['GET', 'POST'])
def post_baked_goods():
    if request.method == 'GET':
        bakeries = []
        for bake in BakedGood.query.all():
            bake_dict = bake.to_dict()
            bakeries.append(bake_dict)
        
        response = make_response(
            bakeries,
            200
        )
        return response
    
    elif request.method == 'POST':
        new_bake = BakedGood(
            name = request.form.get("name"),
            price = request.form.get("price"),
            created_at = request.form.get("created_at"),
            updated_at = request.form.get("updated_at"),
            bakery_id = request.form.get("bakery_id"),
        )

        db.session.add(new_bake)
        db.session.commit()

        bake_dict = new_bake.to_dict()

        response = make_response(
            bake_dict,
            201
        )
        return response
    
@app.route('/baked_goods/<int:id>', methods = ['GET', 'DELETE'])
def delete_baked_goods(id):
    baked_goods = BakedGood.query.filter(BakedGood.id == id).first()

    if request.method == 'GET':
        baked_goods_dicts = baked_goods.to_dict()

        response = make_response(
            baked_goods_dicts,
            200
        )
        return response 
    
    elif request.method == 'DELETE':
        db.session.delete(baked_goods)
        db.session.commit()

        response_body = {
            "delete_successful" : True,
            "message" : "Review deleted."
        }

        response = make_response(
            response_body,
            200
        )
        return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
