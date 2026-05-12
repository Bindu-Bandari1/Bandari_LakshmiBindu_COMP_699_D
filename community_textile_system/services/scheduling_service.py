from database.db import fetch_all, execute_query, fetch_one
from datetime import datetime


# -----------------------------
# convert HTML datetime to DB format
# -----------------------------
def normalize_time(time_str):
    try:
        # convert "2026-04-23T14:30" → "2026-04-23 14:30"
        dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return None


# -----------------------------
# check if time slot is available
# -----------------------------
def is_time_available(staff_id, proposed_time):
    query = """
    SELECT * FROM request
    WHERE assigned_staff_id = ?
    AND scheduled_time = ?
    AND status IN ('SCHEDULED', 'ACCEPTED')
    """
    existing = fetch_all(query, (staff_id, proposed_time))

    return len(existing) == 0


# -----------------------------
# check if request belongs to staff
# -----------------------------
def is_request_assigned(request_id, staff_id):
    query = """
    SELECT * FROM request
    WHERE request_id = ? AND assigned_staff_id = ?
    """
    return fetch_one(query, (request_id, staff_id)) is not None


# -----------------------------
# assign schedule safely
# -----------------------------
def assign_schedule(request_id, staff_id, proposed_time):
    # normalize time
    formatted_time = normalize_time(proposed_time)

    if not formatted_time:
        return False, "Invalid time format"

    # check ownership
    if not is_request_assigned(request_id, staff_id):
        return False, "Unauthorized action"

    # check availability
    if not is_time_available(staff_id, formatted_time):
        return False, "Time slot not available"

    query = """
    UPDATE request
    SET scheduled_time = ?, status = 'SCHEDULED'
    WHERE request_id = ? AND assigned_staff_id = ?
    """
    execute_query(query, (formatted_time, request_id, staff_id))

    return True, "Scheduled successfully"


# -----------------------------
# get schedule for staff
# -----------------------------
def get_staff_schedule(staff_id):
    query = """
    SELECT * FROM request
    WHERE assigned_staff_id = ?
    AND scheduled_time IS NOT NULL
    ORDER BY scheduled_time
    """
    return fetch_all(query, (staff_id,))


# -----------------------------
# get schedule for household
# -----------------------------
def get_user_schedule(user_id):
    query = """
    SELECT * FROM request
    WHERE user_id = ?
    AND scheduled_time IS NOT NULL
    ORDER BY scheduled_time
    """
    return fetch_all(query, (user_id,))