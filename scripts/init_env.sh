#!/bin/bash
#
# Performs all necessarily operations to initialize services that are
# started by start_env.sh script.

./scripts/migration.sh apply

cd src || exit

INIT_SCRIPTS=(scripts.docs_to_db scripts.create_indices scripts.texts_to_index)

for script in "${INIT_SCRIPTS[@]}"; do
  python3 -m "$script" || exit 1
done
