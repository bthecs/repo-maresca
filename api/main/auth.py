from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify, abort


def professional_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims["is_professional"]:
            abort(403, description="Permission denied. Professional access required.")
        return fn(*args, **kwargs)
    return decorated
