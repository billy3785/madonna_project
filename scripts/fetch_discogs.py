import requests
import json
import mysql.connector

# Discogs API Credentials
DISCOGS_API_KEY = "WfUBmwNEQzcphKBIpZGP"
DISCOGS_SECRET = "rFTxnlgwwuxPfFLPudsGYWVwvrHznHwA"
ARTIST_ID = 8760  # Madonna's Discogs ID

# MariaDB Connection
db = mysql.connector.connect(
    host="madonna_mariadb",
    user="root",
    password="MadonnA816!!@@",
    database="madonna_db"
)
cursor = db.cursor()

# Fetch all Madonna albums from Discogs
url = f"https://api.discogs.com/artists/{ARTIST_ID}/releases?per_page=100"
headers = {"User-Agent": "MadonnaProject"}
response = requests.get(url, headers=headers)
data = response.json()

# Insert into MariaDB
for release in data["releases"]:
    title = release["title"]
    year = release.get("year", None)
    discogs_id = release["id"]

    # Insert album
    cursor.execute("INSERT INTO albums (title, release_year, discogs_id) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE title=title", (title, year, discogs_id))
    db.commit()

print("✅ Albums imported!")