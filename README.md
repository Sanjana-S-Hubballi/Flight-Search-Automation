# Flight Search Automation with Data-Driven Testing

This project automates the flight search workflow on [Goibibo.com](https://www.goibibo.com) using Playwright, Python, and Pytest.
It fills search details, applies filters, extracts flight results, and saves them to CSV files.

# Project workflow
1. Loads test data.
2. Opens the Goibibo website.
3. Closes the login/signup popup.
4. Perform search steps: enter from/to, select dates, travellers, class.
5. Apply filters (like Non-Stop, Student Fare, Price Slider).
6. Extract the results and save them in a csv file.

![image (1)](https://github.com/user-attachments/assets/25d7a49e-13d9-4ada-b533-7b212497dd24)

# Setup Instructions

### Step 1: Clone this repository
git clone [https://github.com/yourusername/flight-search-automation.git](https://github.com/Sanjana-S-Hubballi/Flight-Search-Automation.git)
cd flight-search-automation

### Step 2: Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

### Step 3: Install dependencies
pip install -r requirements.txt

**Install playwright browser** : pip install playwright

### Step 4: Execute all tests
 pytest tests/test_flight_booking.py --html=results/ddt_report.html -v

### Step 5: Sample Input data
![image](https://github.com/user-attachments/assets/e791ecaa-85c9-439e-9b64-d01152b35675)


