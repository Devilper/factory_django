# vim: set noet:
default:
    check
check:
    python manage.py check

run:
    python manage.py runserver 0.0.0.0:8000

.PHONY: default run