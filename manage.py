#!/usr/bin/env python

import os
import sys


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
