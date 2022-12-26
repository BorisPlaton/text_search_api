#!/bin/bash
#
# Sets environment variables from the file and runs migration with the specified command.
# Checks that all necessarily environment variables exists.

ENV_FILE='.env.dist'

if [[ -n $MIGRATION_ENV_FILE ]]; then
  ENV_FILE="$MIGRATION_ENV_FILE"
fi

if [[ -f $MIGARTION_ENV_FILE ]]; then
  echo "${ENV_FILE} is chosen as a file with environment variables."
  source "$ENV_FILE"
fi

DB_ENV_VARS=("$POSTGRES_USER" "$POSTGRES_PASSWORD" "$POSTGRES_HOST" "$POSTGRES_PORT" "$POSTGRES_DB")
for ENV_VAR in "${DB_ENV_VARS[@]}"; do
  test -n "$ENV_VAR" || (echo "The environment variable hasn't been found" && exit 1)
done

yoyo "$1" -c yoyo.ini -d "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}" "${@:2}"
