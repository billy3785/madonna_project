import requests
import pymysql

# ✅ Setlist.fm API details
MBID = "79239441-bfd5-4981-a70c-55c3f15c1287"
base_url = f"https://api.setlist.fm/rest/1.0/artist/{MBID}/setlists"
headers = {
    "Accept": "application/json",
    "x-api-key": "rW4Z_ERv3kVKUWMp9QvekOZo-_ikff4iCWQy",
    "User-Agent": "MadonnaProject/1.0"
}

# ✅ Database connection using pymysql
db = pymysql.connect(
    host="madonna_mariadb",
    user="billy",
    password="MadonnA816!!@@",
    database="madonna_archive",
    cursorclass=pymysql.cursors.DictCursor
)
cursor = db.cursor()

# ✅ Insert setlist data safely into the database
def insert_setlist(date, venue, city, country, tour_name, songs):
    try:
        cursor.execute("""
            INSERT INTO setlists (event_date, venue, city, country, tour_name)
            VALUES (%s, %s, %s, %s, %s)
        """, (date, venue, city, country, tour_name))

        setlist_id = cursor.lastrowid

        for song in songs:
            cursor.execute("""
                INSERT INTO songs (title) VALUES (%s)
                ON DUPLICATE KEY UPDATE title=title
            """, (song,))
            song_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO setlist_songs (setlist_id, song_id)
                VALUES (%s, %s)
            """, (setlist_id, cursor.lastrowid))

        db.commit()
    except Exception as e:
        print(f"❌ Error inserting setlist: {e}")
        db.rollback()

# ✅ Fetch setlists with pagination and error handling
def fetch_and_store_setlists():
    page = 1
    while True:
        params = {"p": page}
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            break

        data = response.json()
        setlists = data.get("setlist", [])

        if not setlists:
            print("🔍 No further setlists found.")
            break

        for setlist in setlists:
            date = setlist.get('eventDate')
            venue = setlist.get('venue', {}).get('name')
            city = setlist.get('venue', {}).get('city', {}).get('name')
            country = setlist.get('venue', {}).get('city', {}).get('country', {}).get('name')
            tour_name = setlist.get('tour', {}).get('name')
            songs = [s.get('name') for s in setlist.get('sets', {}).get('set', [])[0].get('song', [])]

            insert_setlist(date, venue, city, country, tour_name, songs)

        print(f"➡️ Page {page} processed successfully.")
        page += 1

# ✅ Run the script
if __name__ == "__main__":
    print("🚀 Starting Setlist.fm fetch script...")
    fetch_and_store_setlists()
    db.close()
    print("✅ Setlist fetch and storage completed.")