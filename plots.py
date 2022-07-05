import plotly.express as px

def get_votes(data,y='PROPORTION',color='VOTES'):
    fig = px.bar(data_frame=data.reset_index(),
        x='PROPOSALID',
        y=y,
        color=color)
    return fig

def get_minted(traits):
    traits.index = traits['MINT_TIME']
    d = traits.resample('d')['TOKENID'].count().cumsum().to_frame('NUMBER_OF_NOUNS_MINTED').reset_index()
    fig = px.bar(data_frame=d,
        x='MINT_TIME',
        y='NUMBER_OF_NOUNS_MINTED')
    return fig

def vote_vs_minted(df,data, col='MINTED'):
    # VOTES
    df['PROPOSALID'] = df['PROPOSALID'].astype('int')
    df['PROPORTION'] = df['VOTES'] / df['PROPOSALID'].map(data[col])
    df['PROPOSALID'] = df['PROPOSALID'].astype('str')

    fig = px.line_polar(df, r="PROPORTION", theta="PROPOSALID", color="SUPPORT",
                        width = 400,height=600
                 )
    # fig.update_layout(polar_angularaxis_showticklabels=True)
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.1,
        xanchor="center",
        x=0.5
    ))
    return fig

def filter_votes_based_on_proportion(data, val=0.4):
    fig = px.bar(data_frame=data.reset_index().query('PROPORTION > @val'),
        x='PROPOSALID',
        y='PROPORTION',
        color='VOTES')
    return fig

