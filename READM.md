This is a simple web application that allows users to fetch Delhi High Court case details by entering:

Case Type
Case Number
Filing Year
The app uses Playwright (headless browser automation) and BeautifulSoup (for HTML parsing) to scrape public data from the official Delhi High Court portal.

🌐 Live Stack Used
Backend: Python, Flask
Frontend: HTML, CSS
Scraping: Playwright + BeautifulSoup
Database: SQLit3
Templating: Jinja2

✅ Features
Simple UI for case lookup
Form Fields: Case Type (dropdown), Case Number, Filing Year
Scrapes:
Parties’ names
Filing Date
Next Hearing Date
Latest Order/Judgment PDF link
Stores all queries and raw responses in SQLite
Mock Data supported for testing
User-friendly error messages
Downloadable PDFs

⚙️ How to Run
Clone this repository

Install required dependencies:

bash
Copy
Edit
pip install -r requirements.txt
playwright install
Run the app:

bash
Copy
Edit
python app.py
Visit http://localhost:5000 in your browser

🔐 CAPTCHA Handling
The Delhi High Court portal doesn't have a CAPTCHA on the case status page we target. If CAPTCHA or view-state token appeared:
We would document usage of manual tokens or third-party solving services (e.g., 2Captcha), or fallback to mock data.

🧪 Testing
You can test the application using mock data:

Example:
Case Type: MOCK
Case Number: 0001
Filing Year: 2025
This triggers mock data instead of scraping.

📁 Project Structure
csharp
Copy
Edit
├── app.py                # Main Flask application
├── scraper/
│   └── court_scraper.py  # Web scraping logic
├── templates/
│   ├── index.html        # Input form
│   └── result.html       # Display result
├── static/
│   └── style.css         # CSS styles
├── queries.db            # SQLite database
├── README.md             # Project README


✍️ Author
Sanskar Pandey
Email: sanskarpandey@gmail.com