import streamlit as st
#from scripts.utils import read_flipside
from landing import landing_page
from beautify import flipside_logo, discord_logo
import os

from data_loading import load_queries
from queries import *

# from dotenv import load_dotenv
# load_dotenv()
st.set_page_config(page_title="Flipside Crypto: Nouns Voting", layout="wide")

votes = load_queries(VOTE_QUERY)
traits = load_queries(TRAIT_QUERY)

landing_page(votes, traits)

flipside_logo(text="🍄 ShroomDK 🍄")
discord_logo(os.getenv('DISCORD_USERNAME'))
flipside_logo()





