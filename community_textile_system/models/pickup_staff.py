from models.user import User
from database.db import execute_query, fetch_all, fetch_one


class PickupStaff(User):
    def __init__(self, user_id, name, email, password, staff_id, assigned_area_id, is_approved):
        super().__init__(user_id, name, email, password, role="staff")
        self.staff_id = staff_id
        self.assigned_area_id = assigned_area_id
        self.is_approved = is_approved

    # -----------------------------
    # create staff profile (admin approval required)
    # -----------------------------
    @staticmethod
    def create_profile(user_id, staff_id, area_id):
        query = """
        INSERT INTO pickup_staff (user_id, staff_id, assigned_area_id, is_approved)
        VALUES (?, ?, ?, 0)
        """
        execute_query(query, (user_id, staff_id, area_id))

    # -----------------------------
    # approve staff (admin will use this)
    # -----------------------------
    @staticmethod
    def approve_staff(user_id):
        query = """
        UPDATE pickup_staff
        SET is_approved = 1
        WHERE user_id = ?
        """
        execute_query(query, (user_id,))

    # -----------------------------
    # view all open requests
    # -----------------------------
    def view_open_requests(self):
        query = """
        SELECT * FROM request
        WHERE status = 'PENDING'
        """
        return fetch_all(query)

    # -----------------------------
    # accept request
    # -----------------------------
    def accept_request(self, request_id):
        query = """
        UPDATE request
        SET status = 'ACCEPTED',
            assigned_staff_id = ?
        WHERE request_id = ? AND status = 'PENDING'
        """
        execute_query(query, (self.user_id, request_id))

    # -----------------------------
    # propose pickup time
    # -----------------------------
    def propose_time(self, request_id, scheduled_time):
        query = """
        UPDATE request
        SET scheduled_time = ?, status = 'SCHEDULED'
        WHERE request_id = ? AND assigned_staff_id = ?
        """
        execute_query(query, (scheduled_time, request_id, self.user_id))

    # -----------------------------
    # update collection status
    # -----------------------------
    def update_status(self, request_id, status):
        query = """
        UPDATE request
        SET status = ?
        WHERE request_id = ? AND assigned_staff_id = ?
        """
        execute_query(query, (status, request_id, self.user_id))

    # -----------------------------
    # view items in a request
    # -----------------------------
    def view_items(self, request_id):
        query = """
        SELECT * FROM item
        WHERE request_id = ?
        """
        return fetch_all(query, (request_id,))

    # -----------------------------
    # view condition result
    # -----------------------------
    def view_condition_result(self, item_id):
        query = """
        SELECT * FROM condition_result
        WHERE item_id = ?
        """
        return fetch_one(query, (item_id,))

    # -----------------------------
    # view handling path
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
    # override handling path
    # -----------------------------
    def override_handling_path(self, item_id, new_path, reason):
        # get result id first
        query = "SELECT result_id FROM condition_result WHERE item_id = ?"
        result = fetch_one(query, (item_id,))

        if result:
            result_id = result["result_id"]

            update_query = """
            UPDATE handling_path
            SET path_type = ?, override_reason = ?, is_confirmed = 1
            WHERE result_id = ?
            """
            execute_query(update_query, (new_path, reason, result_id))

            # mark item as overridden
            item_query = """
            UPDATE item
            SET overridden_flag = 1
            WHERE item_id = ?
            """
            execute_query(item_query, (item_id,))

    # -----------------------------
    # mark item received
    # -----------------------------
    def mark_received(self, request_id):
        query = """
        UPDATE request
        SET status = 'COMPLETED'
        WHERE request_id = ? AND assigned_staff_id = ?
        """
        execute_query(query, (request_id, self.user_id))

    # -----------------------------
    # mark item rejected
    # -----------------------------
    def mark_rejected(self, request_id):
        query = """
        UPDATE request
        SET status = 'REJECTED'
        WHERE request_id = ? AND assigned_staff_id = ?
        """
        execute_query(query, (request_id, self.user_id))