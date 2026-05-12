-- =========================
-- USERS TABLE (BASE CLASS)
-- =========================
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL, -- household / staff / admin
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- HOUSEHOLD TABLE (UPDATED)
-- =========================
CREATE TABLE household (
    user_id INTEGER PRIMARY KEY,
    address TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =========================
-- PICKUP STAFF TABLE
-- =========================
CREATE TABLE pickup_staff (
    user_id INTEGER PRIMARY KEY,
    staff_id TEXT UNIQUE,
    assigned_area_id INTEGER,
    is_approved INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =========================
-- ADMIN TABLE
-- =========================
CREATE TABLE admin (
    user_id INTEGER PRIMARY KEY,
    admin_code TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- =========================
-- SERVICE AREA
-- =========================
CREATE TABLE service_area (
    area_id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_name TEXT UNIQUE NOT NULL
);

-- =========================
-- TEXTILE CATEGORY
-- =========================
CREATE TABLE textile_category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT UNIQUE NOT NULL
);

-- =========================
-- REQUEST TABLE
-- =========================
CREATE TABLE request (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    request_type TEXT NOT NULL, -- pickup / dropoff
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    scheduled_time TEXT,
    assigned_staff_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (assigned_staff_id) REFERENCES pickup_staff(user_id)
);

-- =========================
-- ITEM TABLE
-- =========================
CREATE TABLE item (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    item_type TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    condition_note TEXT,
    photo_path TEXT,
    confirmed_path TEXT,
    overridden_flag INTEGER DEFAULT 0,
    FOREIGN KEY (request_id) REFERENCES request(request_id)
);

-- =========================
-- CONDITION RESULT (ML OUTPUT)
-- =========================
CREATE TABLE condition_result (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    condition_label TEXT, -- good / worn / damaged
    confidence_score REAL,
    model_version TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES item(item_id)
);

-- =========================
-- HANDLING PATH
-- =========================
CREATE TABLE handling_path (
    path_id INTEGER PRIMARY KEY AUTOINCREMENT,
    result_id INTEGER NOT NULL,
    path_type TEXT, -- reuse / repair / recycle
    is_confirmed INTEGER DEFAULT 0,
    override_reason TEXT,
    FOREIGN KEY (result_id) REFERENCES condition_result(result_id)
);

-- =========================
-- INDEXES (PERFORMANCE)
-- =========================
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_request_user ON request(user_id);
CREATE INDEX idx_item_request ON item(request_id);