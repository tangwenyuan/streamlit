import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title='Net-Load Forecasting', page_icon=":sunny:", layout='wide')

'''
### Net-Load Forecasting

**Project Title**: Day-Ahead Probabilistic Forecasting of Net-Load and Demand Response Potentials with High Penetration of Behind-the-Meter Solar-plus-Storage

**Agency**: U.S. Department of Energy

**Award Number**: DE-EE0009357

**Project Period**: 06/01/2021 to 05/31/2024

**Lead Organization**: NC State University

**Team Member Organizations**: Purdue University, North Carolina Electric Membership Corporation (NCEMC), Dominion Energy

If you have any questions or comments, please contact the Principal Investigator [Wenyuan Tang](https://tangwenyuan.github.io).
'''

''

orgs = ['doe', 'ncsu', 'purdue', 'ncemc', 'dominion']
cols = st.columns([278, 145, 108, 280, 198])
for i in range(5):
    cols[i].markdown('<img src="data:image/png;base64,{}" height="70">'.format(base64.b64encode(Path('figs/' + orgs[i] + '.png').read_bytes()).decode()), unsafe_allow_html=True)
