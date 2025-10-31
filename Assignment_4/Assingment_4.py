import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go


# ========== Stationary distribution function ==========
def compute_stationary_distribution(P_Y, P_L_given_Y, P_notL_given_notY, s):
    """
    P_Y                 ->  P(Y)   
    P_notY              ->  P(Ȳ)
    P_L_given_Y         ->  P(L|Y)
    P_L_given_notY      ->  P(L|Ȳ)
    P_notL_given_Y      ->  P(L̅|Y)
    P_notL_given_notY   ->  P(L̅|Ȳ)
    """

    P_notY = 1 - P_Y
    P_notL_given_Y = 1 - P_L_given_Y

    # Combined forgetting factor
    f = (P_L_given_Y * P_Y + P_notL_given_notY * P_notY)

    # Alpha
    a = 1

    # Pi values
    pi = np.zeros(8)
    pi[0] = a * P_Y**4  * 1                 * P_notL_given_Y**7     * 1         * 1
    pi[1] = a * P_Y**3  * 1                 * P_notL_given_Y**6     * s         * f
    pi[2] = a * P_Y**2  * 1                 * P_notL_given_Y**5     * s**2      * f**2
    pi[3] = a * P_Y     * 1                 * P_notL_given_Y**4     * s**3      * f**3
    pi[4] = a * 1       * 1                 * P_notL_given_Y**3     * s**4      * f**4
    pi[5] = a * 1       * P_L_given_Y       * P_notL_given_Y**2     * s**5      * f**4
    pi[6] = a * 1       * P_L_given_Y**2    * P_notL_given_Y**1     * s**6      * f**4
    pi[7] = a * 1       * P_L_given_Y**3    * 1                     * s**7      * f**4


    # Normalize so probabilities sum to 1
    total = np.sum(pi)
    pi = pi / total

    return pi


# ========== Dash app ==========
app = Dash(__name__)

app.layout = html.Div([
    html.H2("Stationary Distribution Visualizer", style={"textAlign": "center"}),
    dcc.Graph(id="pi-plot"),

    html.Div([
        # ===== s =====
        html.Div([
            html.Div("s", style={
                "textAlign": "center", "fontWeight": "bold", "marginBottom": "8px"
            }),
            html.Div(
                dcc.Slider(
                    id="s",
                    min=1.0, max=25.0, step=0.5, value=5.0,
                    marks={1.0001: "1", 5.0: "5", 10.0: "10", 15.0: "15",
                        20.0: "20", 24.999: "25"},
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode="drag",
                ),
                style={"marginLeft": "30px", "marginRight": "30px"}
            )
        ], style={"marginBottom": "40px"}),

        # ===== P_Y =====
        html.Div([
            html.Div("P(Y)", style={
                "textAlign": "center", "fontWeight": "bold", "marginBottom": "8px"
            }),
            html.Div(
                dcc.Slider(
                    id="P_Y",
                    min=0.0, max=1.0, step=0.01, value=0.5,
                    marks={0.0001: "0.0", 0.5: "0.5", 0.9999: "1.0"},
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode="drag",
                ),
                style={"marginLeft": "30px", "marginRight": "30px"}
            )
        ], style={"marginBottom": "40px"}),

        # ===== P_L_given_Y =====
        html.Div([
            html.Div("P(L|Y)", style={
                "textAlign": "center", "fontWeight": "bold", "marginBottom": "8px"
            }),
            html.Div(
                dcc.Slider(
                    id="P_L_given_Y",
                    min=0.0, max=1.0, step=0.01, value=0.5,
                    marks={0.0001: "0.0", 0.5: "0.5", 0.9999: "1.0"},
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode="drag",
                ),
                style={"marginLeft": "30px", "marginRight": "30px"}
            )
        ], style={"marginBottom": "40px"}),

        # ===== P_notL_given_notY =====
        html.Div([
            html.Div("P(nL|nY)", style={
                "textAlign": "center", "fontWeight": "bold", "marginBottom": "8px"
            }),
            html.Div(
                dcc.Slider(
                    id="P_notL_given_notY",
                    min=0.0, max=1.0, step=0.01, value=0.5,
                    marks={0.0001: "0.0", 0.5: "0.5", 0.9999: "1.0"},
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode="drag",
                ),
                style={"marginLeft": "30px", "marginRight": "30px"}
            )
        ], style={"marginBottom": "40px"}),

    ], style={"width": "80%", "margin": "auto"})

])



# ========== Callback for interactive updates ==========
@app.callback(
    Output("pi-plot", "figure"),
    Input("P_Y", "value"),
    Input("P_L_given_Y", "value"),
    Input("P_notL_given_notY", "value"),
    Input("s", "value"),
)
def update_plot(P_Y, P_L_given_Y, P_notL_given_notY, s):
    pi = compute_stationary_distribution(P_Y, P_L_given_Y, P_notL_given_notY, s)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=list(range(len(pi))),
        y=pi,
        marker=dict(color="cyan"),
        text=[f"{v:.4f}" for v in pi],
        textposition="outside",
    ))

    # --- Dashed vertical line in the middle ---
    fig.add_vline(
        x=3.5,  # between state 3 and 4
        line_dash="dash",
        line_color="black",
        line_width=2,
        opacity=0.7
    )

    # --- Forget value box ---
    fig.add_annotation(
        x=1.5, y=0.92,
        text="Forget value",
        showarrow=False,
        font=dict(size=14, color="Black", family="Arial Black"),
        bgcolor="rgba(255, 99, 71, 0.85)",  # tomato red, semi-transparent
        bordercolor="rgba(200, 50, 50, 1)",
        borderpad=8,
        borderwidth=2,
        xanchor="center",
        yanchor="bottom",
    )

    # --- Memorize value box ---
    fig.add_annotation(
        x=5.5, y=0.92,
        text="Memorize value",
        showarrow=False,
        font=dict(size=14, color="Black", family="Arial Black"),
        bgcolor="rgba(46, 204, 113, 0.85)",  # greenish
        bordercolor="rgba(40, 180, 90, 1)",
        borderpad=8,
        borderwidth=2,
        xanchor="center",
        yanchor="bottom",
    )

    # --- Layout ---
    fig.update_layout(
        xaxis_title="State index",
        yaxis_title="π value",
        yaxis=dict(range=[0, 1]),
        template="plotly_white"
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)

