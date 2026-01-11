pip install pyrogram tgcrypto mega.py
pip install -r requirements.txt
docker builder prune -a
docker-compose build --no-cache
docker-compose up -d
docker logs -f telegram_leech_bot
