#!/bin/bash
#
# Sets environment variables from the file and runs migration with the specified command.

ENV_FILE='.env.dist'

if [[ -n $MIGRATION_ENV_FILE ]]; then
  ENV_FILE="$MIGRATION_ENV_FILE"
fi

echo "${ENV_FILE} is chosen as a file with environment variables."
source "$ENV_FILE"

yoyo "$1" -c yoyo.ini -d "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}" "${@:2}"
