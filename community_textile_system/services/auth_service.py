from models.user import User
from models.household import Household
from models.pickup_staff import PickupStaff
from models.admin import Admin
from database.db import fetch_one


# -----------------------------
# register household user
# -----------------------------
def register_household(name, email, password, address, phone_number):
    # check if email already exists
    existing = fetch_one("SELECT * FROM users WHERE email = ?", (email,))
    if existing:
        return None, "Email already registered"

    # basic validation
    if not all([name, email, password, address, phone_number]):
        return None, "All fields are required"

    # create user
    user_id = User.register(name, email, password, role="household")

    if not user_id:
        return None, "User creation failed"

    # create household profile (UPDATED)
    Household.create_profile(user_id, address, phone_number)

    return user_id, "Registration successful"


# -----------------------------
# login user (all roles)
# -----------------------------
def login_user(email, password):
    user = User.login(email, password)

    if not user:
        return None, "Invalid email or password"

    # check role-specific conditions
    if user.role == "staff":
        staff = fetch_one(
            "SELECT * FROM pickup_staff WHERE user_id = ?",
            (user.user_id,)
        )
        if staff and staff["is_approved"] == 0:
            return None, "Staff not approved yet"

    return user, "Login successful"


# -----------------------------
# reset password
# -----------------------------
def reset_password(user_id, new_password):
    user = User.get_by_id(user_id)

    if not user:
        return "User not found"

    user.reset_password(new_password)
    return "Password updated successfully"


# -----------------------------
# get dashboard route (helper)
# -----------------------------
def get_dashboard(user):
    if user.role == "household":
        return "household_dashboard"
    elif user.role == "staff":
        return "staff_dashboard"
    elif user.role == "admin":
        return "admin_dashboard"
    return None