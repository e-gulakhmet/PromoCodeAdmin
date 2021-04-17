from app.settings import BASE_DIR
import os
from django.apps import AppConfig
import os


class PromoCodeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'promo_code'
    promo_codes_file_path = os.path.join(BASE_DIR, name, "data", "promo_codes.json")
