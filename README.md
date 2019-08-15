# Recipe_site


Back end for Recipe site. This is a Django-MySQL project.

## Recipe site development and testing

### Abstract

This page describes how to quickly get the set of services comprising the backend up and running for development and testing.

### Preconditions

#### Install latest Docker and Docker Compose. Currently tested platforms
* ``Docker 17.04.0+``
* ``Docker Compose 1.10.0+``
* ``Ubuntu (16.04+) and MAC OS X 10.11+``

#### If you are using a Linux machine then make sure to add your computer user to the ``docker group``. 


#### Checkout the Github repo
```bash
git clone https://github.com/jbernal0019/Recipe_site.git
```

### Instantiate Recipe site

Start Recipe site from the repository source directory by running the make bash script:

```bash
./docker-make.sh
```
All the steps performed by the above script are properly documented in the script itself. 

After running this script all the automated tests should have successfully run and a Django development server should be running in interactive mode in this terminal.

### Playing with the REST API 

This API uses the standard [Collection+JSON](http://amundsen.com/media-types/collection/) hypermedia type to exchange resource representations with clients. 
All the functionality provided by the API can be discovered by clients by doing `GET` requests to links (`href`elements) presented by the hypermedia documents returned by the web server, starting with the API’s “home page”.
As such the amount of required human-readable documentation is greatly minimized.
The only non-standard property that I have added to the hypermedia document format is `total` which gives the total number of items across all API pages.

The API’s “home page” relative url is: /api/v1/ which serves a list of recipes.

#### A simple unauthenticated GET request:

Using curl:

```bash
curl http://localhost:8080/api/v1/
```

Using [HTTPie](https://httpie.org/) REST API client:

```bash
http http://localhost:8080/api/v1/
```

#### Create a new user to be able to make authenticated requests:

Using curl:

```bash
curl -XPOST -H 'Content-Type: application/vnd.collection+json' -H 'Accept: application/vnd.collection+json' -d '{"template":{"data":[{"name":"username","value":"user"}, {"name":"email","value":"user@server.com"}, {"name":"password","value":"user1234"}]}}' 'http://localhost:8080/api/v1/users/'
```

Using [HTTPie](https://httpie.org/) REST API client:

```bash
http POST http://localhost:8080/api/v1/users/ template:='{"data":[{"name":"username","value":"user"}, {"name":"email","value":"user@server.com"}, {"name":"password","value":"user1234"}]}' Content-Type:application/vnd.collection+json Accept:application/vnd.collection+json
```

#### A simple POST request to create a new recipe:

Using curl:

```bash
curl -u user:user1234 -XPOST -H 'Content-Type: application/vnd.collection+json' -H 'Accept: application/vnd.collection+json' -d '{"template":{"data":[{"name":"name","value":"recipe1"}]}}' 'http://localhost:8080/api/v1/'
```

Using [HTTPie](https://httpie.org/) REST API client:

```bash
http -a user:user1234 POST http://localhost:8080/api/v1/ template:='{"data":[{"name":"name","value":"recipe1"}]}' Content-Type:application/vnd.collection+json Accept:Application/vnd.collection+json
```

#### A simple PUT request to update an existing recipe:

Using curl:

```bash
curl -u user:user1234 -X PUT -H 'Content-Type: application/vnd.collection+json' -H 'Accept: application/vnd.collection+json' -d '{"template":{"data":[{"name":"name","value":"New name"}]}}' 'http://localhost:8080/api/v1/1/'
```

Using [HTTPie](https://httpie.org/) REST API client:

```bash
http -a user:user1234 PUT http://localhost:8080/api/v1/1/ template:='{"data":[{"name":"name","value":"New name"}]}' Content-Type:application/vnd.collection+json Accept:application/vnd.collection+json
```

#### A simple POST request to add a new ingredient to an existing recipe:

Using curl:

```bash
curl -u user:user1234 -XPOST -H 'Content-Type: application/vnd.collection+json' -H 'Accept: application/vnd.collection+json' -d '{"template":{"data":[{"name":"text","value":"Ingredient1"}]}}' 'http://localhost:8080/api/v1/1/ingredients/'
```

Using [HTTPie](https://httpie.org/) REST API client:

```bash
http -a user:user1234 POST http://localhost:8080/api/v1/1/ingredients/ template:='{"data":[{"name":"text","value":"Ingredient1"}]}' Content-Type:application/vnd.collection+json Accept:application/vnd.collection+json
```

### Destroy Recipe site

Stop and remove Recipe site services by running the destroy bash script from the repository source directory:

```bash
./docker-destroy.sh
```
