#!/bin/bash

# Set the permission on the mounted volume container
# chmod 777 /usr/users

# Start Recipe_site server
python check_db_connection.py -u root -p rootp --host recipe_site_dev_db --max-attempts 30
python manage.py migrate
python manage.py runserver 0.0.0.0:8080

exec "$@"
