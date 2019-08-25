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

title -d 1 "Waiting until database server is ready to accept connections..."
docker-compose exec recipe_site_dev_db sh -c 'while ! psql -U recipe -d recipe_site_dev -c "select 1" 2> /dev/null; do sleep 5; done;'
windowBottom

title -d 1 "Running Django Unit tests..."
docker-compose exec recipe_site_dev python manage.py test
windowBottom

title -d 1 "Restarting Recipe sites's Django development server" "in interactive mode..."
docker-compose stop recipe_site_dev
docker-compose rm -f recipe_site_dev
docker-compose run --service-ports recipe_site_dev
echo ""
windowBottom
