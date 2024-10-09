# Backblaze Runner

This script is used to backup folders to Backblaze B2. It uses rclone to upload the folders to a remote path.

## Dependencies

- rclone
- python
- pdm
- yq

## Configuration

The configuration is done in a yaml file titled `config.yaml`.

The yaml file is structured as follows:

```yaml
bucket-name: backups

backups:
  - name: test
    localPath: ./test
    mountPath: /backups/test
```

The `localPath` is the path to the folder that you want to backup. The `mountPath` is the path where the folder will be mounted in the container. 

Note: The mountPath really can be anything you want, a good structure would be to mount everything under `/backups`, for organization.

The `name` is the name of the backup.

Must copy the `config.template.yaml` file to `config.yaml` and fill out the file.

`cp config.template.yaml config.yaml`

Must copy the `rclone.template.conf` file to `rclone.conf` and fill out the file.

`cp rclone.template.conf rclone.conf`

## Running the script

To run the script locally, you need to have the dependencies installed. You can install the dependencies using the `pdm` package manager.

```bash
pdm install
pdm run python src/backblaze-runner/__main__.py
```

## Running the script with Docker

Use the substiute.sh script to dynamically substitute the config.yaml file into the docker compose file.

```bash
./substitute.sh
docker compose up
```

This will mount the appropriate folders on the machine as volumes and run the script.

## Running the backup as a cron job

```bash
crontab -e
```

```bash
0 0 * * * docker compose -f /your/path/to/docker-compose.yml up
```










