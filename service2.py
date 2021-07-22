from flask import Flask,jsonify,abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from dataclasses import dataclass
from flask_migrate import Migrate
from producer import publish

import json,os
import requests
app= Flask(__name__)
file_path = os.path.abspath(os.getcwd())+"\database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path
db = SQLAlchemy(app)
migrate = Migrate(app,db)
CORS(app)


@dataclass
class Product(db.Model):
    #__tablename__ = "Product_details"
    id:int
    title:str
    image:str
    id=db.Column(db.Integer,primary_key=True,autoincrement=False)
    title=db.Column(db.String(200))
    image=db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    #__tablename__ = "User_details"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    product_id=db.Column(db.Integer)

    UniqueConstraint('user_id,product_id',name='user_product_unique')

@app.route('/api/products')
def index():
    return jsonify(Product.query.all())

#Making internal connection
@app.route('/api/products/<int:id>/like',methods=['POST'])
def like(id):
    req=requests.get('http://127.0.0.1:8000/api/user')

    json=req.json()
    print(json)
    try:
      productUser=ProductUser(user_id=json['id'],product_id=id)
      print(productUser)
      db.session.add(productUser)
      db.session.commit()
      publish('product liker', id)
    except:
        abort(400,'Your already like th image')


    # return jsonify(req.json())
    return jsonify({
         'message':'success'
    })

if __name__ =='__main__':
    app.run(debug=True,host='0.0.0.0')