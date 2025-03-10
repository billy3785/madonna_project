Here’s a detailed README.md for your project, incorporating all the latest updates and ensuring clarity for future development.

⸻

Madonna Archive Project

A Comprehensive AI-Powered Database for Madonna’s Career & History

🚀 Goal: To build the most structured, AI-powered Madonna archive, integrating concert history, music discography, media metadata, and AI-based entity recognition—all while using free and open-source tools.

⸻

📌 Project Overview

This project is designed to ingest, clean, and structure raw historical data from text files, JSON metadata, and media files. The final product will allow advanced search, AI-powered metadata tagging, and database-backed browsing of Madonna’s career.

🔹 Core Functionalities

✔ Ingest & Normalize Data → Process raw text, JSON, and media files into structured formats.
✔ Prevent Duplicates → Detect & merge redundant posts with identical captions.
✔ AI-Powered Image Recognition → Identify faces, locations, and objects in photos.
✔ Concert & Setlist Tracking → Scrape Setlist.fm for every Madonna concert & song performance.
✔ Discography Integration → Scrape Discogs for album/single releases, tracklists, and production credits.
✔ Embed Metadata in Media Files → Store structured data inside EXIF metadata of images & videos.

⸻

📌 Technologies Used

🛠 Core Stack
	•	MariaDB → Relational database for structured storage.
	•	ChromaDB → AI-powered vector search for metadata retrieval.
	•	FastAPI → Backend API for querying and integrating data.
	•	Docker → Containerized deployment of all services.

🤖 AI Processing Tools (100% Free & Open Source)
	•	OCR (Text from Images) → Tesseract OCR
	•	Face Recognition → DeepFace / InsightFace
	•	Object Detection → YOLOv8 / Detectron2
	•	Handwritten Text Extraction → Tesseract OCR + Custom AI Models
	•	Text Embeddings & Search → Hugging Face Sentence Transformers
	•	Named Entity Recognition (NER) → spaCy / Haystack

🔗 External Data Sources
	•	Setlist.fm → Complete Madonna concert & setlist history.
	•	Discogs API → Madonna’s full album & tracklist data.
	•	Google Vision API (Free Tier) → Landmark & location detection in images.

⸻

📌 Project Architecture

madonna_project/
│── backend/                 # FastAPI application for API endpoints
│── ai_processing/           # AI-based metadata extraction & recognition
│── data/                    # Storage for raw & processed data
│── docker/                  # Docker configuration files
│── notebooks/               # Jupyter notebooks for data analysis
│── scripts/                 # Utility scripts (data normalization, scraping)
│── media/                   # Image & video storage
│── README.md                # Project documentation
│── docker-compose.yml       # Docker configuration for services
│── .gitignore               # Ignore unnecessary files in Git



⸻

📌 Services (Docker)

This project is fully containerized using Docker. Here’s an overview of the key services:

Service	Description	Port
mariadb	Relational DB for structured data	3306
chromadb	AI-powered vector search	8001
fastapi	Backend API for querying data	8000
adminer	Web UI for MariaDB management	8080
ai_processing	AI-powered face/object/OCR detection	5000

🔹 Running the Project

To start all services, run:

docker-compose up -d



⸻

📌 Data Ingestion Process

1️⃣ Extract & Normalize Text Data
	•	Read raw text files inside each post’s metadata folder.
	•	Standardize dates, converting descriptive values (“Late Summer 1982” → 1982-08-15).
	•	Extract locations from captions & geotags, formatting them as structured venue/city/state/country fields.
	•	Detect & prevent duplicate events based on captions, date ranges, and locations.

2️⃣ Scrape & Structure External Data
	•	Setlist.fm → Fetch Madonna’s entire concert history, setlists, venues, & cities.
	•	Discogs → Scrape Madonna’s master album releases, tracklists, & production credits.
	•	Merge external data with our existing structured database.

3️⃣ AI-Based Image & Video Processing
	•	Detect faces & match to known people (DeepFace).
	•	Identify landmarks & venues (Google Vision API).
	•	Extract handwritten text (Tesseract OCR for scanned setlists, notes).
	•	Tag objects in images (YOLOv8 for props, microphones, outfits).

4️⃣ Store & Embed Metadata
	•	Write structured metadata back into media files as EXIF data.
	•	Ensure all images/videos maintain metadata, even if copied to another system.

⸻

📌 Database Schema

🔹 Key Tables

Table	Purpose
concerts	Stores all Madonna concerts (Setlist.fm)
concert_setlists	Links concerts to songs performed
albums	Stores album, single, and compilation info (Discogs)
songs	Master song database (studio, live, remix versions)
people	Tracks key people (producers, photographers, directors)
media_files	Stores images/videos with extracted metadata
extracted_text	Stores AI-extracted OCR text from images



⸻

📌 API Endpoints (FastAPI)

🎵 Music Data

✅ GET /albums → Get all Madonna albums from Discogs
✅ GET /songs → Get all songs, linking to albums & live performances

🎤 Concert Data

✅ GET /concerts → Get all Madonna concerts from Setlist.fm
✅ GET /concerts/{concert_id}/setlist → Get songs performed at a specific concert

🖼 AI-Powered Image Processing

✅ POST /detect_faces → Detect faces in an image
✅ POST /extract_text → OCR processing for scanned documents
✅ POST /detect_objects → Recognize props & objects in a photo

⸻

📌 Next Steps & Priorities

✅ Verify all Docker services & commit updates
✅ Run the first AI normalization scripts (structured metadata extraction)
✅ Complete Setlist.fm & Discogs API integrations
✅ Embed metadata into media files (EXIF write-back)

⸻

📌 How to Contribute

1️⃣ Clone the repo:

git clone https://github.com/billy3785/madonna_project.git

2️⃣ Start services:

docker-compose up -d

3️⃣ Run normalization scripts:

python scripts/normalize_data.py

4️⃣ Test API requests using FastAPI UI:

http://127.0.0.1:8000/docs



⸻

📌 Final Confirmation Before We Start

✅ This README now fully reflects our latest architecture.
✅ Your Docker setup is up-to-date and committed.
✅ We’re ready to run the normalization scripts.

🚀 Let me know when you’re ready to start running the scripts!