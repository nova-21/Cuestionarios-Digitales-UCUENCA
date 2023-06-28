import time

import streamlit as st
from PIL import Image

from questionnaires.questionnaires_views import show_BDI, show_BAI
from data.actions.patient_actions import get_patient
from data.actions.questionnaire_response_actions import get_pending_questionnaire_responses
from data.conection import create_engine_conection


from tools.time_utilities import get_today

if 'num' not in st.session_state:
    st.session_state.num = 0
if 'contador' not in st.session_state:
    st.session_state.contador = 0
if 'answers_copy' not in st.session_state:
    st.session_state.answers_copy = {}
if 'patient_id' not in st.session_state:
    st.session_state.patient_id = ""
if 'current_patient' not in st.session_state:
    st.session_state.current_patient = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = "Inicio"

general_container = st.empty()

def clean():
    membrete = st.empty()
    membrete.empty()
    with membrete.container():
        img = Image.open("ucuenca.png")
        st.image(img, width=200)
        st.header("Departamento de Bienestar Universitario")
        st.header("Sistema de encuestas psicológicas")

def start():
    with general_container:
        patient_search_form = st.form(key="pacienteBuscar")
        with patient_search_form:
            clean()
            patient_id = st.text_input("Ingrese su cédula:")
            submit = st.form_submit_button("Aceptar")
        if submit:
            patient = get_patient(db_engine=create_engine_conection(), patient_id=patient_id)
            today_str = get_today()
            if patient is not None:
                pending_questionnaires = get_pending_questionnaire_responses(create_engine_conection(), today_str, patient.id)
                if patient.id == patient_id and len(pending_questionnaires)>0:
                    st.session_state.current_patient = patient
                    st.session_state.current_view = "Seleccionar"
                else:
                    st.success("No tiene cuestionarios pendientes de realizar")
                    time.sleep(2)
                    st.experimental_rerun()
            else:
                st.success("No tiene cuestionarios pendientes de realizar")
                time.sleep(2)
                st.experimental_rerun()


def select_questionnaire():
    today_str = get_today()
    pending_questionnaires = get_pending_questionnaire_responses(create_engine_conection(), today_str, st.session_state.current_patient.id)
    if len(pending_questionnaires) > 0:
        with general_container:
            test_selection_form = st.form(key="testSeleccionado")
            with test_selection_form:
                clean()
                patient = st.session_state.current_patient
                st.subheader("Bienvenido " + patient.first_name + " " + patient.first_family_name)
                st.write("Tiene " + str(len(pending_questionnaires)) + " tests pendientes por realizar")
                options_dict = {"Seleccionar": 0}
                for questionnaire in pending_questionnaires:
                    options_dict[questionnaire[1]] = questionnaire[0].id
                questionnaire_selected = st.selectbox("Seleccione el test a realizar", options_dict.keys())
                submit = st.form_submit_button("Aceptar")
            if submit:
                st.session_state.current_questionnaire = options_dict.get(questionnaire_selected)
                st.session_state.current_view = questionnaire_selected
    else:
        st.session_state.current_view = "Inicio"
        st.success("No tiene cuestionarios pendientes de realizar")
        time.sleep(2)
        st.experimental_rerun()

if st.session_state.current_view == "Inicio":
    start()

if st.session_state.current_view == "Seleccionar":
    select_questionnaire()

if st.session_state.current_view == "BDI-2":
    show_BDI(general_container)

if st.session_state.current_view == "BAI":
    show_BAI(general_container)

