# job-tracker

Full-stack web application to track job applications with user authentication and status management.

## Features

- User authentication (signup/login with secure password hashing)
- Add job applications with company, position, date, and status
- View all applications in organized table
- Status tracking (Applied, Interview, Offer, Rejected)
- Color-coded status badges
- Delete applications
- Responsive design for mobile and desktop

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Authentication:** Werkzeug password hashing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jwe23/job-tracker.git
cd job-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open browser to `http://localhost:5000`

## Usage

1. Create an account on the signup page
2. Login with your credentials
3. Add job applications using the form
4. Track application status and view all applications in the dashboard
5. Delete applications as needed

## Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- created_at

### Jobs Table
- id (Primary Key)
- user_id (Foreign Key)
- company
- position
- date_applied
- status
- notes
- url
- created_at

## Security

- Passwords are hashed using Werkzeug's security utilities
- Session-based authentication
- SQL injection protection through parameterized queries

## Future Improvements

- Edit job applications
- Filter by status
- Search functionality
- Export to CSV
- Email notifications
- Application statistics dashboard

## License

MIT
