import pygal
import psycopg2
import os
import pandas as pd


class Graph:
    def __init__(self, name):
        self.name = name
        self.data = None

    def get_data(self):
        conn = psycopg2.connect(os.environ['DB_CONNECTION'])
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "entry" WHERE name=\'{}\''.format(self.name))
        self.data = cursor.fetchall()
        print(self.data)

    def pygal_line_plot(name):
        pass

