import streamlit as st
import json
import random
import string
from pathlib import Path
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Bank Management System", page_icon="🏦")

DATA_FILE = "data.json"

# ---------------- JSON HANDLING ----------------
def load_data():
    if Path(DATA_FILE).exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"users": [], "admin": {"username": "admin", "password": "admin123"}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "db" not in st.session_state:
    st.session_state.db = load_data()

# ---------------- UTILITIES ----------------
def generate_account():
    chars = random.choices(string.ascii_letters + string.digits, k=8)
    return "".join(chars)

def find_user(acc, pin):
    for u in st.session_state.db["users"]:
        if u["accountNumber"] == acc and u["pin"] == pin and not u["isDeleted"]:
            return u
    return None

def add_transaction(user, t_type, amount):
    user["transactions"].append({
        "type": t_type,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "balance": user["balance"]
    })

# ---------------- UI ----------------
st.title("🏦 Bank Management System")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Account Details",
        "Transaction History",
        "Delete Account",
        "Admin Panel"
    ]
)

# ---------------- CREATE ACCOUNT ----------------
if menu == "Create Account":
    st.subheader("🆕 Create Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    pin = st.text_input("4 Digit PIN", type="password")

    if st.button("Create"):
        if age < 18:
            st.error("Account can be created only if age is 18 or above")
        elif not phone.isdigit() or len(phone) != 10:
            st.error("Phone must be 10 digits")
        elif not pin.isdigit() or len(pin) != 4:
            st.error("PIN must be 4 digits")
        else:
            acc = generate_account()
            user = {
                "name": name,
                "age": age,
                "phoneNumber": int(phone),
                "email": email,
                "accountNumber": acc,
                "pin": int(pin),
                "balance": 0,
                "status": "Active",
                "isDeleted": False,
                "transactions": []
            }
            st.session_state.db["users"].append(user)
            save_data(st.session_state.db)

            st.success("Account Created Successfully")
            st.info(f"Account Number: {acc}")

# ---------------- DEPOSIT ----------------
elif menu == "Deposit Money":
    st.subheader("💰 Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        if acc and pin and pin.isdigit():
            user = find_user(acc, int(pin))
            if not user:
                st.error("Invalid credentials")
            elif user["status"] == "Blocked":
                st.error("Account is blocked")
            else:
                user["balance"] += amount
                add_transaction(user, "Deposit", amount)
                save_data(st.session_state.db)
                st.success("Amount Deposited")
                st.info(f"Balance: ₹{user['balance']}")
        else:
            st.warning("Enter valid inputs")

# ---------------- WITHDRAW ----------------
elif menu == "Withdraw Money":
    st.subheader("🏧 Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        if acc and pin and pin.isdigit():
            user = find_user(acc, int(pin))
            if not user:
                st.error("Invalid credentials")
            elif user["status"] == "Blocked":
                st.error("Account is blocked")
            elif amount > user["balance"]:
                st.error("Insufficient balance")
            else:
                user["balance"] -= amount
                add_transaction(user, "Withdraw", amount)
                save_data(st.session_state.db)
                st.success("Amount Withdrawn")
                st.info(f"Balance: ₹{user['balance']}")
        else:
            st.warning("Enter valid inputs")

# ---------------- DETAILS ----------------
elif menu == "Account Details":
    st.subheader("📄 Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("View"):
        if acc and pin and pin.isdigit():
            user = find_user(acc, int(pin))
            if user:
                st.json(user)
            else:
                st.error("Invalid credentials")
        else:
            st.warning("Enter valid inputs")

# ---------------- TRANSACTIONS ----------------
elif menu == "Transaction History":
    st.subheader("📜 Transaction History")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Show History"):
        if acc and pin and pin.isdigit():
            user = find_user(acc, int(pin))
            if user:
                if user["transactions"]:
                    st.table(user["transactions"])
                else:
                    st.info("No transactions found")
            else:
                st.error("Invalid credentials")
        else:
            st.warning("Enter valid inputs")

# ---------------- DELETE ACCOUNT ----------------
elif menu == "Delete Account":
    st.subheader("❌ Delete Account (Soft Delete)")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete Account"):
        if not acc or not pin or not pin.isdigit():
            st.warning("⚠️ Please enter valid Account Number and PIN")
        else:
            user = find_user(acc, int(pin))

            if not user:
                st.error("❌ Invalid Account Number or PIN")
            else:
                user["isDeleted"] = True
                user["status"] = "Closed"
                save_data(st.session_state.db)

                st.success("✅ Account Closed Successfully")
                st.info("Your account is now permanently deactivated")

# ---------------- ADMIN PANEL ----------------
elif menu == "Admin Panel":
    st.subheader("👨‍💼 Admin Panel")

    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")

    if st.button("Login"):
        admin = st.session_state.db["admin"]
        if username == admin["username"] and password == admin["password"]:
            st.success("Admin Login Successful")

            users = st.session_state.db["users"]
            st.write("### All Accounts")
            st.table([
                {
                    "Name": u["name"],
                    "Account": u["accountNumber"],
                    "Balance": u["balance"],
                    "Status": u["status"]
                } for u in users if not u["isDeleted"]
            ])

            st.write("### Bank Statistics")
            st.info(f"Total Users: {len(users)}")
            st.info(f"Total Bank Balance: ₹{sum(u['balance'] for u in users)}")

        else:
            st.error("Invalid Admin Credentials")