import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session,relationship
from sqlalchemy import create_engine,inspect



Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    username = sa.Column(sa.String, unique=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)  # In real app, hash passwords!
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False)
    patients = relationship("Patient", back_populates="user")

    def __init__(self, username, password, first_name, last_name, email, dob):
        self.username = username
        self.password = password  # Remember to hash this in production
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.dob = dob  # Ensure this is defined in the User class

    def __repr__(self):
     return (f"Patient(patient_id={self.patient_id}, user_id={self.user_id}, "
                f"first_name={self.first_name}, last_name={self.last_name}, dob={self.dob})")

class Patient(Base):
    __tablename__ = 'patients'
    patient_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.user_id'))
    first_name = sa.Column(sa.String, nullable=False)
    last_name = sa.Column(sa.String, nullable=False)
    dob = sa.Column(sa.Date, nullable=False)
    user = relationship("User", back_populates="patients")
    

   

class Doctor(Base):
    __tablename__ = 'doctors'
    doctor_id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.user_id'), nullable = False)
    speciality = sa.Column(sa.String, nullable = False)


# Database connection (replace with your database URL)
engine = sa.create_engine('mysql+mysqlconnector://root:Harsh2004@localhost:3306/healthcare')
Base.metadata.create_all(engine)

# Scoped session
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

# Database functions (moved here)
def get_patient_by_id(patient_id):
    try:
        with Session() as session:
            return session.query(Patient).get(patient_id)
    except Exception as e:
        print(f"Error getting patient: {e}")
        return None



def create_patient(patient_data):
    try:
        
        # Create a User object with the necessary fields
        existing_user = session.query(User).filter_by(username=patient_data['username']).first()
        if existing_user:
            print(f"Error creating patient: Username '{patient_data['username']}' already exists.")
            return None

        new_user = User(
            username=patient_data['username'],
            password=patient_data['password'],  # Remember to hash this in production
            first_name=patient_data['first_name'],
            last_name=patient_data['last_name'],
            email=patient_data['email'],
            dob=patient_data['dob']  # Use 'dob' if you renamed it
        )
        
        # Add the user to the session
        with Session() as session:
            session.add(new_user)
            session.commit()  # Commit to get the user_id

            # Now create the Patient object
            new_patient = Patient(
                user_id=new_user.user_id,  # This will be populated after commit
                first_name=patient_data['first_name'],
                last_name=patient_data['last_name'],
                dob=patient_data['dob']
            )
            session.add(new_patient)
            session.commit()
            return new_patient
    except Exception as e:
        print(f"Error creating patient: {e}")
        return None


# Example patient data
patient_data = {
    'username': 'johndoe',
    'password': 'securepassword',  # Remember to hash this in production
    'first_name': 'John',
    'last_name': 'Doe',
    'email': 'john.doe@example.com',
    'dob': '1990-01-01',
}

# Create a patient
new_patient = create_patient(patient_data)

# Print the created patient
print("Created patient:", new_patient)

# Close the session when done
session.close()

# Inspect the table
inspector = inspect(engine)
columns = inspector.get_columns('patients')
for column in columns:
    print(column['name'], column['type'])

