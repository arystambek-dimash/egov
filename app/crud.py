import json

from fastapi import Depends
from passlib.context import CryptContext

from .config import get_db
from .models import ModerationRequestModel, ModerationStatusEnum, RoleModel, UserModel
from .schema import ModerationRequestCreate, SignUpSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(email: str, db=Depends(get_db)):
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone()
    cursor.close()

    if user_data:
        return UserModel(
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


def create_moderation_request(
    moderation_request: ModerationRequestCreate, db=Depends(get_db)
):
    cursor = db.cursor()
    insert_query = """
    INSERT INTO moderation_requests (
        user_id, fields_to_change
    ) VALUES (%s, %s)
    RETURNING id, user_id, manager_id, 'ON_MODERATION', fields_to_change;
    """
    cursor.execute(
        insert_query,
        (
            moderation_request._user_id,
            json.dumps(moderation_request.fields_to_change),
        ),
    )
    moderation_request_data = cursor.fetchone()
    db.commit()
    cursor.close()
    return ModerationRequestModel(
        id=moderation_request_data[0],
        user_id=moderation_request_data[1],
        manager_id=moderation_request_data[2],
        status=moderation_request_data[3],
        fields_to_change=moderation_request_data[4],
    )


def get_moderation_requests(db=Depends(get_db)):
    cursor = db.cursor()
    query = "SELECT * FROM moderation_requests WHERE status = 'ON_MODERATION'"
    cursor.execute(query, ())
    moderation_request_list = cursor.fetchall()
    cursor.close()
    result_list = []
    if moderation_request_list:
        for moderation_request in moderation_request_list:
            result_list.append(
                ModerationRequestModel(
                    id=moderation_request[0],
                    user_id=moderation_request[1],
                    manager_id=moderation_request[2],
                    status=moderation_request[3],
                    fields_to_change=moderation_request[4],
                )
            )
        return result_list
    return None


def get_moderation_request_by_id(moderation_request_id, db=Depends(get_db)):
    cursor = db.cursor()
    query = (
        "SELECT * FROM moderation_requests WHERE status = 'ON_MODERATION' and id = %s"
    )
    cursor.execute(query, (moderation_request_id,))
    moderation_request_data = cursor.fetchone()
    cursor.close()

    if moderation_request_data:
        return ModerationRequestModel(
            id=moderation_request_data[0],
            user_id=moderation_request_data[1],
            manager_id=moderation_request_data[2],
            status=moderation_request_data[3],
            fields_to_change=moderation_request_data[4],
        )
    return None


def approve_moderation_request_by_id(moderation_request_id, user, db=Depends(get_db)):
    cursor = db.cursor()
    query = (
        "SELECT * FROM moderation_requests WHERE status = 'ON_MODERATION' and id = %s"
    )
    cursor.execute(query, (moderation_request_id,))
    moderation_request_data = cursor.fetchone()

    if not moderation_request_data:
        return {"message": "Moderation request not found"}

    fields_to_change = moderation_request_data[4]
    query_string = ", ".join(
        [f"{field}='{fields_to_change[field]}'" for field in fields_to_change]
    )

    query_to_update_user_info = "UPDATE users SET {} WHERE id = %s".format(query_string)
    cursor.execute(query_to_update_user_info, (user.id,))

    query_to_update_moderation = (
        "UPDATE moderation_requests SET status = %s, manager_id = %s WHERE id = %s"
    )
    cursor.execute(
        query_to_update_moderation,
        (ModerationStatusEnum.APPROVED, user.id, moderation_request_id),
    )

    db.commit()
    cursor.close()
    return {"message": "success"}


def cancel_moderation_request_by_id(moderation_request_id, user, db=Depends(get_db)):
    cursor = db.cursor()
    query = (
        "SELECT * FROM moderation_requests WHERE status = 'ON_MODERATION' and id = %s"
    )
    cursor.execute(query, (moderation_request_id,))
    moderation_request_data = cursor.fetchone()

    if not moderation_request_data:
        return {"message": "Moderation request not found"}

    fields_to_change = moderation_request_data[4]
    query_string = ", ".join(
        [f"{field}='{fields_to_change[field]}'" for field in fields_to_change]
    )

    query_to_update_user_info = "UPDATE users SET {} WHERE id = %s".format(query_string)
    cursor.execute(query_to_update_user_info, (user.id,))

    query_to_update_moderation = (
        "UPDATE moderation_requests SET status = %s, manager_id = %s WHERE id = %s"
    )
    cursor.execute(
        query_to_update_moderation,
        (ModerationStatusEnum.CANCELED, user.id, moderation_request_id),
    )

    db.commit()
    cursor.close()
    return {"message": "success"}
