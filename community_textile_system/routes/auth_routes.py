from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_service import register_household, login_user, reset_password

auth_bp = Blueprint('auth', __name__)


# -----------------------------
# register (household only)
# -----------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        address = request.form.get('address')
        phone_number = request.form.get('phone_number')

        # basic validation
        if not all([name, email, password, address, phone_number]):
            flash("All fields are required")
            return redirect(url_for('auth.register'))

        user_id, message = register_household(
            name,
            email,
            password,
            address,
            phone_number
        )

        if user_id:
            flash("Registration successful. Please login.")
            return redirect(url_for('auth.login'))
        else:
            flash(message)

    return render_template('register.html')


# -----------------------------
# login (all roles)
# -----------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Please enter email and password")
            return redirect(url_for('auth.login'))

        user, message = login_user(email, password)

        if user:
            # store session
            session['user_id'] = user.user_id
            session['role'] = user.role

            # redirect based on role
            if user.role == 'household':
                return redirect(url_for('household.dashboard'))
            elif user.role == 'staff':
                return redirect(url_for('staff.dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
        else:
            flash(message)

    return render_template('login.html')


# -----------------------------
# logout
# -----------------------------
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully")
    return redirect(url_for('auth.login'))


# -----------------------------
# reset password
# -----------------------------
@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        user_id = session.get('user_id')
        new_password = request.form.get('password')

        if not user_id:
            flash("Session expired. Please login again.")
            return redirect(url_for('auth.login'))

        if not new_password:
            flash("Please enter a new password")
            return redirect(url_for('auth.reset'))

        message = reset_password(user_id, new_password)
        flash(message)

        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')