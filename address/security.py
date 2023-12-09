from flask import request, current_app, Response
from functools import wraps
from bson.json_util import dumps
from .db import UserDB
import jwt

userdb = UserDB()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        if not token:
            return Response(dumps({"error": "Authorization token is missing"}),
                            mimetype='application/json',
                            status=401)
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['user_id']
            user = userdb.get_user(current_user_id)
            if user is None:
                return Response(dumps({"error": "Invalid payload entered or user does not exist"}),
                                mimetype='application/json',
                                status=401)

        except Exception:
            return Response(dumps({"error": "Authorization token is invalid"}),
                            mimetype='application/json',
                            status=401)
        return f(*args, **kwargs)
    return decorated
