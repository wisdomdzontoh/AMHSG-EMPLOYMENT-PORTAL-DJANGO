# *Health Workers Employment Portal*

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

The Health Workers Employment Portal is a web application designed to facilitate the employment process for health workers. This portal allows health facilities to post job listings and manage applicants, while job seekers can search and apply for jobs in the health sector. It provides an intuitive dashboard for both administrators and users to manage their respective tasks efficiently.

## Features

- **User Authentication**: Secure registration and login for both health workers and employers.
- **Job Listings**: Employers can post job listings, and health workers can search and apply for jobs.
- **Notifications**: Users receive notifications for job applications and other important updates.
- **Profile Management**: Health workers can create and manage their profiles, including uploading resumes.
- **Admin Dashboard**: An admin panel for managing users, job listings, and viewing statistics.

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Database**: SQLite (default) or PostgreSQL (recommended)
- **Deployment**: Gunicorn, Nginx, Docker (optional)
- **Version Control**: Git

## Setup and Installation

### Prerequisites

- Python 3.x
- Pipenv or virtualenv
- PostgreSQL (optional, but recommended)
- Git

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/health-workers-employment-portal.git
   cd health-workers-employment-portal
   ```

### Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

### Install the required packages:

pip install -r requirements.txt


**Set up the database:**

* Update the `DATABASES` setting in `settings.py` if using PostgreSQL.
* Run the migrations:
  <pre><div class="dark bg-gray-950 rounded-md border-[0.5px] border-token-border-medium"><div class="flex items-center relative text-token-text-secondary bg-token-main-surface-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span></div></div></pre>

`python manage.py migrate`

## Create a superuser to access the admin dashboard:

`python manage.py createsuperuser`

### Run the development server:

`python manage.py runserver`

2. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000/`.

## Usage

* **Admin:** Access the admin dashboard at `http://127.0.0.1:8000/admin/` to manage users, job listings, and notifications.
* **Health Workers:** Register, log in, search for job listings, and apply for jobs.
* **Employers:** Post job listings, manage applicants, and send notifications.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

* **Your Name** - wisdomdzontoh@gmail.com
* **Project Link** :[ https://github.com/wisdomdzontoh/AMHSG-EMPLOYMENT-PORTAL-DJANGO-.git]()
