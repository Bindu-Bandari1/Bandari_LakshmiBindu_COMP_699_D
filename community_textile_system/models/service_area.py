from database.db import execute_query, fetch_all, fetch_one


class ServiceArea:
    def __init__(self, area_id, area_name):
        self.area_id = area_id
        self.area_name = area_name

    # -----------------------------
    # create new service area
    # -----------------------------
    @staticmethod
    def create(area_name):
        query = """
        INSERT INTO service_area (area_name)
        VALUES (?)
        """
        return execute_query(query, (area_name,))

    # -----------------------------
    # get all service areas
    # -----------------------------
    @staticmethod
    def get_all():
        query = "SELECT * FROM service_area"
        return fetch_all(query)

    # -----------------------------
    # get area by id
    # -----------------------------
    @staticmethod
    def get_by_id(area_id):
        query = "SELECT * FROM service_area WHERE area_id = ?"
        data = fetch_one(query, (area_id,))

        if data:
            return ServiceArea(
                data["area_id"],
                data["area_name"]
            )
        return None

    # -----------------------------
    # update service area name
    # -----------------------------
    def update(self, new_name):
        query = """
        UPDATE service_area
        SET area_name = ?
        WHERE area_id = ?
        """
        execute_query(query, (new_name, self.area_id))
        self.area_name = new_name

    # -----------------------------
    # delete service area
    # -----------------------------
    def delete(self):
        query = "DELETE FROM service_area WHERE area_id = ?"
        execute_query(query, (self.area_id,))