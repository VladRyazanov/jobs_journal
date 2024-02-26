from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.users import User
from data.reqparse import parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"user {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict()})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'user': [user.to_dict(user) for user in users]})

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == args["email"]).first():
            return jsonify({'error': 'user already exists'})

        user = User(
            email=args["email"],
            surname=args["surname"],
            name=args["name"],
            age=args["age"],
            position=args["position"],
            speciality=args["speciality"],
            address=args["address"]
        )
        user.set_password(args["password"])
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})
