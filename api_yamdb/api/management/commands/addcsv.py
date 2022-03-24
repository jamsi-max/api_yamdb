from django.core.management.base import BaseCommand, CommandError
import csv, sqlite3
import os
import re

from api_yamdb.settings import BASE_DIR


def ensure_connection(func):
    def inner(*args, **kwargs):
        with sqlite3.connect('db.sqlite3') as conn:
            result = func(*args, conn=conn, **kwargs)
        return result
    return inner


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def search(self, file_name, endswith=False):
        data_list = []
        pattern = f'^{file_name}$'

        if endswith:
            pattern = f'{file_name}$'

        for root, dirs, files in os.walk(f'{BASE_DIR}'):
            for file in files:
                if re.findall(pattern, file):
                    data_list.append(os.path.join(root, file))
        return data_list

    def add_arguments(self, parser):
        parser.add_argument('bd_name', type=str)

    @ensure_connection
    def handle(self, conn, *args, **options):
        file_list_csv = self.search('.csv', endswith=True)
        db = self.search(options.get('bd_name'))
        table_list = ['reviews_category',
                      'reviews_comments',
                      'reviews_genre',
                      'reviews_genretitle',
                      'reviews_review',
                      'reviews_title',
                      'users']

        if not db:
            raise CommandError('Файл базы данных не найден')

        if not file_list_csv:
            raise CommandError('Файл .csv не найден')

        for table_name in file_list_csv:
            with open(table_name, encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader)
                print("*"*80)
                print(table_name)

                # cursor = conn.cursor()
                # cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and sql LIKE '%id%username%email%role%bio%first_name%last_name%';")
                # print(cursor.fetchall())


            # headers = next(reader)
            # table_name = str(table_name.split('\\')[-1].split('.')[0]).replace('_', '')
        # print(table_name)
        # table_name = 'category'

        # cursor = conn.cursor()
        #     column_name
        #     cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' and name='users_yamdbuser';")
            # if table_name.lower() == 'users':
            #     cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' and name='users_yamdbuser';")
            # else:
            #     cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' and name like '%{table_name}';")
            # print("*"*80)
            # print(table_name)
            # print(cursor.fetchall())

        # with open(file_list_csv[-1], newline='', encoding='utf-8') as f:
        #     csv_dict_reader = csv.DictReader(f)
        #     for row in csv_dict_reader:
        #         row = dict(row)
                # row.update(int(v) for v in row.values() if v.isdigit())
                # print(row)
            # reader = csv.reader(f)
            # headers = next(reader)
            # stmt = f'INSERT INTO {table_name} VALUES({",".join("?"*len(headers))})'
            # print(stmt)
            # for velue in reader:
            #     cursor.executemany(stmt, velue)
            # print('add BD succefull')

            # reader = csv.reader(f)
            # header = next(reader)
            
            # for row in reader:
            #     print(row)

        # self.stdout.write(self.style.SUCCESS('Successfully'))

        # with open('data.csv','r') as fin: # `with` statement available in 2.5+
        #     # csv.DictReader uses first line in file for column headings by default
        #     dr = csv.DictReader(fin) # comma is default delimiter
        #     to_db = [(i['col1'], i['col2']) for i in dr]

        #     cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
        #     con.commit()
        #     con.close()
        # print(options.get('files_name'))
        
        
        # for root, dirs, files in os.walk("/mydir"):
        #     for file in files:
        #         if file.endswith(".txt"):
        #             print(os.path.join(root, file))

        # if file_list:
        #     for file in file_list:
        #         print(file)
        #         self.stdout.write(self.style.SUCCESS(f'Successfully closed poll {file}'))