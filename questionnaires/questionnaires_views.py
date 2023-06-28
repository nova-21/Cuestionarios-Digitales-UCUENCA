import time
import streamlit as st
import json
from PIL import Image
from data.actions.questionnaire_response_actions import add_questionnaire_response_answers
from data.conection import create_engine_conection


def cargar_preguntas(encuesta):
    """
    Loads the questions and related information from a JSON file.

    Parameters:
    - encuesta (str): The name of the questionnaire.

    Returns:
    - tuple: A tuple containing the loaded questions, section keys, and instructions.
    """
    archivo = "./questionnaires/" + encuesta + ".json"
    f = open(archivo, encoding='utf-8')
    preguntas = json.load(f)
    claves = list(preguntas["seccion"].keys())
    indicaciones = preguntas["indicaciones"]
    return preguntas, claves, indicaciones


def limpiar():
    """
    Clears the previous content and displays the header for the survey.
    """
    membrete = st.empty()
    membrete.empty()
    with membrete.container():
        img = Image.open("ucuenca.png")
        st.image(img, width=200)
        st.header("Departamento de Bienestar Universitario")
        st.subheader("Sistema de encuestas psicológicas")


def show_questions(preguntas, claves, indicaciones, text):
    """
    Displays the questions, instructions, and collects responses from the user.

    Parameters:
    - preguntas (dict): Dictionary containing the questions.
    - claves (list): List of section keys.
    - indicaciones (str): Instructions for the questionnaire.
    - text (str): Text to display before the questions.
    """
    for _ in list(preguntas):
        placeholder = st.empty()
        num = st.session_state.num
        with placeholder.form(key=str(num)):
            limpiar()
            st.markdown(text)
            st.caption(indicaciones)

            valor = st.radio(claves[num], key=num + 1, options=(preguntas["seccion"][claves[num]]).values())
            submit = st.form_submit_button("Enviar")
        if submit:
            st.session_state.answers_copy[claves[num]] = valor
            st.session_state.contador = st.session_state.contador + int(valor[0])
            st.session_state.num += 1
            if st.session_state.num >= len(claves):
                placeholder.text("")
                break
            placeholder.empty()
        else:
            st.stop()


def show_BDI(general_container):
    """
    Displays and collects responses for the BDI-2 questionnaire.

    Parameters:
    - general_container: The container in which the questionnaire will be displayed.
    """
    with general_container.empty():
        questions, question_indexes, questionnaire_instructions = cargar_preguntas("BDI-2")
        show_questions(questions, question_indexes, questionnaire_instructions, "Cuestionario de depresión")

        # Determine the text result based on the score
        if 0 <= st.session_state.contador <= 13:
            text_result = "Mínima depresión"
        elif 14 <= st.session_state.contador <= 19:
            text_result = "Depresión leve"
        elif 20 <= st.session_state.contador <= 28:
            text_result = "Depresión moderada"
        elif 29 <= st.session_state.contador <= 63:
            text_result = "Depresión grave"

        # Add the questionnaire response to the database
        add_questionnaire_response_answers(
            create_engine_conection(),
            st.session_state.current_questionnaire,
            st.session_state.contador,
            text_result,
            json.dumps(st.session_state.answers_copy)
        )

        # Reset session state
        st.session_state.num = 0
        st.session_state.contador = 0
        st.session_state.answers_copy = {}

        st.success("Gracias por completar el cuestionario")
        time.sleep(2)
        st.session_state.current_view = "Seleccionar"
        st.experimental_rerun()


def show_BAI(general_container):
    """
    Displays and collects responses for the BAI questionnaire.

    Parameters:
    - general_container: The container in which the questionnaire will be displayed.
    """
    with general_container.empty():
        questions, question_indexes, questionnaire_instructions = cargar_preguntas("BAI")
        show_questions(questions, question_indexes, questionnaire_instructions, "Cuestionario de ansiedad")

        # Determine the text result based on the score
        if 0 <= st.session_state.contador <= 21:
            text_result = "Ansiedad muy baja"
        elif 22 <= st.session_state.contador <= 35:
            text_result = "Ansiedad leve"
        elif st.session_state.contador >= 36:
            text_result = "Ansiedad severa"

        # Add the questionnaire response to the database
        add_questionnaire_response_answers(
            create_engine_conection(),
            st.session_state.current_questionnaire,
            st.session_state.contador,
            text_result,
            json.dumps(st.session_state.answers_copy)
        )

        # Reset session state
        st.session_state.num = 0
        st.session_state.contador = 0
        st.session_state.answers_copy = {}

        st.success("Gracias por completar el cuestionario")
        time.sleep(2)
        st.session_state.current_view = "Seleccionar"
        st.experimental_rerun()
