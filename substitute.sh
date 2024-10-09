#!/bin/bash

# Function to generate volume entries
generate_volumes() {
    volumes=""
    while IFS= read -r line; do
        local_path=$(echo "$line" | awk '{print $2}')
        mount_path=$(echo "$line" | awk '{print $4}')
        volumes+="      - $local_path:$mount_path\n"
    done < <(yq e '.backups[] | "localPath: \(.localPath) mountPath: \(.mountPath)"' config.yaml)
    echo -e "$volumes" | sed '$ s/\\n$//'
}

# Create docker-compose.yaml file
cat > docker-compose.yaml << EOF
version: '3'

services:
  backblaze-runner:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
$(generate_volumes)
EOF

echo "docker-compose.yaml has been generated."