#!/bin/bash
#
# Entrypoint script for the production-ready application. Performs migrations,
# creating Elasticsearch indices, populating database and Elasticsearch
# with data and starting the application.

./scripts/init_env.sh
cd src && python main.py
