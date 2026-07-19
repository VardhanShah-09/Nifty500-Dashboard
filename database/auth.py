import bcrypt
from datetime import datetime

from database.database import get_connection


# =====================================================
# PASSWORD FUNCTIONS
# =====================================================

def hash_password(password):
    """
    Convert a plain-text password into a secure hashed password.
    """
    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(plain_password, hashed_password):
    """
    Verify entered password against stored password.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# =====================================================
# USER RETRIEVAL
# =====================================================

def get_user_by_username(username):
    """
    Get user by username.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def get_user(login):
    """
    Get user by username OR email.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        OR email = ?
        """,
        (login, login)
    )

    user = cursor.fetchone()

    conn.close()

    return user


def get_all_users():
    """
    Get all users.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        ORDER BY id
    """)

    users = cursor.fetchall()

    conn.close()

    return users


# =====================================================
# LOGIN
# =====================================================

def update_last_login(user_id):
    """
    Update last login time.
    """

    conn = get_connection()
    cursor = conn.cursor()

    last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """
        UPDATE users
        SET last_login = ?
        WHERE id = ?
        """,
        (last_login, user_id)
    )

    conn.commit()
    conn.close()


def login_user(login, password):
    """
    Authenticate user using username OR email.
    """

    user = get_user(login)

    if user is None:
        return None

    if user["is_active"] == 0:
        return None

    if verify_password(password, user["password"]):

        update_last_login(user["id"])

        return get_user(login)

    return None


# =====================================================
# CREATE USER
# =====================================================

def create_user(
    username,
    full_name,
    email,
    password,
    role="USER",
    is_admin=0
):
    """
    Create new user.
    """

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(password)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:

        cursor.execute("""
            INSERT INTO users
            (
                username,
                full_name,
                email,
                password,
                role,
                is_admin,
                is_active,
                created_at,
                last_login
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username,
            full_name,
            email,
            hashed_password,
            role,
            is_admin,
            1,
            created_at,
            None
        ))

        conn.commit()

        return True, "User created successfully."

    except Exception as e:

        return False, str(e)

    finally:

        conn.close()


# =====================================================
# UPDATE USER
# =====================================================

def update_user(
    user_id,
    full_name,
    email,
    role,
    is_admin,
    is_active
):
    """
    Update user information.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users

        SET
            full_name=?,
            email=?,
            role=?,
            is_admin=?,
            is_active=?

        WHERE id=?
    """, (
        full_name,
        email,
        role,
        is_admin,
        is_active,
        user_id
    ))

    conn.commit()
    conn.close()


# =====================================================
# DELETE USER
# =====================================================

def delete_user(user_id):
    """
    Delete user.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()


# =====================================================
# PASSWORD RESET
# =====================================================

def reset_password(user_id, new_password):
    """
    Reset user password.
    """

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hash_password(new_password)

    cursor.execute("""
        UPDATE users

        SET password=?

        WHERE id=?
    """, (
        hashed_password,
        user_id
    ))

    conn.commit()
    conn.close()


# =====================================================
# ADMIN RIGHTS
# =====================================================

def make_admin(user_id):
    """
    Grant admin rights.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users

        SET
            role='ADMIN',
            is_admin=1

        WHERE id=?
    """, (user_id,))

    conn.commit()
    conn.close()


def remove_admin(user_id):
    """
    Remove admin rights.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users

        SET
            role='USER',
            is_admin=0

        WHERE id=?
    """, (user_id,))

    conn.commit()
    conn.close()


# =====================================================
# USER STATUS
# =====================================================

def enable_user(user_id):
    """
    Enable user account.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users

        SET is_active=1

        WHERE id=?
    """, (user_id,))

    conn.commit()
    conn.close()


def disable_user(user_id):
    """
    Disable user account.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users

        SET is_active=0

        WHERE id=?
    """, (user_id,))

    conn.commit()
    conn.close()


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    users = get_all_users()

    for user in users:

        print(
            user["id"],
            user["username"],
            user["full_name"],
            user["role"],
            user["is_admin"],
            user["is_active"]
        )
