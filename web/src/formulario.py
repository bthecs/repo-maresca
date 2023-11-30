import io
from pathlib import Path
import streamlit as st
import base64
from fpdf import FPDF
from datetime import datetime


# --- PATH SETTINGS ---
current_dir: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file: Path = current_dir / "styles/.css"

ROLE_OPTIONS: list[str] = [
    "Abogado",
    "Medico",
    "Escribano",
    "Psicologo",
    "Psiquiatra"
]

# --- FUNCTIONS ---
def generate_pdf(html_content: list):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf_output = io.BytesIO()
    for content in html_content:
        pdf.multi_cell(0, 10, txt=content, align="L")
    
    pdf.output(pdf_output)

    pdf_bytes = pdf_output.getvalue()  # Obtiene los bytes del archivo en memoria

    return pdf_bytes 


def displayPDF(pdf):

    pdf_data = base64.b64encode(pdf).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_data}" width="100%" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def formulario():
    # --- CONTENT ---
    st.title("🧰 Formulario")

    st.markdown("""Bienvenido al Formulario de Directivas Anticipadas. Las Directivas Anticipadas son un medio para 
    expresar tus preferencias y deseos sobre la atención médica que deseas recibir en el futuro. Este formulario te 
    brinda la oportunidad de tomar el control de tu atención médica y asegurarte de que tus valores y deseos sean 
    respetados, incluso cuando no puedas comunicarlos personalmente.""")

    html_content = []

    day = datetime.now().strftime("%d")
    month = datetime.now().strftime("%m")
    year = datetime.now().strftime("%Y")

    st.subheader("Información Personal")
    c1, c2 = st.columns(2)

    with c1:
        name = st.text_input("Nombre", placeholder="Ana")
        lastname = st.text_input("Apellido", placeholder="Perez")
        dni = st.text_input("DNI", placeholder="12.345.678")
        cuil = st.text_input("CUIL", placeholder="20-34567890-1")
        birthdate = st.text_input("Fecha de Nacimiento", placeholder=f"{day}/{month}/{year}")
        mail = st.text_input("Email", placeholder="k6t9B@example.com")

    with c2:
        nationality = st.text_input("Nacionalidad", placeholder="Argentino")
        province = st.text_input("Provincia", placeholder="Mendoza")
        locality = st.text_input("Localidad", placeholder="San Rafael")
        phone = st.text_input("Teléfono", placeholder="2604123456")
        phone_optional = st.text_input("Teléfono Opcional", placeholder="")

    c3, c4 = st.columns(2)
    with c3:
        gender = st.radio("Género", ("Mujer", "Hombre", "No Definido"))
    with c4:
        marital_status = st.radio("Estado Civil", ("Casado", "Soltero", "Viudo"))

    st.divider()

    st.subheader("Información Profesional")
    professional_name = st.text_input("Nombre del Profesional", placeholder="Juan")
    professional_dni = st.text_input("DNI del Profesional", placeholder="46.345.678")
    professional_cuil = st.text_input("CUIL del Profesional", placeholder="20-34567890-1")
    professional_license = st.text_input("Matricula del Profesional", placeholder="")
    professional_role = st.selectbox(label="Rol del Profesional", key="role", options=ROLE_OPTIONS)

    st.subheader("Representantes")
    amount_representatives = st.number_input("Cantidad de Representantes", min_value=0, step=1)

    representatives = []
    for i in range(amount_representatives):
        st.subheader(f"Representante {i + 1}")
        name_representative = st.text_input(f"Nombre del Representante {i + 1}", placeholder="Ruben")
        lastname_representative = st.text_input(f"Apellido del Representante {i + 1}", placeholder="Diaz")
        dni_representative = st.text_input(f"DNI del Representante {i + 1}", placeholder="12345678")
        representatives.append({
            "name": name_representative,
            "lastname": lastname_representative,
            "dni": dni_representative
        })

    st.subheader("Directivas")
    directives = st.text_area("Agregue sus directivas ...", placeholder="Escriba aquí sus directivas")

    if st.button("Enviar"):
        html_content.append(
            f"En la Ciudad de {locality}, Provincia de {province} a los {day} días del mes de {month} del año {year}, Yo, {name} {lastname}, D.N.I. N° {dni}, de nacionalidad {nationality}, de estado civil {marital_status}, degénero {gender}, y contacto con el correo {mail}, Tel.: {phone}, Tel. opc.: {phone_optional}, obrando en pleno uso y goce de mis facultades mentales, actuando con plena intención, discernimiento y libertad en los términos del Art. 260 del Código Civil y Comercial de la Nación y sin que me afecten los posibles vicios de error, dolo o fuerza, Arts. 265, 271 y 276 y concordantes del Código Civil y Comercial de la Nación, sin tener información de padecer enfermedad crónica ni aguda de ninguna naturaleza que pueda afectar mi juicio crítico, formalmente expreso y establezco, en uso de las facultades reconocidas por los Art. 60; 59 inc. g del Código Civil y Comercial de la Nación y las que resultan de la Ley 26.529 y Decreto Reglamentario N° 1089/12, estas DIRECTIVAS ANTICIPADAS y DESIGNACIÓN DE UN PREPRESENTANTE PARA LA ATENCIÓN MÉDICA, para el supuesto de encontrarme comprendido en alguna de las situaciones que describo a título ilustrativo o cualquiera similar aún no detallada en estas directivas.\nDirectivas Anticipadas:\n{directives}")
        st.success("Formulario enviado con éxito.")
        pdf = generate_pdf(html_content)
        st.markdown("---")
        st.markdown("## Visualizar PDF")
        displayPDF(pdf)

        if st.download_button("Descargar PDF", data=pdf, file_name="directivas.pdf"):
            st.success("PDF descargado")