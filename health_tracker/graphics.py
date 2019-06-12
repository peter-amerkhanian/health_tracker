from health_tracker.models import Entry
import pygal
from pygal import Config
from pygal.style import Style
import psycopg2
import os

from bokeh.plotting import figure
from bokeh.embed import file_html
from bokeh.resources import CDN


class Graph:
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
        self.type= None

    def get_data_sqlite(self, sessions_name):
        self.data = Entry.query.filter(Entry.name == sessions_name).all()
        print(self.data)

    def get_data_postgres(self, sessions_name):
        conn = psycopg2.connect(os.environ['DB_CONNECTION'])
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "entry" WHERE name=\'{}\''.format(self.name))
        self.data = cursor.fetchall()
        print(self.data)

    def pygal_line_plot(self):
        if not self.data:
            print('No data initialized')
            return None
        else:
            # Pygal config
            config = Config()
            config.show_legend = True
            config.include_x_axis = False
            config.stroke_style={'width': 7}
            config.dots_size = 8
            config.x_label_rotation = -45
            # init data
            stress = [entry.__dict__['stress'] for entry in self.data]
            fatigue = [entry.__dict__['fatigue'] for entry in self.data]
            comfort = [entry.__dict__['comfort'] for entry in self.data]
            date = [entry.__dict__['date'].strftime("%m/%d") for entry in self.data]
            # build graph
            graph = pygal.Bar(config,
                               margin_top=10,
                               range=(1, 5),
                               style=self.pygal_line_style,
                               legend_at_bottom=True,
                               legend_at_bottom_columns=3,
                               legend_box_size=20,
                               truncate_legend=-1)
            graph.x_labels = date
            graph.add('Discomfort lvl', comfort)
            graph.add('Stress lvl', stress)
            graph.add('Fatigue lvl', fatigue)

            graph_2 = pygal.Bar(config,
                              margin_top=10,
                              range=(1, 5),
                              style=self.pygal_line_style,
                              legend_at_bottom=True,
                              legend_at_bottom_columns=2,
                              legend_box_size=20,
                              truncate_legend=-1)
            graph_2.x_labels = date
            rest = [entry.__dict__['rest'] for entry in self.data]
            emotion = [entry.__dict__['emotion'] for entry in self.data]
            graph_2.add('Emotion lvl', emotion)
            graph_2.add('Rest lvl', rest)

            self.type = 'pygal'
            return graph.render_data_uri(), graph_2.render_data_uri()

    def bokeh_line_plot(self):
        if not self.data:
            print('No data initialized')
            return None
        else:
            # init data
            stress = [entry.__dict__['stress'] for entry in self.data]
            fatigue = [entry.__dict__['fatigue'] for entry in self.data]
            hours_sleep = [entry.__dict__['hours_of_sleep'] for entry in self.data]
            date = [entry.__dict__['date'] for entry in self.data]
            # build graph
            p = figure( x_axis_type="datetime", plot_height=600, plot_width=800)
            p.xgrid.grid_line_color = None
            p.ygrid.grid_line_alpha = 0.5
            p.xaxis.axis_label = 'Time'
            p.yaxis.axis_label = 'Sleep'
            p.line(date, hours_sleep)
            self.type = 'bokeh'
            return file_html(p, CDN, "my plot")


