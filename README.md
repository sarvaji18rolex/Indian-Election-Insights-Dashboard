# India Election Dashboard 🇮🇳

An interactive data-driven election analytics dashboard for visualizing Indian election trends, party performance, constituency insights, and predictive analytics.

## Features 

- Interactive India election dashboard
- 28 states political overview
- Lok Sabha 2024 seat analysis
- NDA vs INDIA alliance breakdown
- Tamil Nadu election deep-dive
- Constituency-level insights
- AI-powered election predictions
- Welfare schemes tracking
- Dynamic state pages
- Charts and visual analytics

---

## Project Structure

india_election_dashboard/

├── run.py  
├── app.py  
├── requirements.txt  

├── database/  
│ ├── __init__.py  
│ ├── seed.py  
│ └── init_db.py  

├── templates/  
│ ├── index.html  
│ ├── tamilnadu.html  
│ ├── predictions.html  
│ └── state.html  

└── static/  
├── css/  
│ ├── main.css  
│ └── tamilnadu.css  

├── js/  
│ ├── main.js  
│ ├── tamilnadu.js  
│ ├── predictions.js  
│ └── state.js  

└── images/

---

## Tech Stack

Frontend:
- HTML
- CSS
- JavaScript

Backend:
- Python
- Flask

Database:
- SQLite
- Flask-SQLAlchemy

Visualization:
- Charts
- Interactive dashboards

---

## Installation

Clone project:

```bash
git clone https://github.com/yourusername/india_election_dashboard.git
cd india_election_dashboard
Create virtual environment:

python -m venv venv

Activate:

Windows

venv\Scripts\activate

Mac/Linux

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Seed database:

python database/seed.py

Run project:

python run.py

Open in browser:

http://localhost:5000
Available Routes

Main Dashboard

/

Tamil Nadu Dashboard

/tamilnadu

Predictions

/predictions

Dynamic State Page Example

/state/UP
Data Included
28 States political data
15 Lok Sabha parties
8 Welfare schemes
10 Key Tamil Nadu constituencies
Candidate information
Election prediction models
Prediction Module

Includes:

Confidence scores
Factor analysis
Trend-based projections
2025–2029 election outlook
Screens Included

Dashboard includes:

Party seat visualizations
State-wise political maps
Constituency insights
Tamil Nadu historical trends
Election prediction charts
Future Improvements
Live election result APIs
Interactive map using OpenStreetMap
Constituency heatmaps
Voter turnout analytics
Real-time polling dashboard
License

Educational / Academic Project

Author

Sarvaji M
B.Tech Information Technology



output:

<img width="1365" height="730" alt="Screenshot 2026-04-26 193112" src="https://github.com/user-attachments/assets/0e659fcb-d40c-493f-a357-f443bc3d8a93" />


