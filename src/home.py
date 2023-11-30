import streamlit as st

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "Inicio"
PAGE_ICON: str = "🏠"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)


def home():
    st.markdown("""
    # Directivas Anticipadas
    
    Las Directivas Anticipadas, también conocidas como "Testamento Vital" o "Instrucciones Previas", 
    son un documento legal que permite a una persona expresar sus preferencias y deseos con respecto a su 
    atención médica futura en situaciones en las que puedan estar incapacitadas o no puedan comunicar sus deseos. 
    Estas directivas permiten a los individuos tomar decisiones informadas sobre el tratamiento médico que desean 
    recibir, garantizando que sus valores y preferencias sean respetados.
    
    ### ¿Por qué son importantes las Directivas Anticipadas?
    
    - Autonomía del paciente: Las Directivas Anticipadas permiten a las personas tomar decisiones sobre su propia 
    atención médica y mantener el control de su salud, incluso cuando no pueden comunicarse.
    
    - Evitar conflictos familiares: Ayudan a prevenir conflictos familiares al establecer claramente los deseos 
    del paciente, lo que facilita a los familiares y médicos tomar decisiones en su nombre.
    
    - Garantizar atención personalizada: Permite que la atención médica sea más personalizada y acorde a los 
    valores y deseos del paciente, en lugar de decisiones genéricas.
    
    ### Contenido de las Directivas Anticipadas
    
    El contenido de las Directivas Anticipadas puede variar, pero generalmente incluye:
    
    - Nombramiento de un apoderado de atención médica: La designación de una persona de confianza para tomar 
    decisiones médicas en nombre del paciente si no puede hacerlo.
    
    - Instrucciones específicas: Preferencias detalladas sobre el tratamiento médico, como la aceptación o 
    rechazo de procedimientos médicos específicos, resucitación cardiopulmonar (RCP), alimentación por tubo, etc.
    
    - Deseos de cuidados paliativos: Indicaciones sobre cuidados paliativos y calidad de vida en situaciones 
    terminales.
    
    - Consideraciones religiosas o éticas: Si el paciente tiene creencias religiosas o éticas específicas que 
    deben respetarse en su atención médica.
    
    ### Legalidad de las Directivas Anticipadas
    
    Las Directivas Anticipadas son legalmente vinculantes en muchos países y estados. Sin embargo, las leyes 
    varían, por lo que es importante verificar la legislación específica en tu área. A menudo, se requiere que el 
    documento se firme y testifique de acuerdo con las leyes locales para ser legalmente válido.
    
    ### Cómo Utilizar las Directivas Anticipadas
    
    1. Habla con un profesional de la salud o abogado: Obtén asesoramiento sobre las leyes locales y cómo 
    redactar tus Directivas Anticipadas.
    
    2. Documenta tus preferencias: Completa el documento de Directivas Anticipadas, incluyendo instrucciones 
    específicas y nombramiento de un apoderado de atención médica si lo deseas.
    
    3. Distribuye copias: Asegúrate de que tu médico y las personas de confianza tengan copias de tus Directivas 
    Anticipadas.
    
    4. Revisa y actualiza: Revisa regularmente tus Directivas Anticipadas y ajústalas según sea necesario para 
    reflejar tus deseos actuales.
    
    Las Directivas Anticipadas son una herramienta importante para tomar el control de tu atención médica y 
    asegurarte de que tus preferencias sean respetadas, incluso en situaciones difíciles.""")
