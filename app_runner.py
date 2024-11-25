import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from shared.models.user_model import User, Patient, Base, engine, get_patient_by_id # Import Base and engine here

    
# Create the tables if they don't exist (do this only once!)
Base.metadata.create_all(engine)

#Create a session outside the function
Session = sessionmaker(bind=engine)
session = Session()

def create_patient(user_data): # takes user data
    try:
        new_user = User(**user_data) # Correctly unpacks the dictionary using keyword arguments
        session.add(new_user)
        session.flush()

        if new_user.user_id is None:
            raise ValueError("Failed to create user")

        new_patient = Patient(user_id=new_user.user_id, first_name=user_data['first_name'], last_name=user_data['last_name'], dob=user_data['date_of_birth'])
        session.add(new_patient)
        session.commit()
        return new_patient
    except Exception as e:
        session.rollback()
        print(f"Error creating patient: {e}")
        return None
    finally:
        session.close()





if __name__ == "__main__":
    patient_data = {
        'username': 'johndoe',
        'password': 'securepassword', # Hash this in production!
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'dob': '1990-01-01', # Added dob
    }

    new_patient = create_patient(patient_data)
    print("Created patient:", new_patient)

