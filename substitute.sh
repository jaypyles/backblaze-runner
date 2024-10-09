#!/bin/bash

set -x  # Enable debug mode

# Function to generate volume entries
generate_volumes() {
    echo "Entering generate_volumes function" >&2
    sed -n '/^  - name:/,/mountPath:/ {
        /localPath:/ {
            s/.*localPath: *//
            s/ *#.*//
            h
        }
        /mountPath:/ {
            s/.*mountPath: *//
            s/ *#.*//
            G
            s/\(.*\)\n\(.*\)/      - \2:\1/
            p
        }
    }' config.yaml
    echo "Exiting generate_volumes function" >&2
}

echo "Starting script" >&2

# Generate volumes
echo "Calling generate_volumes" >&2
volumes=$(generate_volumes)
echo "generate_volumes completed" >&2

echo "Contents of volumes variable:" >&2
echo "$volumes" >&2

# Create docker-compose.yaml file
echo "Creating docker-compose.yaml" >&2
cat > docker-compose.yaml << EOF
version: '3'

services:
  backblaze-runner:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ./config.yaml:/app/config.yaml
      - ./rclone.conf:/app/rclone.conf
$volumes
EOF

echo "docker-compose.yaml has been generated." >&2