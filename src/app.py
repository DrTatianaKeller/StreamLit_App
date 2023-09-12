import streamlit as st
import pandas as pd
import matplotlib as plt
import plotly.express as ex
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

mpg_df=pd.read_csv('./data/mpg.csv')
st.title('Introduction to Streamlit')

