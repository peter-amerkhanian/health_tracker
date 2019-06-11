import pygal
from pygal import Config
from pygal.style import Style
import psycopg2
import os
import pandas as pd
from health_tracker.models import Entry


class Graph:
    def __init__(self, name):
        self.name = name
        self.data = None
        self.line_style = Style(
            background='transparent',
            plot_background='transparent',
            foreground='#ffffff',
            foreground_strong='#ffffff',
            foreground_subtle='#ffffff',
            opacity='.6',
            opacity_hover='.9',
            transition='400ms ease-in',
            colors=('#E853A0', '#E8537A', '#E95355', '#E87653', '#E89B53'),
            tooltip_font_size=36,
            legend_font_size=24,
            font_family='googlefont:Work Sans')

    def get_data(self, sessions_name):
        # Postgres:
        # conn = psycopg2.connect(os.environ['DB_CONNECTION'])
        # cursor = conn.cursor()
        # cursor.execute('SELECT * FROM "entry" WHERE name=\'{}\''.format(self.name))
        # self.data = cursor.fetchall()
        # SQLite:
        self.data = Entry.query.filter(Entry.name == sessions_name).all()
        print(self.data)

    def pygal_line_plot(self):
        if not self.data:
            print('No data initialized')
            return None
        else:
            config = Config()
            config.show_legend = True
            config.include_x_axis = False
            config.stroke_style={'width': 5}
            config.dots_size = 10
            config.x_label_rotation = -20
            stress = [entry.__dict__['stress'] for entry in self.data]
            fatigue = [entry.__dict__['fatigue'] for entry in self.data]
            hours_sleep = [entry.__dict__['hours_of_sleep'] for entry in self.data]
            date = [entry.__dict__['date'].strftime("%m/%d, %H:%M") for entry in self.data]
            graph = pygal.Line(config, style=self.line_style, height=600, width=800)
            graph.x_labels = date
            graph.add('Hours of sleep', hours_sleep)
            graph.add('Stress level', stress)
            graph.add('Fatigue level', fatigue)
            return graph.render_data_uri()



