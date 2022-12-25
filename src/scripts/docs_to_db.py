#!/usr/bin/env python
import asyncio
import csv
import re
from datetime import datetime

from config.settings import settings
from database.db import Database
from database.services.inserts import insert_new_document


async def load_documents_to_db():
    """
    Loads documents to the database from the given *.csv file.
    """
    conn = await Database().connect()
    with open(settings.BASE_DIR.parent / 'posts.csv', newline='') as csv_file:
        async with conn.transaction():
            next(csv_file)
            for quantity, row in enumerate(csv.reader(csv_file)):
                await insert_new_document(
                    conn, re.findall(r'\w{2}-\d+', row[2]), row[0],
                    datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                )
            else:
                print(f"{quantity + 1} documents have been inserted to the database.")


if __name__ == '__main__':
    asyncio.run(load_documents_to_db())
