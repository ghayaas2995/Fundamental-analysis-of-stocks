#!/usr/bin/env python
# coding: utf-8

# # Calculating WACC - Weighted Average Cost of Capital

# The WACC is a firm cost of capital. Is the capital rate that a firm is expected to pay on average to all its security holders. WACC uses cost of debt, cost of equity, capital structure of a firm and tax rate. A company capital structure is important to compute WACC since it uses the blended cost of capital across all sources of capital (i.e. cost of debt and cost of equity).

# WACC is commonly used as a discount rate to calculate the net present value of a company. For example, when valuing a company using the Discounted Cash Flow model, we should use WACC to discount future free cash flows.

# WACC is calculated using the below formula:
# 
# WACC = Kd * (1 -Tc) * (D /D+E) + Ke * (E /D+E)
# 
# Where:
# 
# WACC = Weighted Average Cost of Capital
# 
# Kd = Cost of debt
# 
# Tc = Tax effective rate
# 
# Ke = Cost of equity
# 
# D / D + E = Proportion of debt in firm capital structure

# In[1]:


#!pip install pandas_datareader
import pandas_datareader.data as web
import datetime
import requests
import numpy as np


# In[2]:


# Cost of Debt
# the approach to calculate cost of debt is, we are going to calculate credit spread and then we will add the risk free rate
# Therefore, Kd = RF + credit spread
# for each of the element in thw formula for WACC, we will create a function


# In[3]:


# Define the company you want to analyse in the company parameter and input the free api from 
# www.financialmodelingprep.com

company = 'MSFT'
demo = '354f5f0ad406efc5d56acbb8a6b08f1f'


# Interest coverage ratio:
# 
# The interest coverage ratio is a debt and profitability ratio used to determine how easily a company can pay interest on its outstanding debt. The interest coverage ratio is calculated by dividing a company's earnings before interest and taxes (EBIT) by its interest expense during a given period.
# 
# The formula used is:
# 
# \begin{aligned} &\text{Interest Coverage Ratio}=\frac{\text{EBIT}}{\text{Interest Expense}}\\ &\textbf{where:}\\ &\text{EBIT}=\text{Earnings before interest and taxes} \end{aligned} 
# 

# In[4]:


def interest_coverage_and_RF(company):
    # Defining the time frame: from today to a year before
    end= datetime.datetime.today()
    start = (end - datetime.timedelta(366)).strftime('%Y-%m-%d')
    end= datetime.datetime.today().strftime('%Y-%m-%d')
    
    IS= requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?apikey={demo}').json()
    EBIT= IS[0]['ebitda'] - IS[0]['depreciationAndAmortization'] 
    interest_expense = IS[0]['interestExpense']
    interest_coverage_ratio = EBIT / interest_expense
    
    # To extract risk free rate RF:
    Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
    RF = float(Treasury.iloc[-1])
    RF = RF/100
    print('Risk Free Rate of',company,'=', RF,'\nInterest Coverage Ratio =', interest_coverage_ratio)
    return [RF, interest_coverage_ratio]

interest = interest_coverage_and_RF(company)
RF = interest[0]
interest_coverage_ratio = interest[1]


# In[5]:


# COst of Debt:

def cost_of_debt(company, RF,interest_coverage_ratio):
    if interest_coverage_ratio > 8.5:
    #Rating is AAA
        credit_spread = 0.0063
    if (interest_coverage_ratio > 6.5) & (interest_coverage_ratio <= 8.5):
    #Rating is AA
        credit_spread = 0.0078
    if (interest_coverage_ratio > 5.5) & (interest_coverage_ratio <=  6.5):
    #Rating is A+
        credit_spread = 0.0098
    if (interest_coverage_ratio > 4.25) & (interest_coverage_ratio <=  5.49):
    #Rating is A
        credit_spread = 0.0108
    if (interest_coverage_ratio > 3) & (interest_coverage_ratio <=  4.25):
    #Rating is A-
        credit_spread = 0.0122
    if (interest_coverage_ratio > 2.5) & (interest_coverage_ratio <=  3):
    #Rating is BBB
        credit_spread = 0.0156
    if (interest_coverage_ratio > 2.25) & (interest_coverage_ratio <=  2.5):
    #Rating is BB+
        credit_spread = 0.02
    if (interest_coverage_ratio > 2) & (interest_coverage_ratio <=  2.25):
    #Rating is BB
        credit_spread = 0.0240
    if (interest_coverage_ratio > 1.75) & (interest_coverage_ratio <=  2):
    #Rating is B+
        credit_spread = 0.0351
    if (interest_coverage_ratio > 1.5) & (interest_coverage_ratio <=  1.75):
    #Rating is B
        credit_spread = 0.0421
    if (interest_coverage_ratio > 1.25) & (interest_coverage_ratio <=  1.5):
    #Rating is B-
        credit_spread = 0.0515
    if (interest_coverage_ratio > 0.8) & (interest_coverage_ratio <=  1.25):
    #Rating is CCC
        credit_spread = 0.0820
    if (interest_coverage_ratio > 0.65) & (interest_coverage_ratio <=  0.8):
    #Rating is CC
        credit_spread = 0.0864
    if (interest_coverage_ratio > 0.2) & (interest_coverage_ratio <=  0.65):
    #Rating is C
        credit_spread = 0.1134
    if interest_coverage_ratio <=  0.2:
    #Rating is D
        credit_spread = 0.1512
  
    cost_of_debt = RF + credit_spread
    print(cost_of_debt)
    return cost_of_debt

kd = cost_of_debt(company,RF,interest_coverage_ratio)


# In[6]:


# cost of equity:

def costofequity(company):
    
    # Defining the time frame: from today to a year before
    end= datetime.datetime.today()
    start = (end - datetime.timedelta(366)).strftime('%Y-%m-%d')
    end= datetime.datetime.today().strftime('%Y-%m-%d')    
    
    #RF
    Treasury = web.DataReader(['TB1YR'], 'fred', start, end)
    RF = float(Treasury.iloc[-1])
    RF = RF/100

    #Beta
    beta = requests.get(f'https://financialmodelingprep.com/api/v3/company/profile/{company}?apikey={demo}')
    beta = beta.json()
    beta = float(beta['profile']['beta'])

    #Market Return
    SP500 = web.DataReader(['sp500'], 'fred', start, end)
      #Drop all Not a number values using drop method.
    SP500.dropna(inplace = True)

    SP500yearlyreturn = (SP500['sp500'].iloc[-1]/ SP500['sp500'].iloc[-252])-1
    
    cost_of_equity = RF+(beta*(SP500yearlyreturn - RF))
    return cost_of_equity
ke = costofequity(company)
ke


# In[7]:


# To calculate WACC

def wacc(company):
    
    #Calculate effective tax rate
    # retreving the Financial ratios from the financial modeling prep api
    FR = requests.get(f'https://financialmodelingprep.com/api/v3/ratios/{company}?apikey={demo}').json()
    ETR = FR[0]['effectiveTaxRate']  # index [0] represents the latest year effeective tax rate of the company

    #capital structure 
    # Get request of the balance sheet
    BS = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?apikey={demo}').json()
   
    # Debt is calculated by dividing the total debt of company by total debt + total stockholders equity 
    Debt_to = BS[0]['totalDebt'] / (BS[0]['totalDebt'] + BS[0]['totalStockholdersEquity'])
    
    # equity is calculated by dividing the total stockholders equity of company by total debt + total stockholders equity 
    equity_to = BS[0]['totalStockholdersEquity'] / (BS[0]['totalDebt'] + BS[0]['totalStockholdersEquity'])

    #wacc is finally calculated by applying the formula shown earlier
    WACC = (kd*(1-ETR)*Debt_to) + (ke*equity_to)
    print('WACC:',WACC,'\nProportion of equity in firm capital structure:',equity_to,'\nProportion of debt in firm capital structure:',Debt_to)
    return WACC
wacc_company = wacc(company)
print('Wacc of ' + company + ' is ' + str((wacc_company*100))+'%')   


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




