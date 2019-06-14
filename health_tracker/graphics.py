from health_tracker.models import Entry
import psycopg2
import os
from flask import Markup
import pandas as pd

import pygal
from pygal import Config
from pygal.style import Style


class UserData:
    def __init__(self, name):
        self.name = name
        self.data = None
        self.pygal_line_style = Style(background='transparent',
                                      plot_background='transparent',
                                      tooltip_background='#3498db',
                                      foreground='#ffffff',
                                      foreground_strong='#ffffff',
                                      foreground_subtle='#ffffff',
                                      opacity='.6',
                                      opacity_hover='.9',
                                      stroke_width=5,
                                      transition='400ms ease-in',
                                      colors=('#d35400', '#e74c3c', '#ecf0f1', '#f1c40f'),
                                      tooltip_font_size=30,
                                      label_font_size=24,
                                      major_label_font_size=24,
                                      legend_font_size=24,
                                      font_family='googlefont:Work Sans')
        self.no_data_message = None

    def get_data_sqlite(self) -> None:
        """
            init user's data
        """
        self.data = Entry.query.filter(Entry.name == self.name).all()

    def get_data_postgres(self) -> None:
        """ init user's data
        """
        conn = psycopg2.connect(os.environ['DB_CONNECTION'])
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "entry" WHERE name=\'{}\''.format(self.name))
        self.data = cursor.fetchall()

    def to_csv(self, path: str) -> None:
        """ reorders table and saves user's data as a csv
        :param path: file location to be saved at
        """
        if self.data:
            df = pd.DataFrame([entry.__dict__ for entry in self.data])
            df = df.drop("_sa_instance_state", axis=1)
            columns = df.columns.to_list()
            order = [7, 9, 2, 0, 1, 3, 4, 5, 6, 10, 11, 8]
            columns = [columns[ind] for ind in order]
            df = df[columns]
            df.to_csv(path)
        else:
            print('No data initialized')

    def to_excel(self, path: str) -> None:
        """ reorders table and saves user's data as a csv
        :param path: file location to be saved at
        """
        if self.data:
            df = pd.DataFrame([entry.__dict__ for entry in self.data])
            df = df.drop("_sa_instance_state", axis=1)
            columns = df.columns.to_list()
            order = [7, 9, 2, 0, 1, 3, 4, 5, 6, 10, 11, 8]
            columns = [columns[ind] for ind in order]
            df = df[columns]
            df.to_excel(path)
        else:
            print('No data initialized')

    def pygal_line_plot(self, vars: list) -> None:
        """ build and save line plot in pygal
        :param vars: list of the y vars in the graph
        """
        if not self.data:
            self.no_data_message = Markup("""<p>No data available</p>""")
        else:
            # Pygal config
            config = Config()
            config.show_legend = True
            config.include_x_axis = False
            config.stroke_style = {'width': 7}
            config.dots_size = 8
            config.x_label_rotation = -45
            # init graph
            graph = pygal.Bar(config,
                               margin_top=10,
                               range=(1, 5),
                               style=self.pygal_line_style,
                               legend_at_bottom=True,
                               legend_box_size=20,
                               truncate_legend=-1)
            # init data
            date = [entry.__dict__['date'].strftime("%m/%d") for entry in self.data]
            graph.x_labels = date
            for var in vars:
                data = [entry.__dict__[var] for entry in self.data]
                graph.add('{} lvl'.format(var), data)
            path = os.path.join(os.getcwd(),'health_tracker', 'static') if \
                os.getcwd().endswith('health_tracker') else \
                os.path.join(os.getcwd(),'health_tracker', 'health_tracker', 'static')
            graph.render_to_file(os.path.join(path,
                                              '{}_line_graph.svg'.format(self.name)))
