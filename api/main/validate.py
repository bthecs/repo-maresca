import re, requests


def validate(data, regex):
    """Custom Validator"""
    return True if re.match(regex, data) else False


def validate_password(password: str):
    """Password Validator"""
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    return validate(password, reg)


def validate_cuil(cuil: str):
    """Cuil Validator"""
    reg = r"^(20|2[3-7]|30|3[3-4])(-)[0-9]{8}(-)[0-9]$"
    return validate(cuil, reg)


def validate_user(**args):
    """User Validator"""
    # Validate required fields
    if not args.get("cuil") or \
            not args.get("password") or \
            not args.get("name"):
        return {
            "cuil": "El Cuil es requerido",
            "password": "La Contraseña es requerida",
            "name": "El Nombre es requerido",
        }
    # Validate types
    if not isinstance(args.get("cuil"), str) or \
            not isinstance(args.get("password"), str) or \
            not isinstance(args.get("name"), str):
        return {
            "cuil": "El Cuil debe ser una cadenas de caracteres",
            "password": "La Contraseña debe ser una cadenas de caracteres",
            "name": "El Nombre debe ser una cadenas de caracteres",
        }
    # Validate cuil
    if not validate_cuil(args.get("cuil")):
        return {
            "cuil": "El Cuil es invalido"
        }
    # Validate password
    if not validate_password(args.get("password")):
        return {
            "password": "La Contraseña es invalida, debe tener al menos 8 caracteres con letras mayúsculas y "
                        "minúsculas, números y caracteres especiales"
        }
    # Validate name
    if not 2 <= len(args['name'].split(' ')) <= 30:
        return {
            "name": "El Nombre debe tener entre 2 y 30 palabras"
        }
    return True


def validate_cuil_and_password(cuil, password):
    """Cuil and Password Validator"""
    if not (cuil and password):
        return {
            "cuil": "El Cuil es requerido",
            "password": "La Contraseña es requerida"
        }
    if not validate_cuil(cuil):
        return {
            "cuil": "Cuil es invalido"
        }
    if not validate_password(password):
        return {
            "password": "La Contraseña es invalida, debe tener al menos 8 caracteres con letras mayúsculas y "
                        "minúsculas, números y caracteres especiales"
        }
    return True


def validate_contract(contract = None):
    """Check signature"""

    if contract is None:
        raise ValueError("El contrato no se proporcionó correctamente.")
    try:
        url = "https://drp2cj.pjm.gob.ar/ms-pdfcheck/api/v1/upload"

        contract.seek(0)
        contract_content = contract.read()

        files = {'file': (contract.name, contract_content, 'application/pdf')}
        result = requests.post(url, files=files).json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error durante la verificación del contrato: {str(e)}")

    if result['verificationResult']['result'] != 'VALID':
        raise Exception(result['verificationResult']['message'])
    return True
