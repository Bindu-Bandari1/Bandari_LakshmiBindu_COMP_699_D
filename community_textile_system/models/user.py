from database.db import fetch_one, execute_query
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, user_id, name, email, password, role):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    # -----------------------------
    # register new user (household only)
    # -----------------------------
    @staticmethod
    def register(name, email, password, role="household"):
        # hash password before storing
        hashed_password = generate_password_hash(password)

        query = """
        INSERT INTO users (name, email, password, role)
        VALUES (?, ?, ?, ?)
        """
        user_id = execute_query(query, (name, email, hashed_password, role))

        return user_id

    # -----------------------------
    # login user
    # -----------------------------
    @staticmethod
    def login(email, password):
        query = "SELECT * FROM users WHERE email = ?"
        user = fetch_one(query, (email,))

        if user:
            # check password
            if check_password_hash(user["password"], password):
                return User(
                    user["user_id"],
                    user["name"],
                    user["email"],
                    user["password"],
                    user["role"]
                )
        return None

    # -----------------------------
    # get user by id
    # -----------------------------
    @staticmethod
    def get_by_id(user_id):
        query = "SELECT * FROM users WHERE user_id = ?"
        user = fetch_one(query, (user_id,))

        if user:
            return User(
                user["user_id"],
                user["name"],
                user["email"],
                user["password"],
                user["role"]
            )
        return None

    # -----------------------------
    # update profile
    # -----------------------------
    def update_profile(self, name):
        query = """
        UPDATE users
        SET name = ?
        WHERE user_id = ?
        """
        execute_query(query, (name, self.user_id))
        self.name = name

    # -----------------------------
    # reset password
    # -----------------------------
    def reset_password(self, new_password):
        hashed_password = generate_password_hash(new_password)

        query = """
        UPDATE users
        SET password = ?
        WHERE user_id = ?
        """
        execute_query(query, (hashed_password, self.user_id))

    # -----------------------------
    # helper: check role
    # -----------------------------
    def is_household(self):
        return self.role == "household"

    def is_staff(self):
        return self.role == "staff"

    def is_admin(self):
        return self.role == "admin"