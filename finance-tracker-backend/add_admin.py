from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User(
        username="admin",
        name="Admin",
        email="admin@example.com",
        password_hash=generate_password_hash("admin123"),  # Securely hash password
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()

    print("Admin user created successfully!")


with app.app_context():
    admin = User.query.filter_by(username="admin").first()
    print(admin.username, admin.email, admin.is_admin)