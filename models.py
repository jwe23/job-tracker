from datetime import datetime

class User:
    def __init__(self, id, username, email, password_hash, created_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at or datetime.now()

class Job:
    def __init__(self, id, user_id, company, position, date_applied, status, notes='', url='', created_at=None):
        self.id = id
        self.user_id = user_id
        self.company = company
        self.position = position
        self.date_applied = date_applied
        self.status = status
        self.notes = notes
        self.url = url
        self.created_at = created_at or datetime.now()
