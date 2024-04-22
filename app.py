from flask import Flask,jsonify,request
from models import Contact
from config import app,db



@app.route('/contacts',methods=['GET'])
def get_contacts():
    contacts=Contact.query.all()
    json_contact= list(map(lambda x:x.to_jsons(),contacts))
    return jsonify({'contacts':json_contact})


@app.route('/contacts',methods=['POST'])
def create_contact():
    first_name=request.json['contact']['firstName']
    last_name=request.json['contact']['lastName']
    email=request.json['contact']['email']

    if not first_name or not last_name or not email: return jsonify({'error':'All fields are required.'}) ,400
    
    new_contact=Contact(firstName=first_name,lastName=last_name,email=email)
    try: 
        db.session.add(new_contact)
        db.commit()
    except Exception as e:
        return jsonify({'error':'Something went wrong.'}) ,400    

    return jsonify({'contact':new_contact}) ,201


@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "Usr updated."}), 200


@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    
    
    app.run(debug = True)