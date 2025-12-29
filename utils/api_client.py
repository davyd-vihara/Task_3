import requests
import random
from config.urls import Urls
from config.constants import Constants

class ApiClient:
    """Клиент для работы с API Stellar Burgers"""
    
    def __init__(self):
        self.base_url = Urls.API_URL
    
    def register_user(self, email, password, name=None):
        """Регистрация нового пользователя"""
        if name is None:
            name = f"{Constants.TEST_USER_NAME_PREFIX}{random.randint(1000, 9999)}"
        
        url = f"{self.base_url}/auth/register"
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        
        response = requests.post(url, json=payload)
        
        # Проверяем статус код
        if response.status_code == 200:
            # Проверяем, что ответ не пустой
            if not response.text:
                raise Exception(f"API вернул пустой ответ. Status: {response.status_code}")
            
            try:
                response_data = response.json()
            except Exception as e:
                raise Exception(f"Не удалось распарсить JSON ответ. Status: {response.status_code}, Text: {response.text[:200]}, Error: {e}")
            
            # Проверяем, что в ответе есть accessToken
            if "accessToken" not in response_data:
                raise Exception(f"В ответе API отсутствует accessToken. Ответ: {response_data}")
            return response_data
        else:
            # Если пользователь уже существует (403), это нормально
            if response.status_code == 403:
                raise Exception(f"Пользователь уже существует: {email}")
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
        # В референсе используется просто токен без "Bearer " в заголовке
        # Но API может требовать "Bearer ", поэтому пробуем оба варианта
        token = access_token.replace("Bearer ", "") if access_token else access_token
        headers = {
            "Authorization": token  # Как в референсе - просто токен
        }
        
        response = requests.delete(url, headers=headers)
        # Если не сработало с простым токеном, пробуем с Bearer
        if response.status_code not in [200, 202]:
            headers = {
                "Authorization": f"Bearer {token}"
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
        # Убираем префикс "Bearer " если он есть
        token = access_token.replace("Bearer ", "") if access_token else access_token
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Ошибка получения заказов: {response.status_code} - {response.text}")

