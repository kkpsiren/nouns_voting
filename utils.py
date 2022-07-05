import streamlit as st

def get_pic(selected):
    st.image(f'https://noun.pics/{selected}.jpg')

def get_voting_proposal(selected):
    st.write(f'Read more about the Proposal from Nouns.wtf: [Proposal {selected}](https://nouns.wtf/vote/{selected})')