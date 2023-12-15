from fastapi import Depends
from passlib.context import CryptContext

from .config import get_db
from .models import Role, User
from .schema import SignUpSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(email: str, db=Depends(get_db)):
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    cursor.close()

    if user_data:
        return User(
            id=user_data[0],
            email=user_data[1],
            phone_number=user_data[2],
            first_name=user_data[3],
            last_name=user_data[4],
            address=user_data[5],
            password=user_data[6],
            registered_at=user_data[7],
            role_id=user_data[8],
            telegram_chat_id=user_data[9],
        )
    return None


def create_user(user: SignUpSchema, db=Depends(get_db)):
    cursor = db.cursor()
    insert_query = """
    INSERT INTO users (
        email, phone_number, first_name, last_name, address, password, role_id, telegram_chat_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id, email, phone_number, first_name, last_name, address, password, role_id, telegram_chat_id;
    """
    cursor.execute(
        insert_query,
        (
            user.email,
            user.phone_number,
            user.first_name,
            user.last_name,
            user.address,
            pwd_context.hash(user.password),
            1,
            user.telegram_chat_id,
        ),
    )
    user_data = cursor.fetchone()
    db.commit()
    cursor.close()

    return SignUpSchema(
        id=user_data[0],
        email=user_data[1],
        phone_number=user_data[2],
        first_name=user_data[3],
        last_name=user_data[4],
        address=user_data[5],
        password=user_data[6],
        telegram_chat_id=user_data[8],
    )
