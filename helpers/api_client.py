from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import requests

from data.urls import API_BASE_URL


@dataclass
class ApiResponse:
    success: bool
    body: Dict


class StellarApiClient:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url.rstrip('/')

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _request(self, method: str, path: str, json: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict:
        response = requests.request(method, self._url(path), json=json, headers=headers)
        response.raise_for_status()
        return response.json()

    def create_user(self, name: str, email: str, password: str) -> Dict:
        payload = {"name": name, "email": email, "password": password}
        return self._request('POST', '/auth/register', json=payload)

    def login_user(self, email: str, password: str) -> Dict:
        payload = {"email": email, "password": password}
        return self._request('POST', '/auth/login', json=payload)

    def delete_user(self, access_token: str) -> None:
        headers = {"Authorization": access_token}
        response = requests.delete(self._url('/auth/user'), headers=headers)
        if response.status_code not in (200, 202, 204):
            response.raise_for_status()

    def get_ingredients(self) -> List[Dict]:
        data = self._request('GET', '/ingredients')
        return data.get('data', [])

    def create_order(self, ingredient_ids: List[str], access_token: Optional[str] = None) -> Dict:
        headers = {"Content-Type": "application/json"}
        if access_token:
            headers["Authorization"] = access_token
        payload = {"ingredients": ingredient_ids}
        return self._request('POST', '/orders', json=payload, headers=headers)

    def get_orders_feed(self) -> Dict:
        return self._request('GET', '/orders/all')

    def get_user_orders(self, access_token: str) -> Dict:
        headers = {"Authorization": access_token}
        return self._request('GET', '/orders', headers=headers)
