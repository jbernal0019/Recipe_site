#!/bin/bash

# Start Recipe_site server
python check_db_connection.py -u recipe -p Recipe1234 -d recipe_site_dev --host recipe_site_dev_db --max-attempts 30
python manage.py migrate
python manage.py runserver 0.0.0.0:8080

exec "$@"
