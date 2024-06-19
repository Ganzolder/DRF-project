import re
from rest_framework.serializers import ValidationError

url_pattern = re.compile(r'https?://[^\s]+')

# проверка URLов, которые не ведут на youtube.com

forbidden_pattern = re.compile(r'https?://(?!www\.youtube\.com|youtube\.com)[^\s]+')


def validate_materials(text):
    # Ищем все URL в тексте
    urls = url_pattern.findall(text)

    # Проверяем, есть ли среди найденных URL запрещенные
    forbidden_urls = [url for url in urls if forbidden_pattern.match(url)]

    if forbidden_urls:
        raise ValidationError("Запрещенные ссылки найдены.")


