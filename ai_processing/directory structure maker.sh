cd ~/madonna_project

# Create core directories if missing
mkdir -p backend ai_processing data database docker docs frontend notebooks scripts tests logs

# Ensure AI processing folder exists
mkdir -p ai_processing/models ai_processing/config ai_processing/data

# Ensure backend structure
mkdir -p backend/app backend/config backend/routes backend/models backend/services backend/utils

# Ensure database structure
mkdir -p database/migrations database/seed_data

# Ensure Docker directory
mkdir -p docker/volumes

# Create placeholder files
touch backend/main.py backend/requirements.txt backend/Dockerfile
touch ai_processing/Dockerfile ai_processing/requirements.txt
touch database/schema.sql database/init.sql
touch docker/docker-compose.yml
touch README.md .gitignore .env

# Populate .gitignore
cat <<EOL > .gitignore
# Ignore compiled Python files
__pycache__/
*.pyc

# Ignore virtual environment
venv/
.env

# Ignore data & logs
data/raw/
data/embeddings/
logs/

# Ignore Docker volumes
docker/volumes/
docker/mariadb_data/
docker/chroma_data/
EOL

# Ensure permissions
chmod -R 755 ~/madonna_project