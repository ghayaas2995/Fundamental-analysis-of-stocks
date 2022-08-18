# Fundamental-analysis-of-stocks
Project to explore indicators that help a modelling and reporting buy signal with probability of success. Creating a Discounted cash flow model to perform fundamental analysis of stock

Summary of project:

•	Analyzed the particulars of income statement and balance sheet of a company as percentage of revenue by fetching data from api to forecast the revenue growth, net income, and balance sheet for the next 5 years

•	Performed fundamental analysis by calculating WACC of the company and creating a dynamic discounted cash flow model in python to forecast the share price at the end of 5 years to signal current buy / sell opportunity

•	Calculated working average cost of capital of the company to use as a discount rate to calculate net present value of the company to discount the future free cash flows

Important terminologies: 

Cash is what the firm needs in order to be able to pay bills, taxes, salaries and also to pay back to the company capital providers.

The company reported cash flow statements splits company activities into three parts. Investment activities, financing activities and operating activities. For the discounted cash flow method, we will mainly focus on the operating cash flow. Operating cash flow reflects all cash in and outflows related to the production and sale of the company goods and services.

To calculate the free cash flow, we would need the following parameters of the company

Net income

(+) Depreciation

(-) Increase in accounts receivable

(-) Increase in inventory

(-) Increase in other assets

(+) Increase in accounts payable

(+) Increase in other liabilities

Operating cash flow

(-) Purchases of equipment or capital expenditures

Weighted Average Cost of Capital
The WACC is a firm cost of capital. Is the capital rate that a firm is expected to pay on average to all its security holders. WACC uses cost of debt, cost of equity, capital structure of a firm and tax rate. A company capital structure is important to compute WACC since it uses the blended cost of capital across all sources of capital (i.e. cost of debt and cost of equity).

WACC is commonly used as a discount rate to calculate the net present value of a company. For example, when valuing a company using the Discounted Cash Flow model, we should use WACC to discount future free cash flows.

WACC is calculated using the below formula:

WACC = Kd (1 -Tc) (D /D+E) + Ke * (E /D+E)

Where:

WACC = Weighted Average Cost of Capital

Kd = Cost of debt

Tc = Tax effective rate

Ke = Cost of equity

D / D + E = Proportion of debt in firm capital structure
