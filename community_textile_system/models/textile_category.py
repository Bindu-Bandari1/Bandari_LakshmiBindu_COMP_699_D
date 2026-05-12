from database.db import execute_query, fetch_all, fetch_one


class TextileCategory:
    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name

    # -----------------------------
    # create new category
    # -----------------------------
    @staticmethod
    def create(category_name):
        query = """
        INSERT INTO textile_category (category_name)
        VALUES (?)
        """
        return execute_query(query, (category_name,))

    # -----------------------------
    # get all categories
    # -----------------------------
    @staticmethod
    def get_all():
        query = "SELECT * FROM textile_category"
        return fetch_all(query)

    # -----------------------------
    # get category by id
    # -----------------------------
    @staticmethod
    def get_by_id(category_id):
        query = "SELECT * FROM textile_category WHERE category_id = ?"
        data = fetch_one(query, (category_id,))

        if data:
            return TextileCategory(
                data["category_id"],
                data["category_name"]
            )
        return None

    # -----------------------------
    # update category
    # -----------------------------
    def update(self, new_name):
        query = """
        UPDATE textile_category
        SET category_name = ?
        WHERE category_id = ?
        """
        execute_query(query, (new_name, self.category_id))
        self.category_name = new_name

    # -----------------------------
    # delete category
    # -----------------------------
    def delete(self):
        query = "DELETE FROM textile_category WHERE category_id = ?"
        execute_query(query, (self.category_id,))