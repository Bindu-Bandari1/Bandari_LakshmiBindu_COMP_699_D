from models.user import User
from database.db import execute_query, fetch_all, fetch_one


class Admin(User):
    def __init__(self, user_id, name, email, password, admin_code):
        super().__init__(user_id, name, email, password, role="admin")
        self.admin_code = admin_code

    # -----------------------------
    # create admin profile (manual setup)
    # -----------------------------
    @staticmethod
    def create_admin(user_id, admin_code):
        query = """
        INSERT INTO admin (user_id, admin_code)
        VALUES (?, ?)
        """
        execute_query(query, (user_id, admin_code))

    # -----------------------------
    # create service area
    # -----------------------------
    def create_service_area(self, area_name):
        query = """
        INSERT INTO service_area (area_name)
        VALUES (?)
        """
        execute_query(query, (area_name,))

    # -----------------------------
    # update textile category
    # -----------------------------
    def update_category(self, category_name):
        # insert if not exists
        query = """
        INSERT INTO textile_category (category_name)
        VALUES (?)
        """
        execute_query(query, (category_name,))

    # -----------------------------
    # view all service areas
    # -----------------------------
    def view_service_areas(self):
        query = "SELECT * FROM service_area"
        return fetch_all(query)

    # -----------------------------
    # view all categories
    # -----------------------------
    def view_categories(self):
        query = "SELECT * FROM textile_category"
        return fetch_all(query)

    # -----------------------------
    # create pickup staff (admin controlled)
    # -----------------------------
    def create_pickup_staff(self, name, email, password, staff_id, area_id):
        # create user first
        user_query = """
        INSERT INTO users (name, email, password, role)
        VALUES (?, ?, ?, 'staff')
        """
        user_id = execute_query(user_query, (name, email, password))

        # create staff profile
        staff_query = """
        INSERT INTO pickup_staff (user_id, staff_id, assigned_area_id, is_approved)
        VALUES (?, ?, ?, 1)
        """
        execute_query(staff_query, (user_id, staff_id, area_id))

        return user_id

    # -----------------------------
    # approve pickup staff
    # -----------------------------
    def approve_staff(self, user_id):
        query = """
        UPDATE pickup_staff
        SET is_approved = 1
        WHERE user_id = ?
        """
        execute_query(query, (user_id,))

    # -----------------------------
    # view all pickup staff
    # -----------------------------
    def view_staff(self):
        query = """
        SELECT u.user_id, u.name, u.email, ps.staff_id, ps.is_approved
        FROM users u
        JOIN pickup_staff ps ON u.user_id = ps.user_id
        WHERE u.role = 'staff'
        """
        return fetch_all(query)

    # -----------------------------
    # view system requests (monitoring)
    # -----------------------------
    def view_all_requests(self):
        query = "SELECT * FROM request"
        return fetch_all(query)