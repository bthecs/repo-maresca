import streamlit as st
import requests
import base64
from .utils import validate_cuil
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("BASE_URL_API")

def visualizador():
    st.title('Visualizador de PDF')

    with st.form('Visualizar Contrato'):
        cuil = st.text_input('Ingrese el CUIL de la persona')
        submit_button = st.form_submit_button(label='Enviar')
        if submit_button:
            if not validate_cuil(cuil):
                st.error('El CUIL ingresado no es válido')

    if cuil:
        url = f"{API_URL}/contract/{cuil}"
        headers = {
            'Authorization': 'Bearer ' + st.session_state['access_token']
        }
        """
        progress_text = "Operacion en progreso. Por favor espere..."
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(100):
            response = requests.get(url, headers=headers)
            my_bar.progress(percent_complete + 1, text=progress_text)
        """
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            pdf_data = base64.b64encode(response.content).decode("utf-8")
            pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_data}" width="100%" height="1000" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.error('Contrato no encontrado')

        