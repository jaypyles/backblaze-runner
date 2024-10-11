import os
import subprocess
from typing import Any

import yaml
import logging


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
LOG = logging.getLogger(__name__)


def read_yaml() -> dict[str, Any]:
    with open("config.yaml", "r", encoding="utf-8") as f:
        config: dict[str, Any] = yaml.safe_load(f)
        return config


def upload_folder_with_rclone(folder_path: str, remote_name: str, remote_path: str):
    # Construct rclone command
    command = [
        "rclone",
        "--config",
        "./rclone.conf",
        "copy",
        folder_path,
        f"{remote_name}:{remote_path}",
        "--transfers",
        "4",  # Number of parallel uploads
        "--fast-list",  # Add this option to reduce Class C transactions
        "--tpslimit",
        "10",  # Limit API calls per second
        "--progress",  # Show progress in terminal
    ]

    # Execute the rclone command
    try:
        LOG.info(f"Uploading {folder_path} to {remote_name}:{remote_path} using rclone")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)  # Print rclone output to console
    except subprocess.CalledProcessError as e:
        print(f"Error during rclone upload: {e.stderr}")


if __name__ == "__main__":
    config = read_yaml()
    backups = config.get("backups", [])

    for backup in backups:
        mount_path = backup.get("mountPath")
        name = backup.get("name")
        bucket_name = config.get("bucket-name")
        upload_folder_with_rclone(mount_path, "b2", f"{bucket_name}/{name}")
