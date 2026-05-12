from models.request import Request
from models.item import Item
from database.db import execute_query, fetch_all, fetch_one


# -----------------------------
# create new request (household)
# -----------------------------
def create_request(user_id, request_type):
    query = """
    INSERT INTO request (user_id, request_type, status)
    VALUES (?, ?, 'PENDING')
    """
    return execute_query(query, (user_id, request_type))


# -----------------------------
# add item to request
# -----------------------------
def add_item_to_request(request_id, item_type, quantity, note, photo_path):
    return Item.create(request_id, item_type, quantity, note, photo_path)


# -----------------------------
# get all requests for a user
# -----------------------------
def get_user_requests(user_id):
    return Request.get_by_user(user_id)


# -----------------------------
# get request details
# -----------------------------
def get_request_details(request_id):
    request = Request.get_by_id(request_id)
    items = Item.get_by_request(request_id)

    return {
        "request": request,
        "items": items
    }


# -----------------------------
# edit request
# -----------------------------
def edit_request(request_id, new_type):
    request = Request.get_by_id(request_id)

    if request and request.is_editable():
        query = """
        UPDATE request
        SET request_type = ?
        WHERE request_id = ?
        """
        execute_query(query, (new_type, request_id))
        return True

    return False


# -----------------------------
# cancel request
# -----------------------------
def cancel_request(request_id):
    request = Request.get_by_id(request_id)

    if request:
        request.cancel()
        return True

    return False


# =========================================================
# 🔥 MAIN FUNCTION FOR STAFF (MOST IMPORTANT)
# =========================================================
def get_staff_visible_requests(staff_id):
    query = """
    SELECT 
        r.request_id,
        r.request_type,
        r.status,
        r.created_at,
        r.assigned_staff_id,
        r.scheduled_time,

        u.name AS user_name,
        u.email,

        h.address,
        h.phone_number,

        i.item_id,
        i.item_type,
        i.quantity,
        i.photo_path,

        c.condition_label,
        c.confidence_score

    FROM request r
    JOIN users u ON r.user_id = u.user_id
    JOIN household h ON r.user_id = h.user_id

    LEFT JOIN item i ON r.request_id = i.request_id
    LEFT JOIN condition_result c ON i.item_id = c.item_id

    WHERE 
        r.status = 'PENDING'
        OR r.assigned_staff_id = ?

    ORDER BY r.created_at DESC
    """

    return fetch_all(query, (staff_id,))


# -----------------------------
# accept request
# -----------------------------
def accept_request(request_id, staff_id):
    query = """
    UPDATE request
    SET assigned_staff_id = ?, status = 'ACCEPTED'
    WHERE request_id = ?
    """
    execute_query(query, (staff_id, request_id))
    return True


# -----------------------------
# schedule pickup
# -----------------------------
def schedule_request(request_id, time):
    query = """
    UPDATE request
    SET scheduled_time = ?, status = 'SCHEDULED'
    WHERE request_id = ?
    """
    execute_query(query, (time, request_id))
    return True


# -----------------------------
# update status
# -----------------------------
def update_request_status(request_id, status):
    query = """
    UPDATE request
    SET status = ?
    WHERE request_id = ?
    """
    execute_query(query, (status, request_id))
    return True


# -----------------------------
# search requests
# -----------------------------
def search_requests(user_id, keyword):
    query = """
    SELECT * FROM request
    WHERE user_id = ? AND request_type LIKE ?
    """
    return fetch_all(query, (user_id, f"%{keyword}%"))


# -----------------------------
# request history
# -----------------------------
def get_request_history(user_id):
    query = """
    SELECT * FROM request
    WHERE user_id = ?
    AND status IN ('COMPLETED', 'REJECTED', 'CANCELLED')
    ORDER BY created_at DESC
    """
    return fetch_all(query, (user_id,))