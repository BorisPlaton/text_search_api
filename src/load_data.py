#!/usr/bin/env python
import asyncio
import csv
import re
from datetime import datetime

from config.settings import settings
from database.db import Database


async def script(csv_file_name: str):
    """
    Loads data to the database from the given *.csv file.
    """
    conn = await Database().connect()

    with open(settings.BASE_DIR.parent / csv_file_name, newline='') as csv_file:
        async with conn.transaction():
            next(csv_file)
            for row in csv.reader(csv_file):
                row[1] = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                row[2] = re.findall(r'\w{2}-\d+', row[2])
                await conn.execute(
                    """
                    INSERT INTO document(text, created_date, rubrics)
                    VALUES
                        ($1, $2, $3)
                    """, *row
                )


if __name__ == '__main__':
    asyncio.run(script('posts.csv'))
