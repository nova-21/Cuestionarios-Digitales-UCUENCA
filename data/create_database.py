import os
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine(os.environ.get("DATABASE"))

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Patient(Base):
    __tablename__ = "patient"
    id = Column(String(10), primary_key=True)
    first_name = Column(String(50))
    second_name = Column(String(50))
    first_family_name = Column(String(50))
    second_family_name = Column(String(50))
    preferred_name = Column(String(50))
    birth_date = Column(Date)
    sex = Column(String(50))
    gender = Column(String(20))
    sexual_orientation = Column(String(20))
    phone_number = Column(String(11))
    email = Column(String(50))
    profession_occupation = Column(String(50))
    marital_status = Column(String(20))
    patient_type = Column(String(20))
    faculty_dependence = Column(String(20))
    career = Column(String(20))
    semester = Column(String(10))
    city_born = Column(String(25))
    city_residence = Column(String(25))
    address = Column(String(50))
    children = Column(Integer)
    lives_with = Column(String(30))
    emergency_contact_name = Column(String(20))
    emergency_contact_relation = Column(String(20))
    emergency_contact_phone = Column(String(10))
    family_history = Column(String())
    personal_history = Column(String())
    extra_information = Column(String())
    encounter = relationship("Encounter", back_populates="patient")
    appointment = relationship("Appointment", back_populates="patient")
    active = Column(Boolean())


class Practitioner(Base):
    __tablename__ = "practitioner"
    id = Column(String(10), primary_key=True)
    full_name = Column(String(50))
    position = Column(String(20))
    email = Column(String(50))
    phone_number = Column(String(10))
    appointment = relationship("Appointment", back_populates="practitioner")
    encounter = relationship("Encounter", back_populates="practitioner")
    active = Column(Boolean())


class Encounter(Base):
    __tablename__ = "encounter"
    id = Column(Integer, primary_key=True, autoincrement=True)
    encounter_type = Column(String(50))
    topics_boarded = Column(String())
    date = Column(Date)
    activities_sent = Column(String(50))
    attachments = Column(String())
    diagnostics = Column(String())
    patient_id = Column(String(10), ForeignKey("patient.id"))
    patient = relationship("Patient", back_populates="encounter")
    practitioner_id = Column(String(50), ForeignKey("practitioner.id"))
    practitioner = relationship("Practitioner", back_populates="encounter")


class Appointment(Base):
    __tablename__ = "appointment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_type = Column(String(50))
    encounter_type = Column(String(50))
    status = Column(String(15))
    reason = Column(String(15))
    date = Column(Date)
    time = Column(String(5))
    patient_id = Column(String(10), ForeignKey("patient.id"))
    patient = relationship("Patient", back_populates="appointment")
    practitioner_id = Column(String(50), ForeignKey("practitioner.id"))
    practitioner = relationship("Practitioner", back_populates="appointment")


class Questionnaire(Base):
    __tablename__ = "questionnaire"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String())
    title = Column(String())
    questions = Column(String())



class QuestionnaireResponse(Base):
    __tablename__ = "questionnaireresponse"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    patient_id = Column(String(10), ForeignKey("patient.id"))
    state = Column(String(10))
    questionnaire_id = Column(Integer)
    result = Column(String())
    answers = Column(String())
    points = Column(Integer)


#
# Base.metadata.create_all(engine)
