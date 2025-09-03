# Project Detials:

    Project Name: Fastapi Boilerplate

    # Api url: http://localhost:8000/

    # Swagger api docs: http://localhost:8000/docs

        *** username and password is in .env

    # Developer dash app: 

        *** To create super admin, seed data when db is not initilized.

# Create virtual env

python -m venv venv

# Activate venv

Go to cmd: venv\Scripts\activate.bat # For current settings

# Install all requirements

pip install -r requirements.txt

# Set the env first & then run the server

uvicorn main:app --reload

# Migration steps from scratch

 1. alembic init alembic

 2. alembic revision --autogenerate -m "Initial migration"

 3. alembic upgrade head

 4. alembic stamp head # If migration file is manually deleted