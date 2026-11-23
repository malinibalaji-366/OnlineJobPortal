# Online Job Portal

A web-based job recruitment platform built using **Python, Django and MySQL**. The application connects job seekers with companies, allowing candidates to explore job opportunities and companies to publish and manage job postings.

🌐 **Live Demo:** https://onlinejobportal-production-3d5ee4ce.up.railway.app

## Features

### Candidate Module
- Candidate registration and login
- Candidate dashboard
- View and edit candidate profile
- Browse available job opportunities
- Apply for jobs
- Track job applications

### Company Module
- Company registration and login
- Company dashboard
- Post new job opportunities
- Manage job postings
- View candidate applications
- Update application status

### General Features
- Role-based access for candidates and companies
- Django authentication
- MySQL database integration
- Responsive web interface
- Production deployment using Railway

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| MySQL | Database |
| HTML5 | Page structure |
| CSS3 | Styling |
| JavaScript | Client-side functionality |
| Git & GitHub | Version control |
| Gunicorn | Production application server |
| WhiteNoise | Static file serving |
| Railway | Cloud deployment |

## Project Structure

```text
OnlineJobPortal/
│
├── accounts/
├── candidates/
├── companies/
├── jobs/
├── jobportal/
├── templates/
├── static/
├── media/
├── manage.py
├── requirements.txt
├── Procfile
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/malinibalaji-366/OnlineJobPortal.git
cd OnlineJobPortal
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=online_job_portal
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
```

**Note:** Never upload your `.env` file or secret credentials to GitHub.

### 5. Create the MySQL database

```sql
CREATE DATABASE online_job_portal;
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/

## Deployment

The application is deployed using Railway.

- Source code hosted on GitHub
- MySQL database hosted on Railway
- Gunicorn used as the application server
- WhiteNoise configured for static files
- Production environment variables configured securely

## Testing

The deployed application has been tested for:

- Candidate registration and login
- Company registration and login
- Dashboard access
- Job posting and browsing
- Job application workflow
- Application management

## Future Enhancements

- Advanced job search and filtering
- Email notifications
- Resume upload and management
- Improved candidate-company communication
- Enhanced analytics dashboard

## Author

**Malini Balaji**

GitHub: [malinibalaji-366](https://github.com/malinibalaji-366)

---

⭐ If you find this project interesting, feel free to explore the repository!
