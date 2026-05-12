from database.db import execute_query, fetch_one, fetch_all


class Item:
    def __init__(self, item_id, request_id, item_type, quantity,
                 condition_note, photo_path, confirmed_path, overridden_flag):
        self.item_id = item_id
        self.request_id = request_id
        self.item_type = item_type
        self.quantity = quantity
        self.condition_note = condition_note
        self.photo_path = photo_path
        self.confirmed_path = confirmed_path
        self.overridden_flag = overridden_flag

    # -----------------------------
    # create new item
    # -----------------------------
    @staticmethod
    def create(request_id, item_type, quantity, condition_note, photo_path):
        query = """
        INSERT INTO item (request_id, item_type, quantity, condition_note, photo_path)
        VALUES (?, ?, ?, ?, ?)
        """
        item_id = execute_query(query, (request_id, item_type, quantity, condition_note, photo_path))
        return item_id

    # -----------------------------
    # get item by id
    # -----------------------------
    @staticmethod
    def get_by_id(item_id):
        query = "SELECT * FROM item WHERE item_id = ?"
        data = fetch_one(query, (item_id,))

        if data:
            return Item(
                data["item_id"],
                data["request_id"],
                data["item_type"],
                data["quantity"],
                data["condition_note"],
                data["photo_path"],
                data["confirmed_path"],
                data["overridden_flag"]
            )
        return None

    # -----------------------------
    # get all items in a request
    # -----------------------------
    @staticmethod
    def get_by_request(request_id):
        query = """
        SELECT * FROM item
        WHERE request_id = ?
        """
        return fetch_all(query, (request_id,))

    # -----------------------------
    # update item details
    # -----------------------------
    def update_item(self, item_type, quantity, note):
        query = """
        UPDATE item
        SET item_type = ?, quantity = ?, condition_note = ?
        WHERE item_id = ?
        """
        execute_query(query, (item_type, quantity, note, self.item_id))

        self.item_type = item_type
        self.quantity = quantity
        self.condition_note = note

    # -----------------------------
    # update photo path
    # -----------------------------
    def update_photo(self, photo_path):
        query = """
        UPDATE item
        SET photo_path = ?
        WHERE item_id = ?
        """
        execute_query(query, (photo_path, self.item_id))
        self.photo_path = photo_path

    # -----------------------------
    # set confirmed handling path
    # -----------------------------
    def set_confirmed_path(self, path):
        query = """
        UPDATE item
        SET confirmed_path = ?
        WHERE item_id = ?
        """
        execute_query(query, (path, self.item_id))
        self.confirmed_path = path

    # -----------------------------
    # mark item as overridden
    # -----------------------------
    def mark_overridden(self):
        query = """
        UPDATE item
        SET overridden_flag = 1
        WHERE item_id = ?
        """
        execute_query(query, (self.item_id,))
        self.overridden_flag = 1

    # -----------------------------
    # delete item
    # -----------------------------
    def delete(self):
        query = "DELETE FROM item WHERE item_id = ?"
        execute_query(query, (self.item_id,))