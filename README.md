# Noteman #

Django application to add links between files and allow tagging them as well to
make organizing files easier.

## Installation (development version) ##

Requires:

  * Git
  * Docker
  * docker-compose

### Getting the source code ###

#### Over SSH (preferred) ####

```
git clone git@github.com:cbb4bbc5/thesis-app.git
```

#### Over HTTPS ####

```
git clone https://github.com/cbb4bbc5/thesis-app.git
```

### Building and running ###

```
cd thesis-app
docker compose build
docker compose up
```

Now going to <localhost:35329> should reveal the Web UI.

To stop the application run:

```
docker compose down
```
