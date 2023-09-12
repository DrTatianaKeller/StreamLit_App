import streamlit as st
import pandas as pd
import matplotlib as plt
import plotly.express as ex
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

#put into cash
@st.cache_data
def load_data(path):
    df=pd.read_csv(path)
    return df
mpg_df_raw=load_data(path='./data/mpg.csv')
mpg_df=deepcopy(mpg_df_raw)

mpg_df=pd.read_csv('./data/mpg.csv')
st.title('Introduction to Streamlit')

