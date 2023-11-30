import base64
import io

from flask import Blueprint, jsonify, request
from flask import send_file
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt
from flask_cors import cross_origin

from .auth import professional_required
from .models import User, Contract
from .validate import validate_user, validate_cuil_and_password, validate_cuil, validate_contract

main = Blueprint('main', __name__)


@main.route("/")
def hello():
    return "Hello World!"


@main.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        # Validar los datos
        if not data:
            return {
                "message": "Por favor, ingrese los datos del usuario.",
                "data": None,
                "error": "Bad request"
            }, 400
        # Validar los datos del usuario
        is_validated = validate_cuil_and_password(data.get("cuil"), data.get("password"))
        if is_validated is not True:
            return dict(
                message="Los datos son invalidos.",
                data=None,
                error=is_validated
            ), 400
        # Iniciar sesión
        user = User().login(data.get("cuil"), data.get("password"))
        if user:
            try:
                access_token = create_access_token(
                    identity=user["cuil"],
                    additional_claims={"is_professional": user["is_professional"]})
                return {
                    "message": "Inicio de sesión exitoso!",
                    "data": {
                        "access_token": access_token,
                        "user": user
                    }
                }, 200
            except Exception as e:
                return {
                    "message": "Algo salio mal.",
                    "error": str(e),
                    "data": None
                }, 500
        else:
            return {
                "message": "Error al iniciar sesión.",
                "data": None,
                "error": "Unauthorized"
            }, 404

    except Exception as e:
        return {
            "message": "Algo salio mal.",
            "error": str(e),
            "data": None
        }, 500


@main.route("/register", methods=["POST"])
def register():
    try:
        user = request.json
        # Validar los datos
        if not user:
            return {
                "message": "Por favor, ingrese los datos del usuario.",
                "data": None,
                "error": "Bad request"
            }, 400

        # Validar los datos del usuario
        is_validated = validate_user(**user)
        if is_validated is not True:
            return dict(
                message="Los datos son invalidos.",
                data=None,
                error=is_validated
            ), 400

        # Crea el usuario
        user = User().create(**user)
        if not user:
            return {
                "message": "El usuario ya existe.",
                "data": None,
                "error": "Conflict"
            }, 409
        return {
            "message": "El usuario fue creado exitosamente!",
            "data": user
        }, 201

    except Exception as e:
        return {
            "message": "Algo salio mal.",
            "error": str(e),
            "data": None
        }, 500

@main.route("/check_token", methods=["GET"])
@jwt_required()
def check_token():
    try:
        # Obtén la identidad del token
        verify_jwt_in_request()
        claims = get_jwt()

        return {
            "message": "El token es valido.",
            "data": {"cuil": claims.get("sub"), "is_professional": claims.get("is_professional")},
        }, 200

    except Exception as e:
        return jsonify({
            "message": "Algo salió mal al decodificar el token.",
            "error": str(e),
            "data": None
        }), 500


@main.route('/contract', methods=['POST'])
@professional_required
def upload_contract():
    try:
        # Validar el cuil
        is_validated = validate_cuil(request.form.get("cuil"))
        if is_validated is not True:
            return {
                "message": "Los datos son invalidos.",
                "data": None,
                "error": {"cuil": "El Cuil es invalido"}
            }, 400
        # Validar el contrato
        if "contract" not in request.files:
            return {
                "message": "Por favor, adjunte el contrato.",
                "data": None,
                "error": "Bad request"
            }, 400

        # Validar la firma del contrato
        is_validated = validate_contract(request.files["contract"])
        if is_validated is not True:
            return {
                "message": "Los datos son invalidos.",
                "data": None,
                "error": is_validated
            }, 400

        # Crea el contrato
        contract = Contract().create(request.form["cuil"], request.files["contract"])
        if not contract:
            return {
                "message": "El contrato ya existe.",
                "data": None,
                "error": "Conflict"
            }, 409
        return {
            "message": "El contrato fue creado exitosamente!",
            "data": contract
        }, 201

    except Exception as e:
        return {
            "message": "Algo salio mal.",
            "error": str(e),
            "data": None
        }, 500


@main.route('/contract/<cuil>', methods=['GET'])
@jwt_required()
def get_contract(cuil):
    try:
        # Get the user by cuil
        user = User().get_by_cuil(get_jwt_identity())
        if not user.get("is_professional") and cuil != user.get("cuil"):
            return {
                "message": "No tienes permisos para ver este contrato.",
                "data": None,
                "error": "Forbidden"
            }, 403

        contract = Contract().get_by_cuil(cuil)

        if not contract:
            return {
                "message": "Contrato no encontrado para el cuil proporcionado.",
                "data": None,
                "error": "Not Found"
            }, 404

        # Decodificar el contenido base64
        decoded_content = base64.b64decode(contract["contract"])

        # Devolver el archivo como respuesta
        return send_file(
            io.BytesIO(decoded_content),
            as_attachment=True,
            download_name=f"contrato_{cuil}.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return {
            "message": "Algo salió mal.",
            "error": str(e),
            "data": None
        }, 500


@main.route('/contract/<cuil>', methods=['PUT'])
@professional_required
def update_contract(cuil):
    try:
        # Validar que el contrato exista
        existing_contract = Contract().get_by_cuil(cuil)
        if not existing_contract:
            return {
                "message": "El contrato no existe para ese cuil.",
                "data": None,
                "error": "Not Found"
            }, 404

        # Validar la firma del contrato
        is_validated = validate_contract(request.files["contract"])
        if is_validated is not True:
            return {
                "message": "Los datos son invalidos.",
                "data": None,
                "error": is_validated
            }, 400

        # Actualizar el contrato
        updated_contract = Contract().update(cuil, request.files["contract"])

        return {
            "message": "Contrato actualizado exitosamente!",
            "data": updated_contract
        }, 200

    except Exception as e:
        return {
            "message": "Algo salió mal.",
            "error": str(e),
            "data": None
        }, 500



@main.errorhandler(403)
def forbidden(e):
    return jsonify({
        "message": "Forbidden",
        "error": str(e),
        "data": None
    }), 403


@main.errorhandler(404)
def forbidden(e):
    return jsonify({
        "message": "Endpoint Not Found",
        "error": str(e),
        "data": None
    }), 404
