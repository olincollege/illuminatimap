'''
Contains config values for plot generation.
'''
network_plot_config = dict(
    trace1=dict(
        mode='lines',
        line=dict(color='rgb(180,155,191)', width=1),
        hoverinfo='none'
    ),
    trace2=dict(
        mode='markers',
        name='billionaires',
        marker=dict(
            symbol='circle',
            size=6,
            # colorscale='Viridis',
            autocolorscale=True,
            line=dict(color='rgb(50,50,50)', width=0.5)
        ),
        hoverinfo='text'
    )
)

network_layout_config = dict(
    title="Links between 150 most viewed American billionaires' Wikipedia pages",
    title_font_color='rgb(255,255,255)',
    width=1000,
    height=800,
    showlegend=False,
    paper_bgcolor='rgb(22,16,25)',
    margin=dict(t=50),
    annotations=[
        dict(
            showarrow=False,
            text='Note that warmer colors indicate a larger number of page views',
            xref='paper',
            yref='paper',
            x=0,
            y=0.1,
            xanchor='left',
            yanchor='bottom',
            font=dict(
                size=14,
                color='rgb(255,255,255)'
            )
        )
    ],
    hovermode='closest'
)

scatter_plot_config = dict(
    mode='markers',
    marker_color='rgb(204,40,81)',
    marker_size=4,
    hovertemplate='<b>%{text}</b>' +
    '<br><b>Links</b>: %{x}' +
    '<br><b>Views</b>: %{y}<br><extra></extra>'
)

scatter_axis_config = dict(
    title_font=dict(
        # size=24,
        color='rgb(255,255,255)'),
    tickcolor='rgb(180,155,191)',
    tickfont=dict(
        color='rgb(255,255,255)',
        # size=20
    ),
    gridcolor='rgb(44,32,50)'
)


scatter_update_layout = dict(
    title='Number of links to page vs. page views over the last 60 days',
    title_font=dict(
        color='rgb(255,255,255)',
        # size=32
    ),
    paper_bgcolor='rgb(22,16,25)',
    plot_bgcolor='rgb(22,16,25)',
    # width=1920,
    # height=1080,
)

kk_axis_config = dict(
    showbackground=False,
    showline=False,
    zeroline=False,
    showgrid=False,
    showticklabels=False,
    title=''
)
