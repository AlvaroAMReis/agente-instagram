import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
BASE_URL = "https://graph.instagram.com"

def get_profile():
    """Busca informações básicas do perfil"""
    url = f"{BASE_URL}/me"
    params = {
        "fields": "id,username,account_type,media_count",
        "access_token": TOKEN
    }
    response = requests.get(url, params=params)
    return response.json()

def get_posts():
    """Busca os últimos posts"""
    url = f"{BASE_URL}/me/media"
    params = {
        "fields": "id,caption,media_type,timestamp,like_count,comments_count",
        "access_token": TOKEN
    }
    response = requests.get(url, params=params)
    return response.json()
