from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask_bcrypt import Bcrypt
import re
from datetime import datetime, timedelta


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

app.secret_key = "secure-login-system-2026"

bcrypt = Bcrypt(app)


# Maximum failed attempts
MAX_ATTEMPTS = 5

# Lock account for 2 minutes
LOCK_TIME = timedelta(minutes=2)

# Store failed attempts in memory
login_attempts = {}


# ---------------- DATABASE ----------------

def get_db_connection():

    connection = sqlite3.connect("users.db")

    connection.row_factory = sqlite3.Row

    return connection


# ---------------- SECURITY LOG ----------------

def add_security_log(email, activity):

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO security_logs (email, activity)
        VALUES (?, ?)
        """,
        (email, activity)
    )

    connection.commit()
    connection.close()


# ---------------- HOME ----------------

@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Empty field validation
        if not username or not email or not password or not confirm_password:

            return render_template(
                "register.html",
                error="All fields are required!"
            )

        # Username validation
        if len(username) < 3:

            return render_template(
                "register.html",
                error="Username must contain at least 3 characters!"
            )

        # Email validation
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(email_pattern, email):

            return render_template(
                "register.html",
                error="Please enter a valid email address!"
            )

        # Confirm password
        if password != confirm_password:

            return render_template(
                "register.html",
                error="Passwords do not match!"
            )

        # Password length
        if len(password) < 8:

            return render_template(
                "register.html",
                error="Password must contain at least 8 characters!"
            )

        # Password strength
        has_upper = bool(re.search(r"[A-Z]", password))
        has_lower = bool(re.search(r"[a-z]", password))
        has_digit = bool(re.search(r"\d", password))
        has_special = bool(re.search(r"[^A-Za-z0-9]", password))

        if not has_upper or not has_lower or not has_digit or not has_special:

            return render_template(
                "register.html",
                error="Password must contain uppercase, lowercase, number and special character!"
            )

        # Bcrypt hash
        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        connection = get_db_connection()

        try:

            connection.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
                """,
                (username, email, hashed_password)
            )

            connection.commit()

        except sqlite3.IntegrityError:

            connection.close()

            return render_template(
                "register.html",
                error="Email is already registered!"
            )

        connection.close()

        add_security_log(
            email,
            "Account registered successfully"
        )

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:

            return render_template(
                "login.html",
                error="Email and password are required!"
            )

        current_time = datetime.now()

        # Check temporary lock
        if email in login_attempts:

            attempt_data = login_attempts[email]

            if attempt_data["blocked_until"]:

                if current_time < attempt_data["blocked_until"]:

                    remaining = int(
                        (
                            attempt_data["blocked_until"]
                            - current_time
                        ).total_seconds()
                    )

                    return render_template(
                        "login.html",
                        error=f"Too many failed attempts. Try again in {remaining} seconds."
                    )

                else:

                    login_attempts[email] = {
                        "count": 0,
                        "blocked_until": None
                    }

        # Get user
        connection = get_db_connection()

        user = connection.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        connection.close()

        # Verify password
        if user and bcrypt.check_password_hash(
            user["password"],
            password
        ):

            # Reset failed attempts
            login_attempts.pop(email, None)

            session.clear()

            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["email"] = user["email"]

            add_security_log(
                email,
                "Successful login"
            )

            return redirect(url_for("dashboard"))

        # Failed login
        if email not in login_attempts:

            login_attempts[email] = {
                "count": 0,
                "blocked_until": None
            }

        login_attempts[email]["count"] += 1

        failed_count = login_attempts[email]["count"]

        add_security_log(
            email,
            f"Failed login attempt #{failed_count}"
        )

        # Block after maximum attempts
        if failed_count >= MAX_ATTEMPTS:

            login_attempts[email]["blocked_until"] = (
                current_time + LOCK_TIME
            )

            add_security_log(
                email,
                "Login temporarily blocked"
            )

            return render_template(
                "login.html",
                error="Too many failed attempts. Login blocked for 2 minutes."
            )

        return render_template(
            "login.html",
            error=f"Invalid email or password! Attempt {failed_count}/{MAX_ATTEMPTS}"
        )

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"],
        email=session["email"]
    )


# ---------------- SECURITY LOGS ----------------

@app.route("/security-logs")
def security_logs():

    if "user_id" not in session:

        return redirect(url_for("login"))

    connection = get_db_connection()

    logs = connection.execute(
        """
        SELECT * FROM security_logs
        WHERE email = ?
        ORDER BY timestamp DESC
        """,
        (session["email"],)
    ).fetchall()

    connection.close()

    return render_template(
        "security_logs.html",
        logs=logs
    )


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    email = session.get("email")

    if email:

        add_security_log(
            email,
            "User logged out"
        )

    session.clear()

    return redirect(url_for("login"))


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)