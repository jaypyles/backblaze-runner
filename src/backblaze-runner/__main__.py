import os
import subprocess
from typing import Any

import yaml


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
        "10",  # Number of parallel uploads
        "--progress",  # Show progress in terminal
    ]

    # Execute the rclone command
    try:
        print(f"Uploading {folder_path} to {remote_name}:{remote_path} using rclone")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(result.stdout)  # Print rclone output to console
    except subprocess.CalledProcessError as e:
        print(f"Error during rclone upload: {e.stderr}")


if __name__ == "__main__":
    config = read_yaml()
    backups = config.get("backups", [])

    for backup in backups:
        local_path = backup.get("localPath")
        mount_path = backup.get("mountPath")
        name = backup.get("name")
        bucket_name = config.get("bucket-name")
        upload_folder_with_rclone(local_path, "b2", f"{bucket_name}/{name}")
