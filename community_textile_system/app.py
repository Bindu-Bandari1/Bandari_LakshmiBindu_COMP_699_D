from flask import Flask, redirect, send_from_directory
from routes.auth_routes import auth_bp
from routes.household_routes import household_bp
from routes.staff_routes import staff_bp
from routes.admin_routes import admin_bp
from database.db import init_db
import os


def create_app():
    app = Flask(__name__)

    # -----------------------------
    # BASE DIRECTORY (IMPORTANT FIX)
    # -----------------------------
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # -----------------------------
    # SECRET KEY
    # -----------------------------
    app.secret_key = "your_secret_key_here"

    # -----------------------------
    # UPLOAD FOLDER CONFIG (SAFE PATH)
    # -----------------------------
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Create uploads folder if not exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # -----------------------------
    # 🔥 SERVE UPLOADED FILES (CRITICAL)
    # -----------------------------
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # -----------------------------
    # DEFAULT ROUTE
    # -----------------------------
    @app.route('/')
    def home():
        return redirect('/login')

    # -----------------------------
    # REGISTER BLUEPRINTS
    # -----------------------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(household_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(admin_bp)

    return app


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(BASE_DIR, "database", "app.db")

    if not os.path.exists(db_path):
        init_db()
        print("Database created successfully")

    app = create_app()
    app.run(debug=True)