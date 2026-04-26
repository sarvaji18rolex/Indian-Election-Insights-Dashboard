"""Entry point — seeds DB if needed, then starts Flask."""
import os, sys

BASE = os.path.dirname(__file__)
DB   = os.path.join(BASE, "database", "election.db")

if not os.path.exists(DB):
    sys.path.insert(0, BASE)
    from database.seed import seed
    seed()

from app import app
app.run(debug=True, port=5000)
