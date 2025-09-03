# Create virtual env

python -m venv venv

# Activate venv

Go to cmd: venv\Scripts\activate.bat

# Set the env first & then run the server

uvicorn main:app --reload

# Install all requirements

pip install -r requirements.txt