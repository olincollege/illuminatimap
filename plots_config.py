#This file serves as a helper function file for the scatterplot generation.
scatter_axis_config = dict(
    title_font=dict(
        #size=24,
        color='rgb(255,255,255)'),
    tickcolor='rgb(180,155,191)',
    tickfont=dict(
        color='rgb(255,255,255)',
        #size=20
        ),
    gridcolor='rgb(44,32,50)'
    )


scatter_update_layout = dict(
    title='Number of links to page vs. page views over the last 60 days',
    title_font=dict(
        color='rgb(255,255,255)',
        #size=32
        ), 
    paper_bgcolor='rgb(22,16,25)',
    plot_bgcolor='rgb(22,16,25)',
    #width=1920,
    #height=1080,
    )

kk_axis_config = dict(
    showbackground=False,
    showline=False,
    zeroline=False,
    showgrid=False,
    showticklabels=False,
    title=''
    )