from database.db import execute_query, fetch_one


class HandlingPath:
    def __init__(self, path_id, result_id, path_type, is_confirmed, override_reason):
        self.path_id = path_id
        self.result_id = result_id
        self.path_type = path_type
        self.is_confirmed = is_confirmed
        self.override_reason = override_reason

    # -----------------------------
    # create handling path based on ML result
    # -----------------------------
    @staticmethod
    def create(result_id, condition_label):
        # map condition to handling path
        if condition_label == "good":
            path = "reuse"
        elif condition_label == "worn":
            path = "repair"
        else:
            path = "recycle"

        query = """
        INSERT INTO handling_path (result_id, path_type, is_confirmed)
        VALUES (?, ?, 0)
        """
        path_id = execute_query(query, (result_id, path))
        return path_id

    # -----------------------------
    # get handling path by item
    # -----------------------------
    @staticmethod
    def get_by_item(item_id):
        query = """
        SELECT hp.*
        FROM handling_path hp
        JOIN condition_result cr ON hp.result_id = cr.result_id
        WHERE cr.item_id = ?
        """
        data = fetch_one(query, (item_id,))

        if data:
            return HandlingPath(
                data["path_id"],
                data["result_id"],
                data["path_type"],
                data["is_confirmed"],
                data["override_reason"]
            )
        return None

    # -----------------------------
    # confirm handling path (household)
    # -----------------------------
    def confirm(self):
        query = """
        UPDATE handling_path
        SET is_confirmed = 1
        WHERE path_id = ?
        """
        execute_query(query, (self.path_id,))
        self.is_confirmed = 1

    # -----------------------------
    # override handling path (staff)
    # -----------------------------
    def override(self, new_path, reason):
        query = """
        UPDATE handling_path
        SET path_type = ?, override_reason = ?, is_confirmed = 1
        WHERE path_id = ?
        """
        execute_query(query, (new_path, reason, self.path_id))

        self.path_type = new_path
        self.override_reason = reason
        self.is_confirmed = 1