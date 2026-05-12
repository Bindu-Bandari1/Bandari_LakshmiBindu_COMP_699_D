from database.db import execute_query
from werkzeug.security import generate_password_hash

# admin details
name = "Bandari Admin"
email = "admin@bandari.com"
password = generate_password_hash("bandari123")  # change if needed

# insert admin
query = """
INSERT INTO users (name, email, password, role)
VALUES (?, ?, ?, 'admin')
"""

execute_query(query, (name, email, password))

print("Admin created successfully!")