import bcrypt
import json
from dataclasses import dataclass
from services.db import admins_col


@dataclass
class Admin:
    email: str          # Key / unique index in DB
    name: str
    password_hash: str  # bcrypt hash — never store the raw password
    role: str = "admin"

# Generate JSON for an admin user
def generate_admin_json():
    password = ""  # Replace with the actual password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    admin_user = Admin(
        email="",       # Change this
        name="Tom Weaver Admin",
        password_hash=password_hash,
        role="admin"
    )

    admin_json = json.dumps(admin_user.__dict__, indent=4)
    #print(admin_json)
    #create_admin_account(admin_json)

def create_admin_account(admin_json: str):
    data = json.loads(admin_json)
    col = admins_col()

    if col.find_one({"email": data["email"]}):
        raise ValueError(f"Admin with email '{data['email']}' already exists.")

    col.insert_one(data)
    print(f"Admin account created for {data['email']}")

