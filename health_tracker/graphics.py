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
        self.pandas_df = None

    def get_data_sqlite(self) -> None:
        """
            init user's data from a sqlite db
        """
        # Init the data in the raw form
        self.data = Entry.query.filter(Entry.name == self.name).all()
        # Init the data as a pandas df
        df = pd.DataFrame([entry.__dict__ for entry in self.data])
        df = df.drop("_sa_instance_state", axis=1)
        df['date'] = pd.to_datetime(df["date"].dt.strftime('%Y-%m-%d'))
        df = df.sort_values('date', ascending=False)
        columns = df.columns.to_list()
        print(columns)
        date_and_bools = [3, 1, 7, 10]
        varying_answers = [5, 8, 11, 13]
        one_to_fives = [0, 2, 4, 6, 14, 15]
        order = date_and_bools + varying_answers + one_to_fives
        columns = [columns[ind] for ind in order]
        print(columns)
        df = df[columns]
        self.pandas_df = df

    def get_data_postgres(self) -> None:
        """ init user's data from the connected postgres db
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
            self.pandas_df.to_csv(path)
        else:
            print('No data initialized')

    def to_excel(self, path: str) -> None:
        """ reorders table and saves user's data as a csv
        :param path: file location to be saved at
        """
        if self.data:
            self.pandas_df.to_excel(path)
        else:
            print('No data initialized')

    def build_table(self) -> str:
        """ build html table of the pandas df
        """
        if self.data:
            df = self.pandas_df
            print("df to html")
            html_string = df.to_html(index=False, justify='center')
            html_string = html_string.replace('<table border="1" class="dataframe">', '')
            html_string = html_string.replace('</table>', '')
            return Markup(html_string)
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
            revered_df = self.pandas_df.sort_values('date', ascending=True)
            dates = [x.strftime('%Y-%m-%d') for x in list(revered_df['date'])]
            graph.x_labels = dates
            print(graph.x_labels)
            for var in vars:
                print(var)
                data = list(revered_df[var])
                graph.add('{} lvl'.format(var), data)
            path = os.path.join(os.getcwd(),'health_tracker', 'static') if \
                os.getcwd().endswith('health_tracker') else \
                os.path.join(os.getcwd(),'health_tracker', 'health_tracker', 'static')
            graph.render_to_file(os.path.join(path,
                                              '{}_line_graph.svg'.format(self.name)))
