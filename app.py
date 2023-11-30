import requests
import streamlit as st
from streamlit_option_menu import option_menu
from src import home, visualizador, cargar_directivas, formulario, actualizar_directivas
from src.auth import Authentication, is_authenticated, get_claims


def main_navbar():
    """
    Creates the logout widget
    """
    selected_option = None
    main_page_sidebar = st.sidebar.empty()
    if st.session_state['LOGGED_IN'] == True:
        claims = get_claims()
        st.markdown(f"Claims: {claims}" if claims else "Claims: None")
        if claims.get("is_professional") == True:
            selected_option = option_menu(
                menu_title="Menu",
                menu_icon='list-columns-reverse',
                icons=["🏠", "🧰", "✍️", "🔄", "🔎"],
                options=["Inicio", "Formulario", "Cargar Directivas", "Actualizar Directivas", "Visualizar Directivas"],
                orientation="horizontal"
            )
        else:
            selected_option = option_menu(
                menu_title="Menu",
                menu_icon='list-columns-reverse',
                icons=["🏠", "🔎"],
                options=["Inicio", "Visualizar Directivas"],
                orientation="horizontal"
            )
        with main_page_sidebar:
            st.sidebar.markdown("---")
            st.sidebar.markdown("Bienvenido al sistema de gestión de directivas anticipadas!")
            st.sidebar.markdown("- En la página de `Inicio`, podrá encontrar información sobre el sistema.")
            st.sidebar.markdown("- En la página de `Formulario`, podrá completar el formulario de directivas anticipadas.")
            st.sidebar.markdown("- En la página de `Cargar Directivas`, podrá cargar un archivo PDF con las directivas anticipadas.")
            st.sidebar.markdown("- En la página de `Actualizar Directivas`, podrá actualizar las directivas anticipadas de una persona.")
            st.sidebar.markdown("- En la página de `Visualizar Directivas`, podrá visualizar las directivas anticipadas de una persona.")
            logout_click_check = main_page_sidebar.button("Cerrar Sesión")

            if logout_click_check == True:
                st.session_state['LOGOUT_BUTTON_HIT'] = True
                st.session_state['LOGGED_IN'] = False
                st.session_state['access_token'] = None
                main_page_sidebar.empty()
                st.experimental_rerun()

    return main_page_sidebar, selected_option

login_ui = Authentication()
LOGGED_IN = login_ui.build_login_ui()


if LOGGED_IN == True:
    main_page_sidebar, selected_option = main_navbar()

    if selected_option == "Inicio":
        home.home()
    elif selected_option == "Formulario":
        formulario.formulario()
    elif selected_option == "Cargar Directivas":
        cargar_directivas.cargar_directivas()
    elif selected_option == "Actualizar Directivas":
        actualizar_directivas.actualizar_directivas()
    elif selected_option == "Visualizar Directivas":
        visualizador.visualizador()

    if st.session_state['LOGGED_IN'] == False:
        main_page_sidebar.empty()
