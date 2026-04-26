from flask import Flask, render_template, jsonify, request
import sqlite3, os
from datetime import datetime, date

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), "database", "election.db")

def qdb(sql, args=()):
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(sql, args).fetchall()]
    conn.close()
    return rows

def days_since(date_str):
    try:
        fmt = "%Y-%m" if len(date_str) == 7 else "%Y"
        d = datetime.strptime(date_str, fmt).date()
        return max(0, (date.today() - d).days)
    except Exception:
        return 0

def days_until(date_str):
    try:
        d = datetime.strptime(date_str, "%Y-%m-%d").date()
        return max(0, (d - date.today()).days)
    except Exception:
        return 0

def enrich_state(s):
    s["days_ruling"] = days_since(s["ruling_since"])
    s["years_ruling"] = round(s["days_ruling"] / 365, 1)
    s["days_to_election"] = days_until(s["next_election"])
    return s

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tamilnadu")
def tamilnadu():
    return render_template("tamilnadu.html")

@app.route("/predictions")
def predictions():
    return render_template("predictions.html")

@app.route("/state/<code>")
def state_page(code):
    return render_template("state.html", state_code=code.upper())

@app.route("/api/dashboard")
def api_dashboard():
    states = qdb("""
        SELECT s.*, p.name AS party_name, p.abbr, p.color, p.symbol, p.logo, p.alliance
        FROM states s JOIN parties p ON s.ruling_party_id = p.id
        ORDER BY s.population DESC
    """)
    for s in states:
        enrich_state(s)
    ls_2024 = qdb("""
        SELECT l.*, p.name, p.abbr, p.color, p.symbol, p.logo, p.alliance
        FROM lok_sabha l JOIN parties p ON l.party_id = p.id
        WHERE l.year = 2024 ORDER BY l.seats_won DESC
    """)
    tally = qdb("""
        SELECT p.name, p.abbr, p.color, p.symbol, p.alliance, p.logo,
               COUNT(s.id) AS states_ruled
        FROM parties p LEFT JOIN states s ON s.ruling_party_id = p.id
        GROUP BY p.id HAVING states_ruled > 0 ORDER BY states_ruled DESC
    """)
    upcoming = sorted(
        [{"state": s["name"], "code": s["code"], "date": s["next_election"],
          "ruling": s["party_name"], "color": s["color"], "days": s["days_to_election"]}
         for s in states if s["days_to_election"] > 0],
        key=lambda x: x["days"]
    )[:8]
    nda = sum(1 for s in states if "NDA" in (s.get("alliance") or ""))
    india = sum(1 for s in states if "INDIA" in (s.get("alliance") or ""))
    return jsonify({"states": states, "lok_sabha": ls_2024, "tally": tally,
                    "upcoming": upcoming, "nda_states": nda, "india_states": india})

@app.route("/api/state/<code>")
def api_state(code):
    rows = qdb("""
        SELECT s.*, p.name AS party_name, p.abbr, p.color, p.symbol, p.logo,
               p.description AS party_desc, p.alliance
        FROM states s JOIN parties p ON s.ruling_party_id = p.id
        WHERE UPPER(s.code) = ?
    """, (code.upper(),))
    if not rows:
        return jsonify({"error": "Not found"}), 404
    state = enrich_state(rows[0])
    results = qdb("""
        SELECT ar.*, p.name AS party_name, p.abbr, p.color, p.symbol, p.logo
        FROM assembly_results ar JOIN parties p ON ar.party_id = p.id
        WHERE ar.state_id = ? ORDER BY ar.year DESC, ar.seats_won DESC
    """, (state["id"],))
    candidates = qdb("""
        SELECT c.*, p.name AS party_name, p.abbr, p.color, p.logo
        FROM candidates c JOIN parties p ON c.party_id = p.id
        WHERE c.state_id = ?
    """, (state["id"],))
    preds = qdb("""
        SELECT pr.*, p.name AS party_name, p.abbr, p.color
        FROM predictions pr JOIN parties p ON pr.party_id = p.id
        WHERE pr.state_id = ? ORDER BY pr.predicted_seats DESC
    """, (state["id"],))
    return jsonify({"state": state, "results": results, "candidates": candidates, "predictions": preds})

@app.route("/api/tamilnadu")
def api_tamilnadu():
    state = enrich_state(qdb("""
        SELECT s.*, p.name AS party_name, p.color, p.logo, p.alliance
        FROM states s JOIN parties p ON s.ruling_party_id = p.id WHERE s.code='TN'
    """)[0])
    results = qdb("""
        SELECT ar.*, p.name AS party_name, p.abbr, p.color, p.symbol, p.logo
        FROM assembly_results ar JOIN parties p ON ar.party_id = p.id
        WHERE ar.state_id=1 ORDER BY ar.year DESC, ar.seats_won DESC
    """)
    candidates = qdb("""
        SELECT c.*, p.name AS party_name, p.abbr, p.color, p.logo
        FROM candidates c JOIN parties p ON c.party_id = p.id WHERE c.state_id=1
    """)
    preds = qdb("""
        SELECT pr.*, p.name AS party_name, p.abbr, p.color
        FROM predictions pr JOIN parties p ON pr.party_id = p.id WHERE pr.state_id=1
    """)
    history = [
        {"party":"DMK","color":"#E60026","y1989":150,"y1991":0,"y1996":173,"y2001":31,"y2006":96,"y2011":23,"y2016":89,"y2021":159},
        {"party":"AIADMK","color":"#006400","y1989":27,"y1991":164,"y1996":4,"y2001":132,"y2006":61,"y2011":150,"y2016":136,"y2021":66},
        {"party":"INC","color":"#19A84B","y1989":25,"y1991":63,"y1996":11,"y2001":9,"y2006":34,"y2011":5,"y2016":8,"y2021":18},
        {"party":"BJP","color":"#FF6B00","y1989":0,"y1991":0,"y1996":0,"y2001":4,"y2006":0,"y2011":0,"y2016":0,"y2021":4},
    ]
    welfare = [
        {"name":"Kalaignar Magalir Urimai Thittam","beneficiaries":"1.06 Cr women","amount":"₹1,000/month","year":2023},
        {"name":"CM Breakfast Scheme","beneficiaries":"2.5 L students","amount":"Free breakfast","year":2022},
        {"name":"Pudhumai Penn","beneficiaries":"6 L girls","amount":"₹1,000/month","year":2023},
        {"name":"Illam Thedi Kalvi","beneficiaries":"25 L students","amount":"Free tutoring","year":2021},
        {"name":"CM Health Insurance","beneficiaries":"1.56 Cr families","amount":"₹5 L cover","year":2022},
        {"name":"Naan Mudhalvan","beneficiaries":"10 L youth","amount":"Skill training","year":2022},
        {"name":"Makkalai Thedi Maruthuvam","beneficiaries":"90 L+","amount":"Doorstep healthcare","year":2021},
        {"name":"Green Tamil Nadu Mission","beneficiaries":"All Districts","amount":"₹8,500 Cr","year":2023},
    ]
    constituencies = [
        {"name":"Kolathur","incumbent":"DMK","color":"#E60026","margin":25000,"status":"CM Stronghold"},
        {"name":"Chepauk-Thiruvallikeni","incumbent":"DMK","color":"#E60026","margin":12000,"status":"Dy. CM"},
        {"name":"Edappadi","incumbent":"AIADMK","color":"#006400","margin":4500,"status":"EPS Stronghold"},
        {"name":"Coimbatore South","incumbent":"BJP","color":"#FF6B00","margin":1360,"status":"Competitive"},
        {"name":"Madurai East","incumbent":"DMK","color":"#E60026","margin":18200,"status":"Safe DMK"},
        {"name":"Trichy West","incumbent":"DMK","color":"#E60026","margin":11200,"status":"Safe DMK"},
        {"name":"Salem West","incumbent":"AIADMK","color":"#006400","margin":3200,"status":"Competitive"},
        {"name":"Tirunelveli","incumbent":"DMK","color":"#E60026","margin":14600,"status":"Safe DMK"},
        {"name":"Vellore","incumbent":"DMK","color":"#E60026","margin":9800,"status":"Safe DMK"},
        {"name":"Dharmapuri","incumbent":"DMK","color":"#E60026","margin":7100,"status":"Alliance"},
    ]
    return jsonify({"state":state,"results":results,"candidates":candidates,
                    "predictions":preds,"history":history,"welfare":welfare,"constituencies":constituencies})

@app.route("/api/predictions")
def api_predictions():
    preds = qdb("""
        SELECT pr.*, p.name AS party_name, p.abbr, p.color, p.logo,
               s.name AS state_name, s.code AS state_code
        FROM predictions pr
        JOIN parties p ON pr.party_id = p.id
        LEFT JOIN states s ON pr.state_id = s.id
        ORDER BY pr.election_year, pr.confidence DESC
    """)
    return jsonify({"predictions": preds})

@app.route("/api/parties")
def api_parties():
    parties = qdb("""
        SELECT p.*, COUNT(s.id) AS states_ruled
        FROM parties p LEFT JOIN states s ON s.ruling_party_id = p.id
        GROUP BY p.id ORDER BY states_ruled DESC
    """)
    return jsonify({"parties": parties})

if __name__ == "__main__":
    if not os.path.exists(DB):
        import sys; sys.path.insert(0, os.path.dirname(__file__))
        from database.seed import seed; seed()
    app.run(debug=True, port=5000)
