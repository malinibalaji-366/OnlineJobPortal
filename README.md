# Online Job Portal

A web-based recruitment platform developed using Python, Django and MySQL. The application connects job seekers with companies through a centralized platform for job searching, recruitment and application management.

## Features

### Candidate
- Candidate registration and login
- Candidate profile creation and editing
- Browse available job listings
- Search and filter jobs
- View job details
- Apply for jobs
- Track application status
- Prevent duplicate applications

### Company
- Company registration and login
- Company profile management
- Post new job vacancies
- Edit and delete job postings
- Activate and deactivate job listings
- View candidate applications
- Update application status

### Admin
- Manage users and roles
- Manage candidate profiles
- Manage company profiles
- Manage jobs and applications through Django Admin

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| MySQL | Database |
| HTML5 | Page structure |
| CSS3 | Styling |
| Bootstrap 5 | Responsive UI |
| JavaScript | Frontend interactions |
| VS Code | Development environment |

## Project Modules

- `accounts` – User registration, login and role management
- `candidates` – Candidate profile management
- `companies` – Company profile management
- `jobs` – Job postings and applications

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd OnlineJobPortal
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure MySQL

Create a MySQL database and configure the database connection in Django's `settings.py`.

Do not upload your database password or secret credentials to GitHub.

### 6. Apply migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create an admin account

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open the application at:

`http://127.0.0.1:8000/`

Django Admin:

`http://127.0.0.1:8000/admin/`

## Project Structure

```text
OnlineJobPortal/
│
├── accounts/
├── candidates/
├── companies/
├── jobs/
├── templates/
├── static/
├── manage.py
├── requirements.txt
└── README.md
```

## Future Enhancements

- Resume upload functionality
- Email notifications
- Job recommendation system
- Interview scheduling
- Advanced analytics
- Online deployment

## Author

**Malini Balaji**

Personal Full Stack Web Development Project.

## License

This project is developed for learning and portfolio demonstration purposes.