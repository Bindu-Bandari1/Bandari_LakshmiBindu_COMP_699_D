from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.request_service import (
    get_staff_visible_requests,   # ✅ UPDATED
    accept_request,
    update_request_status
)
from services.scheduling_service import assign_schedule, get_staff_schedule
from models.pickup_staff import PickupStaff

staff_bp = Blueprint('staff', __name__)


# -----------------------------
# helper: enforce staff login
# -----------------------------
def require_staff():
    return session.get('role') == 'staff'


# -----------------------------
# dashboard (overview)
# -----------------------------
@staff_bp.route('/staff/dashboard')
def dashboard():
    if not require_staff():
        return redirect(url_for('auth.login'))

    staff_id = session.get('user_id')

    requests = get_staff_visible_requests(staff_id)   # ✅ FIX

    return render_template(
        'dashboard_staff.html',
        requests=requests
    )


# -----------------------------
# requests page (MAIN WORK PAGE)
# -----------------------------
@staff_bp.route('/staff/requests')
def view_requests():
    if not require_staff():
        return redirect(url_for('auth.login'))

    staff_id = session.get('user_id')

    requests = get_staff_visible_requests(staff_id)   # ✅ FIX

    return render_template(
        'staff_requests.html',
        requests=requests
    )


# -----------------------------
# accept request
# -----------------------------
@staff_bp.route('/staff/accept/<int:request_id>')
def accept(request_id):
    if not require_staff():
        return redirect(url_for('auth.login'))

    staff_id = session.get('user_id')

    if not staff_id:
        flash("Session expired. Please login again.")
        return redirect(url_for('auth.login'))

    if accept_request(request_id, staff_id):
        flash("Request accepted successfully")
    else:
        flash("Unable to accept request")

    return redirect(url_for('staff.view_requests'))


# -----------------------------
# assign schedule
# -----------------------------
@staff_bp.route('/staff/schedule/<int:request_id>', methods=['POST'])
def schedule(request_id):
    if not require_staff():
        return redirect(url_for('auth.login'))

    staff_id = session.get('user_id')
    time = request.form.get('time')

    if not time:
        flash("Please select a valid time")
        return redirect(url_for('staff.view_requests'))

    success, message = assign_schedule(request_id, staff_id, time)
    flash(message)

    return redirect(url_for('staff.view_requests'))


# -----------------------------
# update request status
# -----------------------------
@staff_bp.route('/staff/status/<int:request_id>', methods=['POST'])
def update_status(request_id):
    if not require_staff():
        return redirect(url_for('auth.login'))

    status = request.form.get('status')

    if not status:
        flash("Invalid status update")
        return redirect(url_for('staff.view_requests'))

    if update_request_status(request_id, status):
        flash("Status updated successfully")
    else:
        flash("Update failed")

    return redirect(url_for('staff.view_requests'))


# -----------------------------
# schedule page
# -----------------------------
@staff_bp.route('/staff/my-schedule')
def my_schedule():
    if not require_staff():
        return redirect(url_for('auth.login'))

    staff_id = session.get('user_id')

    schedule = get_staff_schedule(staff_id)

    return render_template(
        'staff_schedule.html',
        schedule=schedule
    )


# -----------------------------
# override handling path
# -----------------------------
@staff_bp.route('/staff/override/<int:item_id>', methods=['POST'])
def override(item_id):
    if not require_staff():
        return redirect(url_for('auth.login'))

    new_path = request.form.get('path')
    reason = request.form.get('reason')

    if not new_path:
        flash("Invalid override data")
        return redirect(url_for('staff.view_requests'))

    staff = PickupStaff(session.get('user_id'), "", "", "", "", None, 1)
    staff.override_handling_path(item_id, new_path, reason)

    flash("Handling path overridden")

    return redirect(url_for('staff.view_requests'))


# -----------------------------
# mark as completed
# -----------------------------
@staff_bp.route('/staff/received/<int:request_id>')
def received(request_id):
    if not require_staff():
        return redirect(url_for('auth.login'))

    staff = PickupStaff(session.get('user_id'), "", "", "", "", None, 1)
    staff.mark_received(request_id)

    flash("Marked as completed")

    return redirect(url_for('staff.view_requests'))


# -----------------------------
# mark as rejected
# -----------------------------
@staff_bp.route('/staff/rejected/<int:request_id>')
def rejected(request_id):
    if not require_staff():
        return redirect(url_for('auth.login'))

    staff = PickupStaff(session.get('user_id'), "", "", "", "", None, 1)
    staff.mark_rejected(request_id)

    flash("Marked as rejected")

    return redirect(url_for('staff.view_requests'))