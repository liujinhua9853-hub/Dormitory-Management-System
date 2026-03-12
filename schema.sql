DROP TABLE IF EXISTS checkouts;
DROP TABLE IF EXISTS checkins;
DROP TABLE IF EXISTS maintenance;
DROP TABLE IF EXISTS inspections;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS rooms;

CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT NOT NULL,
    department TEXT NOT NULL,
    position TEXT NOT NULL,
    phone TEXT,
    hire_date TEXT,
    emergency_contact TEXT,
    emergency_phone TEXT,
    is_resident INTEGER NOT NULL DEFAULT 0 CHECK (is_resident IN (0, 1))
);

CREATE TABLE rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building TEXT NOT NULL,
    floor TEXT NOT NULL,
    room_number TEXT NOT NULL,
    room_type TEXT NOT NULL,
    total_beds INTEGER NOT NULL CHECK (total_beds > 0),
    occupied_beds INTEGER NOT NULL DEFAULT 0 CHECK (occupied_beds >= 0),
    status TEXT NOT NULL CHECK (status IN ('可入住', '满员', '维修中', '停用')),
    notes TEXT,
    UNIQUE (building, room_number)
);

CREATE TABLE checkins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    bed_no TEXT NOT NULL,
    checkin_date TEXT NOT NULL,
    deposit REAL NOT NULL DEFAULT 0,
    key_issued INTEGER NOT NULL DEFAULT 0 CHECK (key_issued IN (0, 1)),
    notes TEXT,
    active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
    FOREIGN KEY (employee_id) REFERENCES employees (id),
    FOREIGN KEY (room_id) REFERENCES rooms (id)
);

CREATE TABLE checkouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    checkin_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    bed_no TEXT NOT NULL,
    checkout_date TEXT NOT NULL,
    room_checked INTEGER NOT NULL DEFAULT 0 CHECK (room_checked IN (0, 1)),
    damaged INTEGER NOT NULL DEFAULT 0 CHECK (damaged IN (0, 1)),
    deposit_returned INTEGER NOT NULL DEFAULT 0 CHECK (deposit_returned IN (0, 1)),
    notes TEXT,
    FOREIGN KEY (checkin_id) REFERENCES checkins (id),
    FOREIGN KEY (employee_id) REFERENCES employees (id),
    FOREIGN KEY (room_id) REFERENCES rooms (id)
);

CREATE TABLE maintenance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_date TEXT NOT NULL,
    building TEXT NOT NULL,
    room_number TEXT NOT NULL,
    content TEXT NOT NULL,
    reporter TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('待处理', '处理中', '已完成')),
    completed_date TEXT,
    notes TEXT
);

CREATE TABLE inspections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inspect_date TEXT NOT NULL,
    building TEXT NOT NULL,
    room_number TEXT NOT NULL,
    inspect_type TEXT NOT NULL CHECK (inspect_type IN ('卫生', '安全', '纪律')),
    inspect_result TEXT NOT NULL,
    issue_desc TEXT,
    handling_result TEXT,
    notes TEXT
);
