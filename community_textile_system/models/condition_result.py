from database.db import execute_query, fetch_one


class ConditionResult:
    def __init__(self, result_id, item_id, condition_label,
                 confidence_score, model_version, processed_at):
        self.result_id = result_id
        self.item_id = item_id
        self.condition_label = condition_label
        self.confidence_score = confidence_score
        self.model_version = model_version
        self.processed_at = processed_at

    # -----------------------------
    # create condition result (ML output)
    # -----------------------------
    @staticmethod
    def create(item_id, condition_label, confidence_score, model_version="v1"):
        query = """
        INSERT INTO condition_result (item_id, condition_label, confidence_score, model_version)
        VALUES (?, ?, ?, ?)
        """
        return execute_query(query, (item_id, condition_label, confidence_score, model_version))

    # -----------------------------
    # get result by item_id
    # -----------------------------
    @staticmethod
    def get_by_item(item_id):
        query = """
        SELECT * FROM condition_result
        WHERE item_id = ?
        """

        data = fetch_one(query, (item_id,))

        if data:
            return ConditionResult(
                data["result_id"],
                data["item_id"],
                data["condition_label"],
                data["confidence_score"],
                data["model_version"],
                data["processed_at"]
            )

        return None

    # -----------------------------
    # update result (re-processing)
    # -----------------------------
    def update_result(self, new_label, new_confidence):
        query = """
        UPDATE condition_result
        SET condition_label = ?, confidence_score = ?
        WHERE result_id = ?
        """

        execute_query(query, (new_label, new_confidence, self.result_id))

        # update object values
        self.condition_label = new_label
        self.confidence_score = new_confidence

    # -----------------------------
    # convert to dictionary (useful for APIs/UI)
    # -----------------------------
    def to_dict(self):
        return {
            "result_id": self.result_id,
            "item_id": self.item_id,
            "condition_label": self.condition_label,
            "confidence_score": self.confidence_score,
            "model_version": self.model_version,
            "processed_at": self.processed_at
        }