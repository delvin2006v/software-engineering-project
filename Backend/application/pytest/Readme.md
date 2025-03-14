This folder contains automated tests for the backend APIs, written with **pytest**.

---

##  How to Run Tests

### Step 1: Install Dependencies

Install the required packages:
```bash
pip install pytest 
```
### Step 2: Start Your Backend Server

Ensure your Flask backend is running at `http://localhost:5000`.

### Step 3: Run the Tests

To run all tests, cd to /pytest and execute:
```bash
pytest -v
```

To run a specific test file, use:
```bash
pytest -v test_<filename>.py
```
