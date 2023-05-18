import sqlite3
import csv
from datetime import datetime


def create_additional_fields_for_user(row):
    # set default values for password, is_staff, is_superuser, is_active, and date_joined
    row['password'] = '12345'
    row['is_active'] = True
    row['date_joined'] = datetime.now()

    # set is_staff and is_superuser based on role
    if row['role'] == 'admin':
        row['is_staff'] = True
        row['is_superuser'] = True
    elif row['role'] == 'moderator':
        row['is_staff'] = True
        row['is_superuser'] = False
    else:
        row['is_staff'] = False
        row['is_superuser'] = False


def create_columns(filename):
    # read column names from the first row of the CSV file
    with open(f'data/{filename}', 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        columns = list(reader.fieldnames)

        # add password, is_staff, is_superuser, is_active, and date_joined fields to the columns list
        if filename == 'users.csv':
            columns.extend(['password', 'is_staff', 'is_superuser', 'is_active', 'date_joined'])
        return columns


def insert_data(cursor, filename, table_name, columns):
    # insert data from csv
    with open(f'data/{filename}', 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if filename == 'users.csv':
                create_additional_fields_for_user(row)

            # extract values for each column
            values = [row[column] for column in columns]
            print(values)


            # execute INSERT statement
            cursor.execute(f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({", ".join("?" * len(columns))})', values)

            # insert category and genre data separately


def main():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    for filename, table in [
        ('users.csv', 'users_mytitlesuser'),
        ('titles.csv', 'titles_title'),
        ('category.csv', 'titles_category'),
        ('genre.csv', 'titles_genre'),
        ('review.csv', 'titles_review'),
        ('comments.csv', 'titles_comment'),
        ('genre_title.csv', 'titles_title_genre'),
    ]:
        insert_data(cursor, filename, table, create_columns(filename))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
