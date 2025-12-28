import requests
import random
from utils.config import Config

class ApiClient:
    """Клиент для работы с API Stellar Burgers"""
    
    def __init__(self):
        self.base_url = Config.API_URL
    
    def register_user(self, email, password, name=None):
        """Регистрация нового пользователя"""
        if name is None:
            name = f"{Config.TEST_USER_NAME_PREFIX}{random.randint(1000, 9999)}"
        
        url = f"{self.base_url}/auth/register"
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка регистрации: {response.status_code} - {response.text}")
    
    def login_user(self, email, password):
        """Вход пользователя"""
        url = f"{self.base_url}/auth/login"
        payload = {
            "email": email,
            "password": password
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка входа: {response.status_code} - {response.text}")
    
    def delete_user(self, access_token):
        """Удаление пользователя"""
        url = f"{self.base_url}/auth/user"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.delete(url, headers=headers)
        return response.status_code in [200, 202]
    
    def create_order(self, access_token, ingredients):
        """Создание заказа"""
        url = f"{self.base_url}/orders"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "ingredients": ingredients
        }
        
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка создания заказа: {response.status_code} - {response.text}")
    
    def get_user_orders(self, access_token):
        """Получение заказов пользователя"""
        url = f"{self.base_url}/orders"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка получения заказов: {response.status_code} - {response.text}")

