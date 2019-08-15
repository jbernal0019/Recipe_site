#!/bin/bash
#
# NAME
#
#   docker-make.sh
#

source ./decorate.sh

declare -i STEP=0

title -d 1 "Changing permissions to 755 on" " $(pwd)"
echo "chmod -R 755 $(pwd)"
chmod -R 755 $(pwd)
windowBottom

title -d 1 "Starting containerized development environment using " " ./docker-compose.yml"
docker pull jbernal0019/recipe_site:dev
echo "docker-compose up -d"
docker-compose up -d
windowBottom

title -d 1 "Waiting until mysql server is ready to accept connections..."
docker-compose exec recipe_site_dev_db sh -c 'while ! mysqladmin -uroot -prootp status 2> /dev/null; do sleep 5; done;'
# Give all permissions to chris user in the DB. This is required for the Django tests:
docker-compose exec recipe_site_dev_db mysql -uroot -prootp -e 'GRANT ALL PRIVILEGES ON *.* TO "recipe"@"%"'
windowBottom

title -d 1 "Running Django Unit tests..."
docker-compose exec recipe_site_dev python manage.py test
windowBottom

title -d 1 "Creating a Recipe site API user"
echo ""
echo "Setting user cook:cook1234"
docker-compose exec recipe_site_dev /bin/bash -c 'python manage.py createsuperuser --noinput --username cook --email cook@server.org 2> /dev/null;'
docker-compose exec recipe_site_dev /bin/bash -c \
'python manage.py shell -c "from django.contrib.auth.models import User; user = User.objects.get(username=\"cook\"); user.set_password(\"cook1234\"); user.save()"'
echo ""
windowBottom

title -d 1 "Restarting Recipe sites's Django development server" "in interactive mode..."
docker-compose stop recipe_site_dev
docker-compose rm -f recipe_site_dev
docker-compose run --service-ports recipe_site_dev
echo ""
windowBottom
