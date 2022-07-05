import streamlit as st
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.express as px
from plots import *
from utils import get_voting_proposal
from queries import TRAIT_QUERY, VOTE_QUERY

cm = sns.light_palette("green", as_cmap=True)
def mapper(vote):
    return {0:'Against', 1:'For', 2:'Abstain'}[vote]

def landing_page(votes, traits):
    
    votes['BLOCK_TIMESTAMP'] = pd.to_datetime(votes['BLOCK_TIMESTAMP']) 
    votes['PROPOSALID'] = votes['PROPOSALID'].astype('int')
    votes['VOTES'] = votes['VOTES'].astype('int')
    try:
        votes['SUPPORT'] = votes['SUPPORT'].astype('int')
        votes['SUPPORT'] = votes['SUPPORT'].map(mapper)
    except:
        pass
    traits['MINT_TIME'] = pd.to_datetime(traits['MINT_TIME'])
    traits = traits.sort_values('MINT_TIME')

    df = votes.groupby(['PROPOSALID','SUPPORT'])['VOTES'].sum().reset_index().sort_values('PROPOSALID')
    turnout = votes.groupby('PROPOSALID')['VOTES'].sum()
    proposal_start = votes.groupby('PROPOSALID')['BLOCK_TIMESTAMP'].max()
    d = pd.Series({i: traits[traits['MINT_TIME']<j]['TOKENID'].count() for i,j in proposal_start.iteritems()},name='MINTED')
    data = turnout.to_frame().join(d)
    data['PROPORTION'] =  data['VOTES'] / data['MINTED']
    
    
    
    l1,l2 = st.columns((800,300))
    with l2:
        st.image('nouns.png',width=300)
    with l1:
        st.markdown("""
# Flipside Crypto <3 Nouns DAO
""")
        st.markdown(f"""
## Nouns Governance Participation
      
### Intro

The Nouns are an Ethereum NFT project that brings a unique minting mechanism to the NFT space. One Noun is auctioned trustlessly every 24 hours, forever. 100% of the proceeds from these auctions are sent to the DAO treasury, 
which as of the time of this writing sits at 27,416 ETH. Getting a Noun won’t be cheap, as recent auctions have closed at over 100 ETH. As a Noun token holder you are entitled to one vote in the DAO, which uses a fork of Compound Governance and controls the treasury. There are no rules about trait rarity, and the artwork is generative and stored on-chain. Once an auction ends, someone must settle the current auction to initiate a new auction, which will restart the minting / auction cycle.

For more details, see https://nouns.wtf/ & and its satellite https://lilnouns.wtf/.
This dashboard shows the on-chain voting for NounsDAO. Which proposals have had the most engagement, relative to the number of tokens minted?

""")
    
    l,r = st.columns(2)
    with l:
        st.markdown('#### Proportion of Votes per Minted Nouns')
        fig = get_votes(data,y='PROPORTION',color='VOTES')
        st.plotly_chart(fig, use_container_width=True)
    with r:
        st.markdown('#### Number of Votes')
        fig = get_votes(data,color='PROPORTION',y='VOTES')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('##### Total Nouns Minted')
    fig = get_minted(traits)
    st.plotly_chart(fig, use_container_width=True)
    
    l,r = st.columns(2)
    with l:
        st.markdown('##### Voter Choice per Minted Nouns')
        fig = vote_vs_minted(df,data, col='MINTED')
        st.plotly_chart(fig, use_container_width=True)
    with r:
        st.markdown('##### Voter Choice per Total Votes')
        fig = vote_vs_minted(df,data, col='VOTES')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('Filter Proposals based on Engagement')
    val = st.number_input('Select Proportion', min_value=0.0, max_value=1.0, value=0.4, step=0.05)
    fig = filter_votes_based_on_proportion(data, val=val)
    st.plotly_chart(fig, use_container_width=True)

    ## inspect single votes
    st.markdown('## Investigate Individual Proposals')
    proposal_max = votes['PROPOSALID'].max()
    proposal = st.number_input('Select Proposal', min_value=1, max_value=proposal_max, value=proposal_max, step=1)
    
    selected_proposal = votes.query('PROPOSALID==@proposal')
    
    s_votes = selected_proposal.groupby('SUPPORT')['VOTES'].sum()
    s_voter = selected_proposal.groupby('SUPPORT')['VOTER'].count()
    if 'For' not in s_votes.index:
        s_votes.loc['For'] = 0
        s_voter.loc['For'] = 0

    col1, col2, col3 = st.columns(3)
    get_voting_proposal(proposal)
    col1.metric("Total Votes", f"{s_votes.sum()} Votes", f"{s_voter.sum()} Addresses")
    col2.metric("Supporting", f"{s_votes.loc['For'] / s_votes.sum() * 100:.0f} % of Votes", f"{s_voter.loc['For'] / s_voter.sum() * 100:.0f} % of Addresses")
    col3.metric("Proportion of All Nouns", f"{s_votes.sum()} / {data.loc[proposal,'MINTED']}", f"{s_votes.sum() / data.loc[proposal,'MINTED'] * 100:.0f} % Turnout ")
    
    st.markdown("### Reasons")
    for i, ser in selected_proposal.iterrows():
        if len(ser["REASON"]) > 0:
            st.markdown(f'*{ser["VOTER"]}* __Voting {ser["SUPPORT"]}__: "{ser["REASON"]}"')
    
    st.markdown(f"""
## Summary

- Proposal ID 2 [link](https://nouns.wtf/vote/2) had most turnout based on the proportion of Minted Nouns (48 %) or 12 / 25  
- 5 Proposals have received more than 40 % turnout with more than 100 casted votes.
  - Proposal ID 81 [link](https://nouns.wtf/vote/81)
  - Proposal ID 82 [link](https://nouns.wtf/vote/82)
  - Proposal ID 83 [link](https://nouns.wtf/vote/83)
  - Proposal ID 87 [link](https://nouns.wtf/vote/87)
  - Proposal ID 95 [link](https://nouns.wtf/vote/95)

- Proposals with Most Abstaining Engagement
  - Proposal ID 72 [link](https://nouns.wtf/vote/72)
  - Proposal ID 86 [link](https://nouns.wtf/vote/86)

- Proposals with Most Negative Engagement
  - Proposal ID 59 [link](https://nouns.wtf/vote/59)
  - Proposal ID 89 [link](https://nouns.wtf/vote/89)
  
## Methods
For this dashboard used the ShroomDK for querying the data from Flipside.  
Plotly and Pandas for the data viz and shamelessly took and modified the intro written by Flipside somewhere earlier (probably the layer3 bounty).
                """)
    with st.expander("Show Queries"):
        st.markdown('#### Minting Query')
        st.markdown(f"""```{TRAIT_QUERY}```""")
        st.markdown('#### Voting Query')
        st.markdown(f"""```{VOTE_QUERY}```""")
    