from shared.models import User, session
from werkzeug.security import generate_password_hash, check_password_hash #For password security


def create_user(username, password):
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password)
    session.add(user)
    session.commit()
    return user

def get_user_by_username(username):
    return session.query(User).filter_by(username=username).first()

def verify_password(user, password):
    return check_password_hash(user.password, password)
