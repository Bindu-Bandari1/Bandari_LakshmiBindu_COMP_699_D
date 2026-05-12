import os
from models.item import Item
from models.condition_result import ConditionResult
from models.handling_path import HandlingPath
from services.ml_service import predict_condition


UPLOAD_FOLDER = "uploads"


# -----------------------------
# save uploaded file
# -----------------------------
def save_file(file, filename):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    return file_path


# -----------------------------
# add item + run ML prediction
# -----------------------------
def add_item_with_ml(request_id, item_type, quantity, note, file):
    # save file
    filename = file.filename
    photo_path = save_file(file, filename)

    # create item
    item_id = Item.create(request_id, item_type, quantity, note, photo_path)

    # run ML model
    condition_label, confidence = predict_condition(photo_path)

    # store condition result (uses confidence_score internally)
    result_id = ConditionResult.create(item_id, condition_label, confidence)

    # create handling path (AI suggestion)
    HandlingPath.create(result_id, condition_label)

    # return data for UI redirect
    return {
        "item_id": item_id,
        "condition_label": condition_label,
        "confidence": confidence,
        "photo_path": photo_path
    }


# -----------------------------
# get items for a request
# -----------------------------
def get_items(request_id):
    return Item.get_by_request(request_id)


# -----------------------------
# get single item with ML result (FIXED)
# -----------------------------
def get_item_result(item_id):
    from database.db import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT i.photo_path, c.condition_label, c.confidence_score
        FROM item i
        JOIN condition_result c ON i.item_id = c.item_id
        WHERE i.item_id = ?
    """, (item_id,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "photo_path": row[0],
            "condition_label": row[1],
            "confidence": row[2]  # UI expects this key
        }

    return None


# -----------------------------
# update item details
# -----------------------------
def update_item(item_id, item_type, quantity, note):
    item = Item.get_by_id(item_id)

    if item:
        item.update_item(item_type, quantity, note)
        return True

    return False


# -----------------------------
# update item photo
# -----------------------------
def update_item_photo(item_id, file):
    item = Item.get_by_id(item_id)

    if item:
        filename = file.filename
        photo_path = save_file(file, filename)

        item.update_photo(photo_path)
        return True

    return False


# -----------------------------
# confirm handling path
# -----------------------------
def confirm_item_path(item_id, path):
    item = Item.get_by_id(item_id)

    if item:
        item.set_confirmed_path(path)
        return True

    return False