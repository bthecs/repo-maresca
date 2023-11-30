import re
import streamlit as st


def validate(data, regex):
    """Custom Validator"""
    return True if re.match(regex, data) else False


def validate_password(password: str):
    """Password Validator"""
    if not password and not isinstance(password, str):
        return False
    reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    return validate(password, reg)


def validate_cuil(cuil: str):
    """Cuil Validator"""
    if not cuil and not isinstance(cuil, str):
        return False
    reg = r"^(20|2[3-7]|30|3[3-4])(-)[0-9]{8}(-)[0-9]$"
    return validate(cuil, reg)


def validate_matricle(matricle: str):
    """Matricle Validator"""
    if not matricle and not isinstance(matricle, str):
        return False
    reg = r"^[0-9]{6,10}$"
    return validate(matricle, reg)


def validate_name(name: str):
    """Name Validator"""
    if not name and not isinstance(name, str):
        return False
    if not 2 <= len(name.split(' ')) <= 30:
        return False
    return True


def validate_register(name, cuil, password, password_confirm, matricle):
    """
    Validates the registration data.
    Returns True if the data is valid, False otherwise.
    """
    if not validate_name(name):
        st.error("Por favor, ingrese un nombre válido!")
        return False
    elif not validate_cuil(cuil):
        st.error("Por favor, ingrese un CUIL válido!")
        return False
    elif not validate_password(password):
        st.error(
            "La Contraseña es inválida, debe tener al menos 8 caracteres con letras mayúsculas y minúsculas, números y caracteres especiales")
        return False
    elif password != password_confirm:
        st.error("Las contraseñas no coinciden!")
        return False
    elif matricle is not None and not validate_matricle(matricle):
        st.error("Por favor, ingrese una matrícula válida!")
        return False
    else:
        return True
