# HomeCare Backend

This is the backend service for the HomeCare application, designed to manage user authentication, email verification, and other essential functionalities for at-home care planning.

## Requirements

- Python 3.9+
- PostgreSQL 16.3
- Virtual Environment (recommended)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/homecare-backend.git
cd homecare-backend
```

### 2. Create a Virtual Environment

python -m venv .venv
source .venv/bin/activate # For Linux/MacOS
.venv\Scripts\activate # For Windows

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Configure Environment Variables

Contact for them!

### 5. Run Database Migrations

```bash
alembic upgrade head
```

### 6. Start the Server

```bash
uvicorn app.main:app --reload
```
