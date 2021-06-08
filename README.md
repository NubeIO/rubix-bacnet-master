# Rubix BACnet Master

## Running in development

- Use [`poetry`](https://github.com/python-poetry/poetry) to manage dependencies
- Simple script to install

    ```bash
    ./setup.sh
    ```

- Join `venv`

    ```bash
    poetry shell
    ```

- Build local binary

    ```bash
    poetry run pyinstaller run.py -n rubix-bacnet-master --clean --onefile --add-data pyproject.toml:. --add-data config:config
    ```

  The output is: `dist/rubix-bacnet-master`

## Docker build

### Build

```bash
./docker.sh
```

The output image is: `rubix-bacnet-master:dev`

### Run

```bash
docker volume create rubix-bacnet-data
docker run --rm -it -p 1718:1718 -v rubix-bacnet-data:/data --name rubix-bacnet rubix-bacnet:dev
```

## Deploy on Production

- Download release artifact
- Review help and start

```bash
$ rubix-bacnet-master -h
Usage: rubix-bacnet-master [OPTIONS]

Options:
  -p, --port INTEGER       Port  [default: 1718]
  -g, --global-dir PATH    Global dir
  -d, --data-dir PATH      Application data dir
  -c, --config-dir PATH    Application config dir
  -i, --identifier TEXT    Identifier  [default: bacnet]
  --prod                   Production mode
  -s, --setting-file TEXT  Rubix BACnet: setting json file
  -l, --logging-conf TEXT  Rubix BACnet: logging config file
  --workers INTEGER        Gunicorn: The number of worker processes for handling requests.
  --gunicorn-config TEXT   Gunicorn: config file(gunicorn.conf.py)
  -h, --help               Show this message and exit.
```
