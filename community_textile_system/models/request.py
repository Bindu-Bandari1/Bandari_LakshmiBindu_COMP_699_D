from database.db import execute_query, fetch_one, fetch_all


class Request:
    def __init__(self, request_id, user_id, request_type, status,
                 created_at, scheduled_time, assigned_staff_id):
        self.request_id = request_id
        self.user_id = user_id
        self.request_type = request_type
        self.status = status
        self.created_at = created_at
        self.scheduled_time = scheduled_time
        self.assigned_staff_id = assigned_staff_id

    # -----------------------------
    # get request by id
    # -----------------------------
    @staticmethod
    def get_by_id(request_id):
        query = "SELECT * FROM request WHERE request_id = ?"
        data = fetch_one(query, (request_id,))

        if data:
            return Request(
                data["request_id"],
                data["user_id"],
                data["request_type"],
                data["status"],
                data["created_at"],
                data["scheduled_time"],
                data["assigned_staff_id"]
            )
        return None

    # -----------------------------
    # get all requests for a user
    # -----------------------------
    @staticmethod
    def get_by_user(user_id):
        query = """
        SELECT * FROM request
        WHERE user_id = ?
        ORDER BY created_at DESC
        """
        return fetch_all(query, (user_id,))

    # -----------------------------
    # get all pending requests
    # -----------------------------
    @staticmethod
    def get_pending_requests():
        query = "SELECT * FROM request WHERE status = 'PENDING'"
        return fetch_all(query)

    # -----------------------------
    # assign staff to request
    # -----------------------------
    def assign_staff(self, staff_id):
        query = """
        UPDATE request
        SET assigned_staff_id = ?, status = 'ACCEPTED'
        WHERE request_id = ?
        """
        execute_query(query, (staff_id, self.request_id))
        self.assigned_staff_id = staff_id
        self.status = "ACCEPTED"

    # -----------------------------
    # schedule pickup
    # -----------------------------
    def schedule(self, time):
        query = """
        UPDATE request
        SET scheduled_time = ?, status = 'SCHEDULED'
        WHERE request_id = ?
        """
        execute_query(query, (time, self.request_id))
        self.scheduled_time = time
        self.status = "SCHEDULED"

    # -----------------------------
    # update request status
    # -----------------------------
    def update_status(self, new_status):
        query = """
        UPDATE request
        SET status = ?
        WHERE request_id = ?
        """
        execute_query(query, (new_status, self.request_id))
        self.status = new_status

    # -----------------------------
    # cancel request (household)
    # -----------------------------
    def cancel(self):
        if self.status == "PENDING":
            query = """
            UPDATE request
            SET status = 'CANCELLED'
            WHERE request_id = ?
            """
            execute_query(query, (self.request_id,))
            self.status = "CANCELLED"

    # -----------------------------
    # check if editable
    # -----------------------------
    def is_editable(self):
        return self.status == "PENDING"

    # -----------------------------
    # get items under request
    # -----------------------------
    def get_items(self):
        query = """
        SELECT * FROM item
        WHERE request_id = ?
        """
        return fetch_all(query, (self.request_id,))

    # -----------------------------
    # delete request (optional cleanup)
    # -----------------------------
    def delete(self):
        query = "DELETE FROM request WHERE request_id = ?"
        execute_query(query, (self.request_id,))