import pandas as pd
import pytz
from sqlalchemy import cast
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import datetime
from data.create_database import QuestionnaireResponse, Questionnaire


def add_questionnaire_response(db_engine, date, patient_id, questionnaire_id):
    res = get_pending_questionnaire(db_engine, date, patient_id, questionnaire_id)
    print(res)
    if len(res) == 0:
        add_questionnaire(db_engine, date, patient_id, "pending", questionnaire_id, "")

def add_questionnaire_response_answers(db_engine, questionnaire_response_id, points, result, answers):
    Session = sessionmaker(bind=db_engine)
    session = Session()

    try:
        # Get the QuestionnaireResponse instance with the specified ID
        response = session.query(QuestionnaireResponse).filter_by(id=questionnaire_response_id).first()

        if response:
            # Update the answers and state fields
            response.result = result
            response.answers = answers
            response.state = "finished"
            response.points = points
            # Commit the changes
            session.commit()
            return "QuestionnaireResponse updated successfully"
        else:
            return f"QuestionnaireResponse with ID {questionnaire_response_id} not found"
    except Exception as e:
        # Rollback the session in case of an error
        session.rollback()
        print(f"Error updating QuestionnaireResponse: {e}")
        return "Error updating QuestionnaireResponse"
    finally:
        # Close the session
        session.close()

def add_questionnaire(db_engine, date, patient_id, state, questionnaire_id, answers):
    # Create a Session
    Session = sessionmaker(bind=db_engine)
    session = Session()
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    elif isinstance(date, datetime):
        date = date.date()
    # Create a new QuestionnaireResponse instance
    questionnaire_response = QuestionnaireResponse()
    questionnaire_response.date = date
    questionnaire_response.patient_id = patient_id
    questionnaire_response.state = state
    questionnaire_response.questionnaire_id = questionnaire_id
    questionnaire_response.answers = answers

    try:
        # Add the new QuestionnaireResponse to the session and commit
        session.add(questionnaire_response)
        session.commit()
        return "Questionnaire response added successfully."
    except IntegrityError:
        # Rollback the session in case of IntegrityError (e.g. duplicate primary key)
        session.rollback()
        message = "Error adding questionnaire response, please check your data and try again."
        print(message)
        return message
    finally:
        # Close the session
        session.close()

def get_pending_questionnaire_responses(db_engine, date, patient_id):
    # Create a Session
    Session = sessionmaker(bind=db_engine)
    session = Session()

    # Query the database for QuestionnaireResponse instances with matching date, patient_id, and state='pending'
    pending_responses = session.query(QuestionnaireResponse, Questionnaire.name).filter_by(date=date, patient_id=patient_id, state='pending').join(Questionnaire, QuestionnaireResponse.questionnaire_id == Questionnaire.id).all()

    # Close the session
    session.close()

    # Return the list of matching QuestionnaireResponse instances
    return pending_responses

def get_pending_questionnaire(db_engine, date, patient_id, questionnaire_id):
    from datetime import datetime, timedelta
    import pytz
    # Create a Session
    Session = sessionmaker(bind=db_engine)
    session = Session()

    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d").date()
    elif isinstance(date, datetime):
        date = date.date()

    # Query the database for QuestionnaireResponse instances with matching date, patient_id, and state='pending'
    pending_responses = session.query(QuestionnaireResponse.id).filter_by(patient_id=patient_id,questionnaire_id=questionnaire_id,
                                                                       state='pending', date = date).all()

    # Close the session
    session.close()

    # Return the list of matching QuestionnaireResponse instances
    return pending_responses