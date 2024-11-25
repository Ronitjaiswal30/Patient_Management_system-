import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from shared.models import Base

class Appointment(Base):
    __tablename__ = 'appointments'
    id = sa.Column(sa.Integer, primary_key=True)
    patient_id = sa.Column(sa.Integer, sa.ForeignKey('patients.id'))
    doctor_id = sa.Column(sa.Integer, sa.ForeignKey('doctors.id'))
    appointment_time = sa.Column(sa.DateTime)



