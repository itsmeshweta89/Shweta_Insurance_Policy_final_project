# This is a Insurance Policy Co-Pilot Assistant

This project has 2 major directtories -
1. app
2. frontend

app - It has all the backend python classes and functionality implementation
frontend - It has streamlit implementation

## Initialize Your Virtual Environment
```bash
# Create environment
python -m venv .venv

# Activate
source .venv/bin/activate
```

## Install Project Dependencies
```bash
pip install -r requirements.txt

## Running the Application Suite

### 1. Launch the FastAPI Backend Core
```bash
cd app
uvicorn main:app 
```

### 2. Launch the Interactive Dashboard Portal
```bash
streamlit run frontend/streamlit.py

## Run the Tests & Generate Test Report
```bash
python app/tests/test_tools.py 
```

