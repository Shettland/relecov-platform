"""
Needle plot graph mutation by sample
"""

# Generic imports
import dash_bio as dashbio
from dash import dcc, html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash

# Local imports
import core.utils.variants


# FIXME: This file is not accessed.
def create_needle_plot_graph_mutation_by_sample(sample_name, mdata):
    sample_list = [2018185, 210067]
    app = DjangoDash("needlePlotBySample")

    app.layout = html.Div(
        children=[
            html.Div(
                children=[
                    # html.Div("Hello"),
                    html.Div(
                        children=[
                            "Show or hide range slider",
                            dcc.Dropdown(
                                id="needleplot-rangeslider",
                                options=[
                                    {"label": "Show", "value": 1},
                                    {"label": "Hide", "value": 0},
                                ],
                                clearable=False,
                                multi=False,
                                value=1,
                                style={"width": "150px", "margin-right": "30px"},
                            ),
                        ]
                    ),
                    html.Div(
                        children=[
                            "Select a Sample",
                            dcc.Dropdown(
                                id="needleplot-select-sample",
                                options=[{"label": i, "value": i} for i in sample_list],
                                clearable=False,
                                multi=False,
                                value=sample_list[0],
                                style={"width": "150px"},
                            ),
                        ]
                    ),
                ],
                style={
                    "display": "flex",
                    "justify-content": "start",
                    "align-items": "flex-start",
                },
            ),
            html.Div(
                children=dashbio.NeedlePlot(
                    width="auto",
                    # margin={"t": 100, "l": 20, "r": 400, "b": 40},
                    id="dashbio-needleplot",
                    mutationData=mdata,
                    rangeSlider=True,
                    xlabel="Genome Position",
                    ylabel="Allele Frequency ",
                    domainStyle={
                        "displayMinorDomains": False,
                        # "textangle": 90,
                    },
                ),
            ),
        ]
    )

    @app.callback(
        Output("dashbio-needleplot", "mutationData"),
        Input("needleplot-select-sample", "value"),
    )
    def update_sample(selected_sample: int):
        mdata = core.utils.variants.create_dataframe(
            sample_name=selected_sample, organism_code="NC_045512"
        )
        mutationData = mdata
        return mutationData

    @app.callback(
        Output("dashbio-needleplot", "rangeSlider"),
        Input("needleplot-rangeslider", "value"),
    )
    def update_range_slider(range_slider_value):
        return True if range_slider_value else False
