from __future__ import annotations

import sqlite3
from contextlib import closing
from datetime import date, datetime
from pathlib import Path

from flask import Flask, g, redirect, render_template, request, url_for, flash, make_response, session
from flask import Flask, g, redirect, render_template, request, url_for, flash, session

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "dormitory.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "dormitory-dev-key"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"


def ensure_users_table():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            display_name TEXT NOT NULL
        )
        """
    )
    admin = db.execute("SELECT id FROM users WHERE username='admin'").fetchone()
    if not admin:
        db.execute("INSERT INTO users (username, password, display_name) VALUES (?, ?, ?)", ("admin", "admin123", "系统管理员"))
    db.commit()


@app.before_request
def require_login():
    allow_endpoints = {"login", "static"}
    if request.endpoint in allow_endpoints or request.endpoint is None:
        return
    if not session.get("user_id"):
        return redirect(url_for("login"))
    ensure_base_tables()
    ensure_checkout_settlement_columns()
    ensure_users_table()


@app.context_processor
def inject_current_user():
    return {"current_user_name": session.get("display_name")}


def ensure_users_table():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            display_name TEXT NOT NULL
        )
        """
    )
    admin = db.execute("SELECT id FROM users WHERE username='admin'").fetchone()
    if not admin:
        db.execute("INSERT INTO users (username, password, display_name) VALUES (?, ?, ?)", ("admin", "admin123", "系统管理员"))
    db.commit()


@app.before_request
def require_login():
    allow_endpoints = {"login", "static"}
    if request.endpoint in allow_endpoints or request.endpoint is None:
        return
    if not session.get("user_id"):
        return redirect(url_for("login"))
    ensure_base_tables()
    ensure_checkout_settlement_columns()
    ensure_users_table()


@app.context_processor
def inject_current_user():
    return {"current_user_name": session.get("display_name")}


def ensure_users_table():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            display_name TEXT NOT NULL
        )
        """
    )
    admin = db.execute("SELECT id FROM users WHERE username='admin'").fetchone()
    if not admin:
        db.execute("INSERT INTO users (username, password, display_name) VALUES (?, ?, ?)", ("admin", "admin123", "系统管理员"))
    db.commit()


@app.before_request
def require_login():
    allow_endpoints = {"login", "static"}
    if request.endpoint in allow_endpoints or request.endpoint is None:
        return
    if not session.get("user_id"):
        return redirect(url_for("login"))
    ensure_base_tables()
    ensure_checkout_settlement_columns()
    ensure_users_table()


@app.context_processor
def inject_current_user():
    return {"current_user_name": session.get("display_name")}


def ensure_users_table():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            display_name TEXT NOT NULL
        )
        """
    )
    admin = db.execute("SELECT id FROM users WHERE username='admin'").fetchone()
    if not admin:
        db.execute("INSERT INTO users (username, password, display_name) VALUES (?, ?, ?)", ("admin", "admin123", "系统管理员"))
    db.commit()


@app.before_request
def require_login():
    allow_endpoints = {"login", "static"}
    if request.endpoint in allow_endpoints or request.endpoint is None:
        return
    if not session.get("user_id"):
        return redirect(url_for("login"))
    ensure_base_tables()
    ensure_checkout_settlement_columns()
    ensure_users_table()


@app.context_processor
def inject_current_user():
    return {"current_user_name": session.get("display_name")}


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        g.db = conn
    return g.db


def is_logged_in() -> bool:
    return session.get("logged_in", False)


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def execute(query: str, params: tuple = ()):
    db = get_db()
    cur = db.execute(query, params)
    db.commit()
    return cur


def query_all(query: str, params: tuple = ()):
    cur = get_db().execute(query, params)
    return cur.fetchall()


def query_one(query: str, params: tuple = ()):
    cur = get_db().execute(query, params)
    return cur.fetchone()


def init_db(with_demo: bool = True):
    schema_path = BASE_DIR / "schema.sql"
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with schema_path.open("r", encoding="utf-8") as f:
            conn.executescript(f.read())

        if with_demo:
            conn.executescript(
                """
                INSERT OR IGNORE INTO employees (id, name, gender, department, position, phone, hire_date, emergency_contact, emergency_phone, is_resident)
                VALUES
                (1, '张三', '男', '生产部', '技术员', '13800000001', '2024-01-10', '张父', '13800001001', 1),
                (2, '李四', '女', '行政部', '文员', '13800000002', '2024-03-15', '李母', '13800001002', 0),
                (3, '王五', '男', '仓储部', '仓管员', '13800000003', '2023-11-01', '王姐', '13800001003', 1);

                INSERT OR IGNORE INTO rooms (id, building, floor, room_number, room_type, total_beds, occupied_beds, status, notes)
                VALUES
                (1, 'A栋', '1', '101', '四人间', 4, 2, '可入住', '靠近电梯'),
                (2, 'A栋', '1', '102', '双人间', 2, 0, '可入住', ''),
                (3, 'B栋', '2', '201', '四人间', 4, 0, '维修中', '空调维修');

                INSERT OR IGNORE INTO checkins (id, employee_id, room_id, bed_no, checkin_date, deposit, key_issued, notes, active)
                VALUES
                (1, 1, 1, '1', '2024-05-01', 500, 1, '已登记', 1),
                (2, 3, 1, '2', '2024-05-12', 500, 1, '已登记', 1);

                INSERT OR IGNORE INTO maintenance (id, report_date, building, room_number, content, reporter, status, completed_date, notes)
                VALUES
                (1, date('now','-5 day'), 'A栋', '101', '卫生间漏水', '张三', '处理中', NULL, ''),
                (2, date('now','-2 day'), 'B栋', '201', '空调不制冷', '宿管员', '待处理', NULL, '等待配件');

                INSERT OR IGNORE INTO inspections (id, inspect_date, building, room_number, inspect_type, inspect_result, issue_desc, handling_result, notes)
                VALUES
                (1, date('now','-3 day'), 'A栋', '101', '卫生', '不合格', '垃圾未及时清理', '限期整改', ''),
                (2, date('now','-1 day'), 'A栋', '102', '安全', '合格', '', '无', '');
                """
            )
            conn.commit()




def ensure_base_tables():
    db = get_db()
    has_employees = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employees'").fetchone()
    if not has_employees:
        init_db(with_demo=True)

def ensure_checkout_settlement_columns():
    db = get_db()
    checkout_exists = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='checkouts'").fetchone()
    if not checkout_exists:
        return
def ensure_checkout_settlement_columns():
    db = get_db()
    existing_columns = {row["name"] for row in db.execute("PRAGMA table_info(checkouts)").fetchall()}
    required_columns = {
        "water_start": "REAL NOT NULL DEFAULT 0",
        "water_end": "REAL NOT NULL DEFAULT 0",
        "water_price": "REAL NOT NULL DEFAULT 0",
        "water_fee": "REAL NOT NULL DEFAULT 0",
        "electricity_start": "REAL NOT NULL DEFAULT 0",
        "electricity_end": "REAL NOT NULL DEFAULT 0",
        "electricity_price": "REAL NOT NULL DEFAULT 0",
        "electricity_fee": "REAL NOT NULL DEFAULT 0",
        "total_amount": "REAL NOT NULL DEFAULT 0",
        "settlement_note": "TEXT",
        "settlement_status": "TEXT NOT NULL DEFAULT '未结清'",
    }
    for col_name, col_type in required_columns.items():
        if col_name not in existing_columns:
            db.execute(f"ALTER TABLE checkouts ADD COLUMN {col_name} {col_type}")
    db.commit()


def validate_phone(phone: str) -> bool:
    return phone.isdigit() and 7 <= len(phone) <= 15


def parse_non_negative_float(value: str, field_name: str) -> float:
    if value is None or str(value).strip() == "":
        raise ValueError(f"{field_name}不能为空")
    try:
        number = float(value)
    except ValueError as exc:
        raise ValueError(f"{field_name}必须为数字") from exc
    if number < 0:
        raise ValueError(f"{field_name}不能为负数")
    return number


def refresh_room_status(room_id: int):
    room = query_one("SELECT total_beds, occupied_beds, status FROM rooms WHERE id=?", (room_id,))
    if not room:
        return
    if room["status"] in ("维修中", "停用"):
        return
    status = "满员" if room["occupied_beds"] >= room["total_beds"] else "可入住"
    execute("UPDATE rooms SET status=? WHERE id=?", (status, room_id))

@app.before_request
def require_login():
    allowed_routes = {"login", "static"}

    if request.endpoint in allowed_routes:
        return

    if not is_logged_in():
        return redirect(url_for("login"))




@app.route("/login", methods=["GET", "POST"])
def login():
    ensure_users_table()
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = query_one("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if not user:
            flash("用户名或密码错误", "error")
            return render_template("login.html")
        session["user_id"] = user["id"]
        session["display_name"] = user["display_name"]
        flash("登录成功", "success")
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("已退出登录", "success")
    return redirect(url_for("login"))




# 认证路由：仅保留一组 login/logout 处理器，避免重复注册端点
@app.route("/login", methods=["GET", "POST"])
def login():
    ensure_users_table()
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = query_one("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if not user:
            flash("用户名或密码错误", "error")
            return render_template("login.html")
        session["user_id"] = user["id"]
        session["display_name"] = user["display_name"]
        flash("登录成功", "success")
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("已退出登录", "success")
    return redirect(url_for("login"))




# 认证路由：仅保留一组 login/logout 处理器，避免重复注册端点
# 如发生合并冲突，禁止再新增同名 login/logout 视图函数。
@app.route("/login", methods=["GET", "POST"])
def login():
    ensure_users_table()
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = query_one("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if not user:
            flash("用户名或密码错误", "error")
            return render_template("login.html")
        session["user_id"] = user["id"]
        session["display_name"] = user["display_name"]
        flash("登录成功", "success")
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("已退出登录", "success")
    return redirect(url_for("login"))




# 认证路由（集中注册，避免端点重复覆盖）
def login_view():
    ensure_users_table()
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = query_one("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if not user:
            flash("用户名或密码错误", "error")
            return render_template("login.html")
        session["user_id"] = user["id"]
        session["display_name"] = user["display_name"]
        flash("登录成功", "success")
        return redirect(url_for("dashboard"))
    return render_template("login.html")


def logout_view():
    session.clear()
    flash("已退出登录", "success")
    return redirect(url_for("login"))


def register_auth_routes():
    if "login" not in app.view_functions:
        app.add_url_rule("/login", endpoint="login", view_func=login_view, methods=["GET", "POST"])
    if "logout" not in app.view_functions:
        app.add_url_rule("/logout", endpoint="logout", view_func=logout_view, methods=["POST"])


register_auth_routes()


@app.route("/")
def dashboard():
    stats = {
        "employee_total": query_one("SELECT COUNT(*) c FROM employees")["c"],
        "resident_total": query_one("SELECT COUNT(*) c FROM employees WHERE is_resident=1")["c"],
        "room_total": query_one("SELECT COUNT(*) c FROM rooms")["c"],
        "beds_total": query_one("SELECT COALESCE(SUM(total_beds),0) c FROM rooms")["c"],
        "beds_used": query_one("SELECT COALESCE(SUM(occupied_beds),0) c FROM rooms")["c"],
        "repair_open": query_one("SELECT COUNT(*) c FROM maintenance WHERE status!='已完成'")["c"],
        "month_checkins": query_one(
            "SELECT COUNT(*) c FROM checkins WHERE strftime('%Y-%m', checkin_date)=strftime('%Y-%m','now')"
        )["c"],
        "month_checkouts": query_one(
            "SELECT COUNT(*) c FROM checkouts WHERE strftime('%Y-%m', checkout_date)=strftime('%Y-%m','now')"
        )["c"],
    }
    stats["beds_free"] = max(stats["beds_total"] - stats["beds_used"], 0)
    return render_template("dashboard.html", stats=stats)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            flash("登录成功", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("用户名或密码错误", "error")

    return render_template("login.html")

@app.route("/employees")
def employees():
    q = request.args.get("q", "").strip()
    if q:
        rows = query_all(
            """
            SELECT * FROM employees
            WHERE name LIKE ? OR department LIKE ? OR position LIKE ? OR phone LIKE ?
            ORDER BY id DESC
            """,
            tuple(f"%{q}%" for _ in range(4)),
        )
    else:
        rows = query_all("SELECT * FROM employees ORDER BY id DESC")
    return render_template("employees.html", employees=rows, q=q)


@app.route("/employees/add", methods=["GET", "POST"])
def employee_add():
    if request.method == "POST":
        form = request.form
        if form["phone"] and not validate_phone(form["phone"]):
            flash("联系电话格式不正确", "error")
            return render_template("employee_form.html", employee=form, mode="add")
        if form["emergency_phone"] and not validate_phone(form["emergency_phone"]):
            flash("紧急联系电话格式不正确", "error")
            return render_template("employee_form.html", employee=form, mode="add")
        execute(
            """
            INSERT INTO employees (name, gender, department, position, phone, hire_date, emergency_contact, emergency_phone, is_resident)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                form["name"],
                form["gender"],
                form["department"],
                form["position"],
                form["phone"],
                form["hire_date"],
                form["emergency_contact"],
                form["emergency_phone"],
                1 if form.get("is_resident") == "1" else 0,
            ),
        )
        flash("员工新增成功", "success")
        return redirect(url_for("employees"))
    return render_template("employee_form.html", employee=None, mode="add")


@app.route("/employees/<int:employee_id>/edit", methods=["GET", "POST"])
def employee_edit(employee_id: int):
    employee = query_one("SELECT * FROM employees WHERE id=?", (employee_id,))
    if not employee:
        flash("员工不存在", "error")
        return redirect(url_for("employees"))
    if request.method == "POST":
        form = request.form
        if form["phone"] and not validate_phone(form["phone"]):
            flash("联系电话格式不正确", "error")
            return render_template("employee_form.html", employee=form, mode="edit")
        execute(
            """
            UPDATE employees SET name=?, gender=?, department=?, position=?, phone=?, hire_date=?, emergency_contact=?, emergency_phone=?, is_resident=?
            WHERE id=?
            """,
            (
                form["name"],
                form["gender"],
                form["department"],
                form["position"],
                form["phone"],
                form["hire_date"],
                form["emergency_contact"],
                form["emergency_phone"],
                1 if form.get("is_resident") == "1" else 0,
                employee_id,
            ),
        )
        flash("员工信息已更新", "success")
        return redirect(url_for("employees"))
    return render_template("employee_form.html", employee=employee, mode="edit")


@app.route("/employees/<int:employee_id>/delete", methods=["POST"])
def employee_delete(employee_id: int):
    active = query_one("SELECT id FROM checkins WHERE employee_id=? AND active=1", (employee_id,))
    if active:
        flash("该员工存在在住记录，不能删除", "error")
    else:
        execute("DELETE FROM employees WHERE id=?", (employee_id,))
        flash("员工已删除", "success")
    return redirect(url_for("employees"))


@app.route("/rooms")
def rooms():
    q = request.args.get("q", "").strip()
    if q:
        rows = query_all(
            """
            SELECT * FROM rooms
            WHERE building LIKE ? OR room_number LIKE ? OR status LIKE ?
            ORDER BY id DESC
            """,
            (f"%{q}%", f"%{q}%", f"%{q}%"),
        )
    else:
        rows = query_all("SELECT * FROM rooms ORDER BY id DESC")
    return render_template("rooms.html", rooms=rows, q=q)


@app.route("/rooms/add", methods=["GET", "POST"])
def room_add():
    if request.method == "POST":
        form = request.form
        total_beds = int(form["total_beds"])
        execute(
            """
            INSERT INTO rooms (building, floor, room_number, room_type, total_beds, occupied_beds, status, notes)
            VALUES (?, ?, ?, ?, ?, 0, ?, ?)
            """,
            (
                form["building"],
                form["floor"],
                form["room_number"],
                form["room_type"],
                total_beds,
                form["status"],
                form["notes"],
            ),
        )
        flash("房间新增成功", "success")
        return redirect(url_for("rooms"))
    return render_template("room_form.html", room=None, mode="add")


@app.route("/rooms/<int:room_id>/edit", methods=["GET", "POST"])
def room_edit(room_id: int):
    room = query_one("SELECT * FROM rooms WHERE id=?", (room_id,))
    if not room:
        flash("房间不存在", "error")
        return redirect(url_for("rooms"))
    if request.method == "POST":
        form = request.form
        total_beds = int(form["total_beds"])
        if room["occupied_beds"] > total_beds:
            flash("床位总数不能小于当前入住人数", "error")
            return render_template("room_form.html", room=room, mode="edit")
        execute(
            """
            UPDATE rooms SET building=?, floor=?, room_number=?, room_type=?, total_beds=?, status=?, notes=?
            WHERE id=?
            """,
            (
                form["building"],
                form["floor"],
                form["room_number"],
                form["room_type"],
                total_beds,
                form["status"],
                form["notes"],
                room_id,
            ),
        )
        refresh_room_status(room_id)
        flash("房间信息已更新", "success")
        return redirect(url_for("rooms"))
    return render_template("room_form.html", room=room, mode="edit")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("已退出登录", "success")
    return redirect(url_for("login"))

@app.route("/rooms/<int:room_id>/delete", methods=["POST"])
def room_delete(room_id: int):
    active = query_one("SELECT id FROM checkins WHERE room_id=? AND active=1", (room_id,))
    if active:
        flash("该房间仍有在住人员，不能删除", "error")
    else:
        execute("DELETE FROM rooms WHERE id=?", (room_id,))
        flash("房间已删除", "success")
    return redirect(url_for("rooms"))


@app.route("/checkins", methods=["GET", "POST"])
def checkins():
    if request.method == "POST":
        form = request.form
        employee_id = int(form["employee_id"])
        room_id = int(form["room_id"])
        bed_no = form["bed_no"].strip()

        employee = query_one("SELECT * FROM employees WHERE id=?", (employee_id,))
        room = query_one("SELECT * FROM rooms WHERE id=?", (room_id,))

        if not employee or not room:
            flash("员工或房间不存在", "error")
            return redirect(url_for("checkins"))
        if room["status"] in ("维修中", "停用"):
            flash("该房间状态不允许入住", "error")
            return redirect(url_for("checkins"))
        if employee["is_resident"] == 1:
            flash("该员工已在住宿舍", "error")
            return redirect(url_for("checkins"))
        if room["occupied_beds"] >= room["total_beds"]:
            flash("该房间已满员", "error")
            return redirect(url_for("checkins"))
        bed_in_use = query_one(
            "SELECT id FROM checkins WHERE room_id=? AND bed_no=? AND active=1",
            (room_id, bed_no),
        )
        if bed_in_use:
            flash("该床位已有人入住", "error")
            return redirect(url_for("checkins"))

        execute(
            """
            INSERT INTO checkins (employee_id, room_id, bed_no, checkin_date, deposit, key_issued, notes, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            """,
            (
                employee_id,
                room_id,
                bed_no,
                form["checkin_date"],
                float(form["deposit"] or 0),
                1 if form.get("key_issued") == "1" else 0,
                form["notes"],
            ),
        )
        execute("UPDATE rooms SET occupied_beds=occupied_beds+1 WHERE id=?", (room_id,))
        refresh_room_status(room_id)
        execute("UPDATE employees SET is_resident=1 WHERE id=?", (employee_id,))
        flash("办理入住成功", "success")
        return redirect(url_for("checkins"))

    records = query_all(
        """
        SELECT c.*, e.name employee_name, r.building, r.room_number
        FROM checkins c
        JOIN employees e ON c.employee_id=e.id
        JOIN rooms r ON c.room_id=r.id
        ORDER BY c.id DESC
        """
    )
    employees_not_resident = query_all("SELECT id, name FROM employees WHERE is_resident=0 ORDER BY name")
    available_rooms = query_all("SELECT id, building, room_number FROM rooms WHERE status='可入住' OR status='满员' ORDER BY building, room_number")
    return render_template(
        "checkins.html",
        records=records,
        employees=employees_not_resident,
        rooms=available_rooms,
        today=date.today().isoformat(),
    )


@app.route("/checkouts", methods=["GET", "POST"])
def checkouts():
    ensure_checkout_settlement_columns()
    if request.method == "POST":
        form = request.form
        checkin_id = int(form["checkin_id"])
        checkin = query_one("SELECT * FROM checkins WHERE id=? AND active=1", (checkin_id,))
        if not checkin:
            flash("入住记录不存在或已退宿", "error")
            return redirect(url_for("checkouts"))

        try:
            water_start = parse_non_negative_float(form.get("water_start"), "水表起始读数")
            water_end = parse_non_negative_float(form.get("water_end"), "水表结束读数")
            water_price = parse_non_negative_float(form.get("water_price"), "水费单价")
            electricity_start = parse_non_negative_float(form.get("electricity_start"), "电表起始读数")
            electricity_end = parse_non_negative_float(form.get("electricity_end"), "电表结束读数")
            electricity_price = parse_non_negative_float(form.get("electricity_price"), "电费单价")
        except ValueError as e:
            flash(str(e), "error")
            return redirect(url_for("checkouts"))

        if water_end < water_start:
            flash("水表结束读数不能小于起始读数", "error")
            return redirect(url_for("checkouts"))
        if electricity_end < electricity_start:
            flash("电表结束读数不能小于起始读数", "error")
            return redirect(url_for("checkouts"))

        settlement_status = form.get("settlement_status", "").strip()
        if settlement_status not in ("未结清", "已结清"):
            flash("结算状态不合法", "error")
            return redirect(url_for("checkouts"))

        water_fee = (water_end - water_start) * water_price
        electricity_fee = (electricity_end - electricity_start) * electricity_price
        total_amount = water_fee + electricity_fee

        execute(
            """
            INSERT INTO checkouts (
                checkin_id, employee_id, room_id, bed_no, checkout_date, room_checked, damaged, deposit_returned, notes,
                water_start, water_end, water_price, water_fee,
                electricity_start, electricity_end, electricity_price, electricity_fee,
                total_amount, settlement_note, settlement_status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                checkin_id,
                checkin["employee_id"],
                checkin["room_id"],
                checkin["bed_no"],
                form["checkout_date"],
                1 if form.get("room_checked") == "1" else 0,
                1 if form.get("damaged") == "1" else 0,
                1 if form.get("deposit_returned") == "1" else 0,
                form["notes"],
                water_start,
                water_end,
                water_price,
                water_fee,
                electricity_start,
                electricity_end,
                electricity_price,
                electricity_fee,
                total_amount,
                form.get("settlement_note", "").strip(),
                settlement_status,
            ),
        )
        execute("UPDATE checkins SET active=0 WHERE id=?", (checkin_id,))
        execute("UPDATE rooms SET occupied_beds=MAX(occupied_beds-1,0) WHERE id=?", (checkin["room_id"],))
        refresh_room_status(checkin["room_id"])
        execute("UPDATE employees SET is_resident=0 WHERE id=?", (checkin["employee_id"],))
        flash("退宿办理成功", "success")
        return redirect(url_for("checkouts"))

    active_checkins = query_all(
        """
        SELECT c.id, e.name employee_name, r.building, r.room_number, c.bed_no, c.checkin_date
        FROM checkins c
        JOIN employees e ON c.employee_id=e.id
        JOIN rooms r ON c.room_id=r.id
        WHERE c.active=1
        ORDER BY c.id DESC
        """
    )
    records = query_all(
        """
        SELECT o.*, e.name employee_name, r.building, r.room_number
        FROM checkouts o
        JOIN employees e ON o.employee_id=e.id
        JOIN rooms r ON o.room_id=r.id
        ORDER BY o.id DESC
        """
    )
    return render_template("checkouts.html", active_checkins=active_checkins, records=records, today=date.today().isoformat())


@app.route("/resident")
def resident_query():
    keyword = request.args.get("name", "").strip()
    row = None
    if keyword:
        row = query_one(
            """
            SELECT e.name employee_name, r.building, r.room_number, c.bed_no, c.checkin_date
            FROM checkins c
            JOIN employees e ON c.employee_id=e.id
            JOIN rooms r ON c.room_id=r.id
            WHERE c.active=1 AND e.name LIKE ?
            ORDER BY c.id DESC
            LIMIT 1
            """,
            (f"%{keyword}%",),
        )
    return render_template("resident_query.html", row=row, keyword=keyword)


@app.route("/maintenance", methods=["GET", "POST"])
def maintenance():
    if request.method == "POST":
        form = request.form
        if form.get("id"):
            done_date = form["completed_date"] if form["status"] == "已完成" else None
            execute(
                """
                UPDATE maintenance
                SET report_date=?, building=?, room_number=?, content=?, reporter=?, status=?, completed_date=?, notes=?
                WHERE id=?
                """,
                (
                    form["report_date"],
                    form["building"],
                    form["room_number"],
                    form["content"],
                    form["reporter"],
                    form["status"],
                    done_date,
                    form["notes"],
                    int(form["id"]),
                ),
            )
            flash("报修记录已更新", "success")
        else:
            done_date = form["completed_date"] if form["status"] == "已完成" else None
            execute(
                """
                INSERT INTO maintenance (report_date, building, room_number, content, reporter, status, completed_date, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    form["report_date"],
                    form["building"],
                    form["room_number"],
                    form["content"],
                    form["reporter"],
                    form["status"],
                    done_date,
                    form["notes"],
                ),
            )
            flash("报修记录已新增", "success")
        return redirect(url_for("maintenance"))

    edit_id = request.args.get("edit_id", type=int)
    edit_item = query_one("SELECT * FROM maintenance WHERE id=?", (edit_id,)) if edit_id else None
    q = request.args.get("q", "").strip()
    if q:
        records = query_all(
            "SELECT * FROM maintenance WHERE building LIKE ? OR room_number LIKE ? OR status LIKE ? ORDER BY id DESC",
            (f"%{q}%", f"%{q}%", f"%{q}%"),
        )
    else:
        records = query_all("SELECT * FROM maintenance ORDER BY id DESC")
    return render_template("maintenance.html", records=records, edit_item=edit_item, today=date.today().isoformat(), q=q)


@app.route("/inspections", methods=["GET", "POST"])
def inspections():
    if request.method == "POST":
        form = request.form
        execute(
            """
            INSERT INTO inspections (inspect_date, building, room_number, inspect_type, inspect_result, issue_desc, handling_result, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                form["inspect_date"],
                form["building"],
                form["room_number"],
                form["inspect_type"],
                form["inspect_result"],
                form["issue_desc"],
                form["handling_result"],
                form["notes"],
            ),
        )
        flash("检查记录已新增", "success")
        return redirect(url_for("inspections"))

    q = request.args.get("q", "").strip()
    if q:
        records = query_all(
            "SELECT * FROM inspections WHERE building LIKE ? OR room_number LIKE ? OR inspect_type LIKE ? ORDER BY id DESC",
            (f"%{q}%", f"%{q}%", f"%{q}%"),
        )
    else:
        records = query_all("SELECT * FROM inspections ORDER BY id DESC")
    return render_template("inspections.html", records=records, today=date.today().isoformat(), q=q)


@app.route("/export/excel")
def export_excel():
    ensure_checkout_settlement_columns()
    datasets = [
        ("员工信息", "SELECT * FROM employees ORDER BY id DESC"),
        ("房间信息", "SELECT * FROM rooms ORDER BY id DESC"),
        ("入住记录", "SELECT * FROM checkins ORDER BY id DESC"),
        ("退宿结算", "SELECT * FROM checkouts ORDER BY id DESC"),
        ("报修记录", "SELECT * FROM maintenance ORDER BY id DESC"),
        ("违规检查", "SELECT * FROM inspections ORDER BY id DESC"),
    ]

    html_parts = [
        "<html><head><meta charset='utf-8'></head><body>",
        f"<h2>宿舍管理数据导出（{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}）</h2>",
    ]

    for title, sql in datasets:
        rows = query_all(sql)
        html_parts.append(f"<h3>{title}</h3>")
        if not rows:
            html_parts.append("<p>暂无数据</p>")
            continue

        headers = list(rows[0].keys())
        html_parts.append("<table border='1' cellspacing='0' cellpadding='4'>")
        html_parts.append("<tr>" + "".join(f"<th>{h}</th>" for h in headers) + "</tr>")
        for row in rows:
            html_parts.append("<tr>" + "".join(f"<td>{'' if row[h] is None else row[h]}</td>" for h in headers) + "</tr>")
        html_parts.append("</table><br>")

    html_parts.append("</body></html>")
    content = "".join(html_parts)

    filename = f"宿舍管理数据导出_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xls"
    response = make_response(content)
    response.headers["Content-Type"] = "application/vnd.ms-excel; charset=utf-8"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


@app.route("/init-db")
def init_db_route():
    init_db(with_demo=True)
    ensure_users_table()
    ensure_checkout_settlement_columns()
    flash("数据库已初始化（包含演示数据）", "success")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    if not DB_PATH.exists():
        init_db(with_demo=True)
    with app.app_context():
        ensure_users_table()
    init_db(with_demo=True)
    with app.app_context():
        ensure_checkout_settlement_columns()
    app.run(debug=True)
