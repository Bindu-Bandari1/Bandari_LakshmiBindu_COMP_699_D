from models.admin import Admin
from models.service_area import ServiceArea
from models.textile_category import TextileCategory
from models.pickup_staff import PickupStaff
from models.user import User
from database.db import fetch_all, fetch_one, execute_query
from werkzeug.security import generate_password_hash


# -----------------------------
# create service area
# -----------------------------
def create_service_area(area_name):
    return ServiceArea.create(area_name)


# -----------------------------
# get all service areas
# -----------------------------
def get_service_areas():
    return ServiceArea.get_all()


# -----------------------------
# create textile category
# -----------------------------
def create_category(category_name):
    return TextileCategory.create(category_name)


# -----------------------------
# get all categories
# -----------------------------
def get_categories():
    return TextileCategory.get_all()


# -----------------------------
# create pickup staff (admin controlled)
# -----------------------------
def create_staff(name, email, password, staff_id, area_id):
    # check if email exists
    existing = fetch_one("SELECT * FROM users WHERE email = ?", (email,))
    if existing:
        return None, "Email already exists"

    # hash password
    hashed_password = generate_password_hash(password)

    # create user
    user_query = """
    INSERT INTO users (name, email, password, role)
    VALUES (?, ?, ?, 'staff')
    """
    user_id = execute_query(user_query, (name, email, hashed_password))

    # create staff profile (not approved initially)
    PickupStaff.create_profile(user_id, staff_id, area_id)

    return user_id, "Staff created successfully (pending approval)"


# -----------------------------
# approve staff
# -----------------------------
def approve_staff(user_id):
    PickupStaff.approve_staff(user_id)
    return "Staff approved"


# -----------------------------
# get all staff
# -----------------------------
def get_all_staff():
    query = """
    SELECT u.user_id, u.name, u.email, ps.staff_id, ps.is_approved, ps.assigned_area_id
    FROM users u
    JOIN pickup_staff ps ON u.user_id = ps.user_id
    WHERE u.role = 'staff'
    """
    return fetch_all(query)


# -----------------------------
# get all requests (admin monitoring)
# -----------------------------
def get_all_requests():
    query = "SELECT * FROM request ORDER BY created_at DESC"
    return fetch_all(query)