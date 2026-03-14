from datetime import datetime
from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Create Database
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shop_name TEXT,
        mobile TEXT,
        password TEXT
    )
    """)

    # REQUEST TABLE
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS requests(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
amount INTEGER,
commission INTEGER,
note TEXT,
status TEXT DEFAULT 'Open',
accepted_by INTEGER,
created_at TEXT
)
""")

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return redirect("/login")

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == "POST":

        shop_name = request.form["shop_name"]
        mobile = request.form["mobile"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO users (shop_name, mobile, password) VALUES (?, ?, ?)",
        (shop_name, mobile, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        mobile = request.form["mobile"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
        "SELECT id, shop_name FROM users WHERE mobile=? AND password=?",
        (mobile,password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user_id"] = user[0]
            session["shop_name"] = user[1]
            session["user"] = mobile

            return redirect("/dashboard")

        else:
            return "Invalid Mobile or Password"

    return render_template("login.html")

    # Live Request Data

@app.route("/api/requests")
def api_requests():

    if "user_id" not in session:
        return {}

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
SELECT r.id, u.shop_name, r.amount, r.commission, r.status
FROM requests r
JOIN users u ON r.user_id = u.id
WHERE r.user_id != ? AND r.status='Open'
ORDER BY r.id DESC
""", (session["user_id"],))

    rows = c.fetchall()
    conn.close()

    data = []

    for r in rows:
        data.append({
    "id": r[0],
    "shop": r[1],
    "amount": r[2],
    "commission": r[3],
    "status": r[4]
})

    return {"requests": data}

# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    user_id = session["user_id"]

    # Requests created by me
    c.execute("""
    SELECT id, amount, commission, status
    FROM requests
    WHERE user_id = ?
    ORDER BY id DESC
""",(user_id,))
    my_requests = c.fetchall()

    # Requests accepted by me
    c.execute("""
    SELECT r.id, u.shop_name, r.amount, r.commission
    FROM requests r
    JOIN users u ON r.user_id = u.id
    WHERE r.accepted_by = ?
    ORDER BY r.id DESC
    """,(user_id,))
    accepted_requests = c.fetchall()

    # Available requests
    c.execute("""
    SELECT r.id, u.shop_name, r.amount, r.commission, r.status
    FROM requests r
    JOIN users u ON r.user_id = u.id
    WHERE r.user_id != ? AND r.status='Open'
    """,(user_id,))
    requests = c.fetchall()

    # Expense (commission paid)
    c.execute("""
    SELECT IFNULL(SUM(commission),0)
    FROM requests
    WHERE user_id=?
    """,(user_id,))
    expense = c.fetchone()[0]

    # Income (commission earned)
    c.execute("""
    SELECT IFNULL(SUM(commission),0)
    FROM requests
    WHERE accepted_by=?
    """,(user_id,))
    income = c.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        shop_name=session["shop_name"],
        mobile=session["user"],
        requests=requests,
        my_requests=my_requests,
        accepted_requests=accepted_requests,
        expense=expense,
        income=income
    )

# CREATE REQUEST
@app.route("/create_request", methods=["GET", "POST"])
def create_request():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        amount = int(request.form["amount"])
        commission = int(amount * 0.02)

        note = request.form.get("note","")

        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("""
        INSERT INTO requests (user_id,amount,commission,note,created_at)
        VALUES (?,?,?,?,?)
        """,(session["user_id"],amount,commission,note,created_at))

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("create_request.html")

# Request Details Route

@app.route("/request_details/<int:req_id>")
def request_details(req_id):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    SELECT r.id,u.shop_name,r.amount,r.commission,r.note,r.created_at
    FROM requests r
    JOIN users u ON r.user_id=u.id
    WHERE r.id=?
    """,(req_id,))

    request = c.fetchone()

    conn.close()

    return render_template("request_details.html",request=request)

@app.route("/accept/<int:req_id>")
def accept(req_id):
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("UPDATE requests SET status='Accepted', accepted_by=? WHERE id=?",
              (session["user_id"], req_id))
    conn.commit()
    conn.close()

    return redirect("/dashboard")
# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True) 