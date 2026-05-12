from models.user import User
from database.db import execute_query, fetch_all, fetch_one


class Household(User):
    def __init__(self, user_id, name, email, password, address, phone_number):
        super().__init__(user_id, name, email, password, role="household")
        self.address = address
        self.phone_number = phone_number

    # -----------------------------
    # create household profile (UPDATED)
    # -----------------------------
    @staticmethod
    def create_profile(user_id, address, phone_number):
        query = """
        INSERT INTO household (user_id, address, phone_number)
        VALUES (?, ?, ?)
        """
        return execute_query(query, (user_id, address, phone_number))

    # -----------------------------
    # get household profile (NEW - useful for staff view)
    # -----------------------------
    @staticmethod
    def get_profile(user_id):
        query = """
        SELECT * FROM household
        WHERE user_id = ?
        """
        return fetch_one(query, (user_id,))

    # -----------------------------
    # create pickup or drop-off request
    # -----------------------------
    def create_request(self, request_type):
        query = """
        INSERT INTO request (user_id, request_type, status)
        VALUES (?, ?, 'PENDING')
        """
        return execute_query(query, (self.user_id, request_type))

    # -----------------------------
    # add item to request
    # -----------------------------
    def add_item(self, request_id, item_type, quantity, note, photo_path):
        query = """
        INSERT INTO item (request_id, item_type, quantity, condition_note, photo_path)
        VALUES (?, ?, ?, ?, ?)
        """
        return execute_query(query, (request_id, item_type, quantity, note, photo_path))

    # -----------------------------
    # view all requests
    # -----------------------------
    def view_requests(self):
        query = """
        SELECT * FROM request
        WHERE user_id = ?
        ORDER BY created_at DESC
        """
        return fetch_all(query, (self.user_id,))

    # -----------------------------
    # view single request details
    # -----------------------------
    def view_request_details(self, request_id):
        query = """
        SELECT * FROM request
        WHERE request_id = ? AND user_id = ?
        """
        return fetch_one(query, (request_id, self.user_id))

    # -----------------------------
    # edit request (only if pending)
    # -----------------------------
    def edit_request(self, request_id, new_type):
        query = """
        UPDATE request
        SET request_type = ?
        WHERE request_id = ? AND status = 'PENDING'
        """
        execute_query(query, (new_type, request_id))

    # -----------------------------
    # cancel request (before pickup)
    # -----------------------------
    def cancel_request(self, request_id):
        query = """
        UPDATE request
        SET status = 'CANCELLED'
        WHERE request_id = ? AND status = 'PENDING'
        """
        execute_query(query, (request_id,))

    # -----------------------------
    # view pickup schedule
    # -----------------------------
    def view_schedule(self, request_id):
        query = """
        SELECT scheduled_time
        FROM request
        WHERE request_id = ? AND user_id = ?
        """
        return fetch_one(query, (request_id, self.user_id))

    # -----------------------------
    # search past requests
    # -----------------------------
    def search_requests(self, keyword):
        query = """
        SELECT * FROM request
        WHERE user_id = ? AND request_type LIKE ?
        """
        return fetch_all(query, (self.user_id, f"%{keyword}%"))

    # -----------------------------
    # view request history
    # -----------------------------
    def view_history(self):
        query = """
        SELECT * FROM request
        WHERE user_id = ?
        AND status IN ('COMPLETED', 'REJECTED', 'CANCELLED')
        ORDER BY created_at DESC
        """
        return fetch_all(query, (self.user_id,))

    # -----------------------------
    # view condition result for item
    # -----------------------------
    def view_condition_result(self, item_id):
        query = """
        SELECT * FROM condition_result
        WHERE item_id = ?
        """
        return fetch_one(query, (item_id,))

    # -----------------------------
    # view handling path suggestion
    # -----------------------------
    def view_handling_path(self, item_id):
        query = """
        SELECT hp.*
        FROM handling_path hp
        JOIN condition_result cr ON hp.result_id = cr.result_id
        WHERE cr.item_id = ?
        """
        return fetch_one(query, (item_id,))

    # -----------------------------
    # confirm handling path
    # -----------------------------
    def confirm_handling_path(self, item_id):
        query = """
        UPDATE handling_path
        SET is_confirmed = 1
        WHERE result_id IN (
            SELECT result_id FROM condition_result WHERE item_id = ?
        )
        """
        execute_query(query, (item_id,))