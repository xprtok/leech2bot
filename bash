pip install pyrogram tgcrypto mega.py
pip install -r requirements.txt
docker builder prune -a

cat <<EOF > requirements.txt
pyrogram
tgcrypto
mega.py
google-api-python-client
google-auth-oauthlib
aiohttp
aiofiles
requests[socks]
python-magic
tqdm
EOF
