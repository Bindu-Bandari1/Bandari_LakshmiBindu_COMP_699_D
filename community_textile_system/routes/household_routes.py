from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.request_service import (
    create_request,
    get_user_requests,
    get_request_details,
    edit_request,
    cancel_request,
    search_requests,
    get_request_history
)
from services.item_service import (
    add_item_with_ml,
    get_items,
    confirm_item_path,
    get_item_result
)
from services.scheduling_service import get_user_schedule

household_bp = Blueprint('household', __name__)


# -----------------------------
# helper: check household role
# -----------------------------
def check_household():
    return session.get('role') == 'household'


# -----------------------------
# dashboard
# -----------------------------
@household_bp.route('/household/dashboard')
def dashboard():
    if not check_household():
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    requests = get_user_requests(user_id)

    return render_template(
        'dashboard_household.html',
        requests=requests
    )


# -----------------------------
# create request
# -----------------------------
@household_bp.route('/household/create-request', methods=['GET', 'POST'])
def create():
    if not check_household():
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        user_id = session.get('user_id')
        request_type = request.form['request_type']

        request_id = create_request(user_id, request_type)

        return redirect(url_for('household.add_item', request_id=request_id))

    return render_template('create_request.html')


# -----------------------------
# add item (STEP 2)
# -----------------------------
@household_bp.route('/household/add-item/<int:request_id>', methods=['GET', 'POST'])
def add_item(request_id):
    if not check_household():
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        item_type = request.form['item_type']
        quantity = request.form['quantity']
        note = request.form['note']
        file = request.files['photo']

        result = add_item_with_ml(request_id, item_type, quantity, note, file)

        return redirect(url_for(
            'household.result',
            item_id=result["item_id"]
        ))

    return render_template(
        'upload_item.html',
        request_id=request_id
    )


# -----------------------------
# RESULT PAGE (STEP 3)
# -----------------------------
@household_bp.route('/household/result/<int:item_id>')
def result(item_id):
    if not check_household():
        return redirect(url_for('auth.login'))

    result = get_item_result(item_id)

    if not result:
        flash("Result not found")
        return redirect(url_for('household.dashboard'))

    return render_template(
        'result.html',
        photo_path=result["photo_path"],
        condition_label=result["condition_label"],
        confidence=result["confidence"]
    )


# -----------------------------
# view requests
# -----------------------------
@household_bp.route('/household/requests')
def view_requests():
    if not check_household():
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    requests = get_user_requests(user_id)

    return render_template(
        'view_requests.html',
        requests=requests
    )


# -----------------------------
# 🔥 FIXED: request details
# -----------------------------
@household_bp.route('/household/request/<int:request_id>')
def request_details(request_id):
    if not check_household():
        return redirect(url_for('auth.login'))

    data = get_request_details(request_id)

    # ✅ FIX: pass requests also
    return render_template(
        'view_requests.html',
        requests=[data["request"]],   # 🔥 IMPORTANT FIX
        data=data
    )


# -----------------------------
# edit request
# -----------------------------
@household_bp.route('/household/edit/<int:request_id>', methods=['POST'])
def edit(request_id):
    if not check_household():
        return redirect(url_for('auth.login'))

    new_type = request.form['request_type']

    if edit_request(request_id, new_type):
        flash("Request updated")
    else:
        flash("Cannot edit request")

    return redirect(url_for('household.view_requests'))


# -----------------------------
# cancel request
# -----------------------------
@household_bp.route('/household/cancel/<int:request_id>')
def cancel(request_id):
    if not check_household():
        return redirect(url_for('auth.login'))

    cancel_request(request_id)
    flash("Request cancelled")

    return redirect(url_for('household.view_requests'))


# -----------------------------
# search
# -----------------------------
@household_bp.route('/household/search', methods=['POST'])
def search():
    if not check_household():
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    keyword = request.form['keyword']

    results = search_requests(user_id, keyword)

    return render_template(
        'view_requests.html',
        requests=results
    )


# -----------------------------
# history
# -----------------------------
@household_bp.route('/household/history')
def history():
    if not check_household():
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    history = get_request_history(user_id)

    return render_template(
        'household_history.html',
        history=history
    )


# -----------------------------
# schedule
# -----------------------------
@household_bp.route('/household/schedule')
def schedule():
    if not check_household():
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    schedule = get_user_schedule(user_id)

    return render_template(
        'household_schedule.html',
        schedule=schedule
    )


# -----------------------------
# confirm handling path
# -----------------------------
@household_bp.route('/household/confirm/<int:item_id>', methods=['POST'])
def confirm_path(item_id):
    if not check_household():
        return redirect(url_for('auth.login'))

    path = request.form['path']

    confirm_item_path(item_id, path)
    flash("Handling path confirmed")

    return redirect(url_for('household.view_requests'))