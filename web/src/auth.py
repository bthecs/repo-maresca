from functools import wraps
import os
import requests
import streamlit as st
from streamlit_option_menu import option_menu
from .utils import validate_register
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("BASE_URL_API")

def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if is_authenticated():
            return fn(*args, **kwargs)
        else:
            st.error(f'{fn.__name__} requires authentication!')

    return wrapper


def is_authenticated():
    if "access_token" not in st.session_state:
        st.session_state["access_token"] = None

    token = st.session_state["access_token"]
    if token is not None:
        response = requests.get(f"{API_URL}/check_token", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            return True
    return False


@auth_required
def get_claims() -> dict:
    """
    Decodes the token and returns the claims.
    """
    token = st.session_state["access_token"]
    if token is not None:
        response = requests.get(f"{API_URL}/check_token", headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            return response.json().get("data")


class Authentication:
    def __init__(self):
        pass
    

    def login_widget(self) -> None:
        """
        Creates the login widget, checks and sets cookies, authenticates the users.
        """

        # Checks if cookie exists.
        if st.session_state['LOGGED_IN'] == False:
            if st.session_state['LOGOUT_BUTTON_HIT'] == False:
                if "access_token" in st.session_state:
                    if st.session_state["access_token"] is not None:
                        st.session_state['LOGGED_IN'] = True

        if st.session_state['LOGGED_IN'] == False:
            st.session_state['LOGOUT_BUTTON_HIT'] = False

            del_login = st.empty()
            with del_login.form("Iniciar Sesión"):
                cuil = st.text_input("CUIL", placeholder='Ingrese su CUIL')
                password = st.text_input("Password", placeholder='Ingrese su Contraseña', type='password')

                st.markdown("###")
                login_submit_button = st.form_submit_button(label='Iniciar Sesión')

                if login_submit_button:
                    # Llamar a la API para la autenticación
                    auth_data = {"cuil": cuil, "password": password}
                    response = requests.post(f"{API_URL}/login", json=auth_data)
                    if response.status_code == 200:
                        st.session_state['LOGGED_IN'] = True
                        st.session_state["access_token"] = response.json().get("data").get("access_token")
                        # Set access_token on cookies
                        # response.set_cookie("access_token", response.json().get("data").get("access_token"))
                        del_login.empty()
                        st.experimental_rerun()
                    else:
                        st.error(response.json().get("message"))
    

    def sign_up_widget(self) -> None:
        """
        Creates the sign-up widget and stores the user info in a secure way in the _secret_auth_.json file.
        """
        with st.form("Sign Up Form"):
            name = st.text_input("Name *", placeholder='Nombre y Apellido')
            cuil = st.text_input("CUIL *", placeholder='CUIL')
            password = st.text_input("Password *", placeholder='Contraseña', type='password')
            password_confirm = st.text_input("Confirm Password *", placeholder='Confirmar contraseña', type='password')
            matricle = st.text_input("Matricle (Opcional)", placeholder='Matricula')
            matricle = None if matricle == "" else matricle

            st.markdown("###")
            sign_up_submit_button = st.form_submit_button(label='Registrar')

            if sign_up_submit_button == True:
                is_validated = validate_register(name, cuil, password, password_confirm, matricle)
                if is_validated:

                    # Llamar a la API para el registro
                    register_data = {
                        "name": name,
                        "cuil": cuil,
                        "password": password,
                        "matricle": matricle,
                        "is_professional": False if matricle is None else True
                    }

                    response = requests.post(f"{API_URL}/register", json=register_data)

                    if response.status_code == 201:
                        st.success(response.json().get("message"))
                        st.stop()

                    else:
                        st.error(response.json().get("message"))
                        st.stop()
                else:
                    st.error("Por favor, complete todos los campos obligatorios!")
                    st.stop()

    def nav_sidebar(self):
        """
        Creates the side navigaton bar
        """
        main_page_sidebar = st.sidebar.empty()
        with main_page_sidebar:
            selected_option = option_menu(
                menu_title="Navigation",
                menu_icon='list-columns-reverse',
                icons=['box-arrow-in-right', 'person-plus'],
                options=['Iniciar Sesión', 'Crear una cuenta'],
            )
        return main_page_sidebar, selected_option

    def build_login_ui(self):
        """
        Brings everything together, calls important functions.
        """
        if 'LOGGED_IN' not in st.session_state:
            st.session_state['LOGGED_IN'] = False

        if 'LOGOUT_BUTTON_HIT' not in st.session_state:
            st.session_state['LOGOUT_BUTTON_HIT'] = False

        main_page_sidebar, selected_option = self.nav_sidebar()

        if selected_option == 'Iniciar Sesión':
            self.login_widget()

        elif selected_option == 'Crear una cuenta':
            self.sign_up_widget()

        if st.session_state['LOGGED_IN'] == True:
            main_page_sidebar.empty()

        return st.session_state['LOGGED_IN']


"""
def register():
    # create registeration form
    st.title("Formulario de Registro")

    # Add input fields for name, email, and password
    cuil = st.text_input("Cuil")
    password = st.text_input("Password", type="password")
    matricula = st.text_input("Matricula")

    # Add a submit button
    if st.button("Register"):
        # Validate input and register user
        if cuil and password:
            url = 'https://informes.nosis.com/Home/Buscar'
            data = {
                'Texto': cuil,
                'Tipo': '-1',
                'EdadDesde': '-1',
                'EdadHasta': '-1',
                'IdProvincia': '-1',
                'Localidad': '',
                'recaptcha_response_field': 'enganio al captcha',
                'recaptcha_challenge_field': 'enganio al captcha',
                'encodedResponse': '',
            }
            response = requests.post(url, data=data)

            data = response.json()

            st.write("Nombre:", data['EntidadesEncontradas'][0]['RazonSocial'])
            st.write("CUIL:", data['EntidadesEncontradas'][0]['Documento'])
            st.write("Provincia:", data['EntidadesEncontradas'][0]['Provincia'])

            url_register = "http://127.0.0.1:6000/register_user"

            register = {
                'cuil': cuil,
                'password': password,
                'matricula': matricula
            }

            response = requests.post(url_register, json=register)

            if response.status_code == 201:
                st.success(response.text)
            else:
                st.error(response.text)

        else:
            st.error("Please fill in all fields")
"""
