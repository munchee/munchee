#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    try:
        a = os.environ["DJANGO_KEY"]
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_azure")
    except KeyError:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "munchee.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
