#!/usr/bin/env python
import os
import sys

PROJECT_DIR = os.path.abspath(__file__)
SETTINGS_DIR = os.path.join(PROJECT_DIR, 'django_url_shortener', 'settings')
LOCAL_SETTINGS = os.path.join(SETTINGS_DIR, 'local')
PRODUCTION_SETTINGS = os.path.join(SETTINGS_DIR, 'production')

sys.path.append(PROJECT_DIR)
sys.path.append(SETTINGS_DIR)
sys.path.append(LOCAL_SETTINGS)
sys.path.append(PRODUCTION_SETTINGS)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "local.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
