import requests
import pymysql
import time

# Discogs API Credentials
DISCOGS_USER_TOKEN = "aWwgicoZNDeHcbTHuIeIJThhZmeInCulYUmzRSNK"
ARTIST_ID = 8760  # Madonna's Discogs ID
PER_PAGE = 100  # Discogs API pagination limit

# MariaDB Connection
db = pymysql.connect(
    host="madonna_mariadb",
    user="billy",
    password="MadonnA816!!@@",
    database="madonna_archive",
    cursorclass=pymysql.cursors.DictCursor
)
cursor = db.cursor()

# Function to fetch releases from Discogs (handling pagination)
def fetch_releases():
    releases = []
    page = 1
    while True:
        url = f"https://api.discogs.com/artists/{ARTIST_ID}/releases?page={page}&per_page={PER_PAGE}"
        headers = {
            "User-Agent": "MadonnaProject",
            "Authorization": f"Discogs token={DISCOGS_USER_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        data = response.json()

        if "releases" not in data:
            print(f"❌ API Error: {data.get('message', 'Unknown error')}")
            break

        releases.extend(data["releases"])

        # Stop if there's no more data
        if "pagination" in data and data["pagination"]["pages"] <= page:
            break

        page += 1
        time.sleep(1)  # Prevent API rate limiting

    return releases

# Fetch releases
all_releases = fetch_releases()

# Process each release
for release in all_releases:
    try:
        discogs_id = release.get("id")
        title = release.get("title")

        # Fetch detailed release info
        release_url = f"https://api.discogs.com/releases/{discogs_id}"
        release_data = requests.get(release_url, headers=headers).json()

        formats = ", ".join([f.get("name", "") for f in release_data.get("formats", [])]) if "formats" in release_data else ""
        label_info = release_data.get("labels", [{}])[0].get("name", "Unknown")
        catalog_number = release_data.get("labels", [{}])[0].get("catno", "")
        country = release_data.get("country", "Unknown")
        release_date = release_data.get("released", "0000-00-00")

        # Insert album (ensuring correct column naming)
        cursor.execute("""
            INSERT INTO albums (title, release_date, discogs_id, formats, label, catalog_number, country)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
            title=VALUES(title), release_date=VALUES(release_date), 
            formats=VALUES(formats), label=VALUES(label), 
            catalog_number=VALUES(catalog_number), country=VALUES(country)
        """, (title, release_date, discogs_id, formats, label_info, catalog_number, country))

        # Get the album_id (handle duplicate entries properly)
        cursor.execute("SELECT id FROM albums WHERE discogs_id = %s", (discogs_id,))
        album_result = cursor.fetchone()
        if album_result:
            album_id = album_result["id"]
        else:
            album_id = cursor.lastrowid

        # Insert tracklist
        for track in release_data.get("tracklist", []):
            track_title = track.get("title")
            duration = track.get("duration", None)

            # Insert or retrieve master song
            cursor.execute("INSERT INTO master_songs (title) VALUES (%s) ON DUPLICATE KEY UPDATE title=VALUES(title)", (track_title,))
            master_song_id = cursor.lastrowid or cursor.execute("SELECT id FROM master_songs WHERE title = %s", (track_title,)).fetchone()["id"]

            # Insert into songs, linking it to master_songs
            cursor.execute("""
                INSERT INTO songs (title, duration, master_song_id)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE title=VALUES(title)
            """, (track_title, duration, master_song_id))
            song_id = cursor.lastrowid or cursor.execute("SELECT id FROM songs WHERE title = %s", (track_title,)).fetchone()["id"]

            # Ensure album-song mapping
            cursor.execute("""
                INSERT INTO song_album (song_id, album_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE song_id=song_id
            """, (song_id, album_id))

        # Insert credits
        for credit in release_data.get("extraartists", []):
            person_name = credit.get("name")
            role = credit.get("role")

            cursor.execute("INSERT INTO people (name) VALUES (%s) ON DUPLICATE KEY UPDATE name=name", (person_name,))
            person_id = cursor.lastrowid or cursor.execute("SELECT id FROM people WHERE name = %s", (person_name,)).fetchone()["id"]

            cursor.execute("""
                INSERT INTO song_credits (song_id, person_id, role)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE role=VALUES(role)
            """, (song_id, person_id, role))

        # Insert images
        for image in release_data.get("images", []):
            image_url = image.get("uri")
            cursor.execute("""
                INSERT INTO release_images (album_id, url)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE url=VALUES(url)
            """, (album_id, image_url))

        db.commit()
        print(f"✅ Successfully inserted: {title}")

    except Exception as e:
        print(f"❌ Error processing release {release.get('title', 'Unknown')}: {e}")

cursor.close()
db.close()
print("✅ Discogs releases imported successfully!")