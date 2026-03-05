"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object (ESTO ES BÁSICAMENTE LO QUE HACE QUE EL NOMBRE DE JACKSON_FAMILY TRAIGA LA ESTRUCTURA)
jackson_family = FamilyStructure("Pepito")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    # This is how you can use the Family datastructure by calling its methods
   return jsonify(jackson_family.get_all_members()), 200

@app.route('/members/<int:memb_id>', methods=['GET'])
def get_member(memb_id):
  
    member = jackson_family.get_member(memb_id)

    if member:
         return jsonify(member), 200
    return jsonify({"erro":"Member not found"}), 404

@app.route('/members', methods=['POST'])
def create():
     data = request.get_json()
     required_fields = ["first_name","lucky_numbers","age"]
     missing = [field for field in required_fields if field not in data]
     if missing:
       return jsonify({"error": f"Missing fields: {missing}"})
     new_member = jackson_family.add_member(data)
     return jsonify(new_member), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete(id):

    deleted = jackson_family.delete_member(id)

    if deleted:
        return jsonify({"done": True}), 200

    return jsonify({"done": False}), 404

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
