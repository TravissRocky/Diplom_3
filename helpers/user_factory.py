import os
import random
import string
from dataclasses import dataclass
from typing import Dict


def _random_string(length: int = 8) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(random.choice(alphabet) for _ in range(length))


def generate_user_credentials() -> Dict[str, str]:
    base_password = os.getenv('STELLAR_TEST_PASSWORD', 'Qwerty123')
    return {
        'name': f'UI Tester {_random_string(4)}',
        'email': f'autotest_{_random_string(6)}@example.com',
        'password': base_password,
    }
