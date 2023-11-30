import requests
import streamlit as st
from .utils import validate_cuil
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("BASE_URL_API")

def actualizar_directivas():

    with st.form('Actualizar Contrato'):
        cuil = st.text_input('CUIL *', placeholder='Ingrese el CUIL')
        contract = st.file_uploader('Cargar archivo pdf *', type=['pdf'])
        submit_button = st.form_submit_button(label='Enviar')

        if submit_button:
            if not validate_cuil(cuil):
                st.error('El CUIL ingresado no es válido')
            if not contract:
                st.error('Debe cargar un archivo PDF')

    if cuil and contract:
        headers = {
            'Authorization': 'Bearer ' + st.session_state['access_token']
        }

        url = f"{API_URL}/contract/{cuil}"
        response = requests.put(url, files={'contract': contract}, headers=headers)

        if response:
            data = response.json()
            if response.status_code == 200:
                st.info(data.get('message'))
                st.stop()
            else:
                st.error(data.get('error'))
                st.stop()
        else:
            st.error('Algo salió mal al enviar el pdf.')
            st.stop()