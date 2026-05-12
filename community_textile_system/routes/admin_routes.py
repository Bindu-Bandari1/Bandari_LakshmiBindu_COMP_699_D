from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.admin_service import (
    create_service_area,
    get_service_areas,
    create_category,
    get_categories,
    create_staff,
    approve_staff,
    get_all_staff,
    get_all_requests
)

admin_bp = Blueprint('admin', __name__)


# -----------------------------
# helper: admin access check
# -----------------------------
def check_admin():
    if session.get('role') != 'admin':
        return False
    return True


# -----------------------------
# dashboard (ONLY overview)
# -----------------------------
@admin_bp.route('/admin/dashboard')
def dashboard():
    if not check_admin():
        return redirect(url_for('auth.login'))

    requests = get_all_requests()
    staff = get_all_staff()

    return render_template(
        'dashboard_admin.html',
        requests=requests,
        staff=staff
    )


# -----------------------------
# SERVICE AREAS PAGE
# -----------------------------
@admin_bp.route('/admin/areas')
def view_areas():
    if not check_admin():
        return redirect(url_for('auth.login'))

    areas = get_service_areas()

    return render_template(
        'admin_areas.html',
        areas=areas
    )


# -----------------------------
# create service area
# -----------------------------
@admin_bp.route('/admin/create-area', methods=['POST'])
def create_area():
    if not check_admin():
        return redirect(url_for('auth.login'))

    area_name = request.form['area_name']

    create_service_area(area_name)
    flash("Service area created successfully")

    return redirect(url_for('admin.view_areas'))


# -----------------------------
# CATEGORIES PAGE
# -----------------------------
@admin_bp.route('/admin/categories')
def view_categories():
    if not check_admin():
        return redirect(url_for('auth.login'))

    categories = get_categories()

    return render_template(
        'admin_categories.html',
        categories=categories
    )


# -----------------------------
# create category
# -----------------------------
@admin_bp.route('/admin/create-category', methods=['POST'])
def create_cat():
    if not check_admin():
        return redirect(url_for('auth.login'))

    category_name = request.form['category_name']

    create_category(category_name)
    flash("Category added successfully")

    return redirect(url_for('admin.view_categories'))


# -----------------------------
# STAFF PAGE
# -----------------------------
@admin_bp.route('/admin/staff')
def view_staff():
    if not check_admin():
        return redirect(url_for('auth.login'))

    staff = get_all_staff()

    return render_template(
        'admin_staff.html',
        staff=staff
    )


# -----------------------------
# create pickup staff
# -----------------------------
@admin_bp.route('/admin/create-staff', methods=['POST'])
def create_staff_route():
    if not check_admin():
        return redirect(url_for('auth.login'))

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    staff_id = request.form['staff_id']
    area_id = request.form['area_id']

    user_id, message = create_staff(name, email, password, staff_id, area_id)
    flash(message)

    return redirect(url_for('admin.view_staff'))


# -----------------------------
# approve staff
# -----------------------------
@admin_bp.route('/admin/approve/<int:user_id>')
def approve(user_id):
    if not check_admin():
        return redirect(url_for('auth.login'))

    approve_staff(user_id)
    flash("Staff approved successfully")

    return redirect(url_for('admin.view_staff'))


# -----------------------------
# REQUESTS PAGE
# -----------------------------
@admin_bp.route('/admin/requests')
def view_requests():
    if not check_admin():
        return redirect(url_for('auth.login'))

    requests = get_all_requests()

    return render_template(
        'admin_requests.html',
        requests=requests
    )