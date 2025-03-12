import requests
import mysql.connector

# Setlist.fm API Credentials
SETLIST_API_KEY = "rW4Z_ERv3kVKUWMp9QvekOZo-_ikff4iCWQy"
ARTIST_MBID = "79239441-bfd5-4981-a70c-55c3f15c1287"

# MariaDB Connection (replace YOUR_DB_PASSWORD!)
db = mysql.connector.connect(
    host="127.0.0.1",  # or "localhost" if running locally
    port=3306,
    user="root",
    password="MadonnA816!!@@",  # <-- Put your actual DB password here
    database="madonna_db"
)
cursor = db.cursor()

# Setlist.fm endpoint for Madonna setlists
url = f"https://api.setlist.fm/rest/1.0/artist/{ARTIST_MBID}/setlists?p=1"
headers = {
    "x-api-key": SETLIST_API_KEY,
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"Failed to retrieve setlists: {response.status_code}")
    exit()

data = response.json()

# Insert setlists into MariaDB
for setlist in data.get("setlist", []):
    venue_name = setlist["venue"]["name"]
    city = setlist["venue"]["city"]["name"]
    country = setlist["venue"]["city"]["country"]["code"]
    event_date = setlist["eventDate"]  # format DD-MM-YYYY, we'll need to convert it to YYYY-MM-DD
    
    # Convert date
    event_date_converted = '-'.join(reversed(event_date.split('-')))

    # Insert venue (avoid duplicates)
    cursor.execute("""
        INSERT INTO venues (name, city, country) 
        VALUES (%s, %s, %s) 
        ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)
    """, (venue_name, city, country))
    venue_id = cursor.lastrowid

    # Insert setlist entry
    cursor.execute("""
        INSERT INTO setlists (venue_id, event_date) 
        VALUES (%s, %s)
    """, (venue_id, event_date_converted))
    setlist_id = cursor.lastrowid

    # Insert songs into setlist_songs
    songs = setlist.get("sets", {}).get("set", [])
    position = 1
    for song_set in songs:
        for song in song_set.get("song", []):
            song_name = song["name"]

            # Insert song if it doesn't exist
            cursor.execute("""
                INSERT INTO songs (title) 
                VALUES (%s) 
                ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)
            """, (song_name,))
            song_id = cursor.lastrowid

            # Associate song with setlist
            cursor.execute("""
                INSERT INTO setlist_songs (setlist_id, song_id, position) 
                VALUES (%s, %s, %s)
            """, (setlist_id, song_id, position))
            position += 1

    db.commit()

print("✅ Setlists and songs successfully imported!")
cursor.close()
db.close()