# import yfinance as yf
import streamlit as st
# import matplotlib.pyplot as plt
import pandas as pd

import numpy as np
import plotly.figure_factory as ff

# from datetime import datetime
# import streamlit as st
# from streamlit_jupyter import StreamlitPatcher, tqdm

# st.sidebar.markdown("### Accrual Calculations by")
# st.sidebar.markdown("Welcome to my first awesome app. This app is built using Streamlit and uses data source from redfin housing market data. I hope you enjoy!")

#Add title and subtitle to the main interface of the app
st.title("Accrual Calculations")
st.markdown("This app illustrates different ways of calculating accruals for North American public companies and computes hedged portfolio returns based on the different approaches")
st.markdown("**Author**: *Minh Phan*")
st.markdown("\n\n\n")


# Download Data
acc_data = pd.read_pickle('./acc_data.pickle')
group_labels = ['Accruals - Balance Sheet', 'Accruals - Cash Flow', 'Nontransaction Accrual']


st.header('Methodologies', divider='rainbow')

st.write("""*Sloan’s (1996)* definition of accruals focused on the change in current net operating assets. This balance sheet approach relies on the 
	transactional consistency between changes in working capital balance sheet accounts and accrual components of revenues and expenses on the income statement. 
	However, this consistency breaks down when nonoperating events such as reclassifications, acquisitions, divestitures, accounting changes and foreign currency translations. 
	*Collins and Hribar (2000)* proposes calculating accruals (the non-cash component of earnings) directly using the cash flow statement.
	""")

st.latex(r'''
Accrual_{Balance Sheet}  = \Delta NetOperatingAsset \newline
	= (\Delta CurAssets - \Delta Cash) - (\Delta CurrentLiabilities - \Delta ShortTermDebt - \Delta TaxPayable) - Depreciation
     ''')

st.latex(r'''
	Accrual_{Cash Flow} = NetIncome - CashFlowOperations
    ''')

st.write("""*Lewellen and Resutek (2016)* split total accruals into investment-related and 'nontransaction' accruals, items such as depreciation and asset write-downs that do not represent new investment expenditures. Non transactional accruals may better proxy for earnings quality as it involves more discretion and does not capture the firm's natural growth""")

st.latex(r'''
Accrual_{Non-Transactional}  = DepAndAmort + DeferredTaxes + GainPPESale + FundFromeOperations + ExtraordinaryItems''')

st.write("""

	All accruals are scaled by average total assets.
	""")


# Plot accruals by group
with st.container():
	st.write("\n\n\n")

	st.header('Distribution of Accrual by Different Methods for Selected Industry', divider='rainbow')

	# col1 = st.columns(1)

	# # Columns
	# with col1:
	ind_list=acc_data.loc[acc_data["gsector_str"]!='']['gsector_str'].unique().tolist()
	industry_sel = st.selectbox("Industry", ind_list, index=0)

	# with col2:
	#      acc_sel = st.selectbox(
	#                 "Accrual Measurement", ['Balance Sheet', 'Cash Flow', 'Non-Transaction Accrual'] , index=0)

	acc_data_sub = acc_data.loc[(acc_data['gsector_str'].isin([industry_sel])) & (acc_data['gsector_str']!='')][['gvkey', 'fyear', 'gsector', 'acc_bs', 'acc_cf', 'ntacc_cf']].dropna()


	fig = ff.create_distplot(
	        [acc_data_sub['acc_bs'], acc_data_sub['acc_cf'], acc_data_sub['ntacc_cf']], group_labels, 
	        show_hist=False, show_rug=False)
	fig.update_layout(
		autosize=False,
		width=1100,
	    height=600,
	    title=dict(text="Accrual Distribution for " + str(industry_sel), font=dict(size=25)),
	    yaxis_title=dict(text='Likelihood', font=dict(size=16, color='#FFFFFF')),
	    xaxis_title=dict(text='Accruals/Avg Assets', font=dict(size=16, color='#FFFFFF')),
	    yaxis=dict(tickfont=dict(size=16)),
	    xaxis=dict(tickfont=dict(size=16)),
	    legend=dict(orientation='h', font=dict(size=16,color='#FFFFFF'))
	)

	# Plot!
	st.plotly_chart(fig, use_container_width=False)

cum_ret = pd.read_pickle('./cum_ret.pickle')

with st.container():
	st.write("\n\n\n")

	st.header('Cumulative Returns from Hedged Strategy', divider='rainbow')

	st.write("""The graph shows cumulative returns from a hedged portfolio (long portfolio with lowest quintile accruals, short portfolio with highest quintile accruals). 
		Portfolio returns are market cap weighted and portfolio sorts are conducted annually. The results show that the cashflow approach performs the best over the 20 years but disambiguating non-transactional accruals in the balance sheet approach is important in mitigating the decline of the accruals anomaly in the 2010's
	""")


	st.line_chart(cum_ret, width=800, height=600)






