#!/usr/bin/env python

import os
import sys

from pathlib import Path
from scraper_api_service.settings import BASE_DIR
print(BASE_DIR / 'db.sqlite3')
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scraper_api_service.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django import qilinmadi. Django o‘rnatilganini va virtual muhit to‘g‘ri yoqilganini tekshiring."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
