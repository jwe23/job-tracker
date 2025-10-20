import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Job
from datetime import datetime

DATABASE = 'jobs.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            date_applied TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT,
            url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(username, email, password):
    """Create a new user"""
    conn = get_db()
    cursor = conn.cursor()
    
    password_hash = generate_password_hash(password)
    
    try:
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_user_by_username(username):
    """Get user by username"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return User(row['id'], row['username'], row['email'], row['password_hash'], row['created_at'])
    return None

def verify_password(user, password):
    """Verify user password"""
    return check_password_hash(user.password_hash, password)

def create_job(user_id, company, position, date_applied, status, notes='', url=''):
    """Create a new job entry"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO jobs (user_id, company, position, date_applied, status, notes, url) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (user_id, company, position, date_applied, status, notes, url)
    )
    conn.commit()
    job_id = cursor.lastrowid
    conn.close()
    return job_id

def get_jobs_by_user(user_id):
    """Get all jobs for a user"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM jobs WHERE user_id = ? ORDER BY date_applied DESC', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    jobs = []
    for row in rows:
        job = Job(row['id'], row['user_id'], row['company'], row['position'], 
                  row['date_applied'], row['status'], row['notes'], row['url'], row['created_at'])
        jobs.append(row)
    
    return rows

def update_job(job_id, company, position, date_applied, status, notes, url):
    """Update a job entry"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        'UPDATE jobs SET company = ?, position = ?, date_applied = ?, status = ?, notes = ?, url = ? WHERE id = ?',
        (company, position, date_applied, status, notes, url, job_id)
    )
    conn.commit()
    conn.close()

def delete_job(job_id):
    """Delete a job entry"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM jobs WHERE id = ?', (job_id,))
    conn.commit()
    conn.close()
