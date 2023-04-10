import pandas as pd
import numpy as np
from get_data import main
from pandas.tseries.offsets import MonthBegin
from pandas.errors import SettingWithCopyWarning
import warnings
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

def calculate_net_revenue(df):
    """
    Calculate the net revenue for each contract_id each month
    """
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    df['month'] = df['invoice_date'].dt.normalize().map(MonthBegin().rollback)
    return  df.groupby(['month', 'contract_id'] ,as_index=False)['original_billing_amount'].sum().rename(columns={'original_billing_amount':'net_revenue'})

def group_by_contract_id(df, contract_id):
    """
    Filter dataframe by contract_id
    """
    return df[df['contract_id']==contract_id].sort_values(by=['month'])

def calculate_churned_amount(df):
    """
    Calculate the churned amount for each contract id for each month based on the net revenue for previous month.
    If Rt <=0 and Rt-1 > 0 then churned amount for RT = RT-1
    where 
     - Rt = Net Revenue for current month
     - Rt-1 = Net Revenue for the previous month
    """
    return np.where((df['net_revenue']<= 0) & (df['net_revenue'].shift(1)> 0), df['net_revenue'].shift(1) , 0)

def main_function():
    """
    Get the data and calculate both the net revenue and the churned amount for each month
    """
    data = pd.DataFrame(columns=["month", "contract_id", "net_revenue", "churned_amount"])
    df = main()
    aggregation_df = calculate_net_revenue(df)
    contracts = list(aggregation_df['contract_id'].unique())
    for contract_id in contracts:
        df_by_contract = group_by_contract_id(aggregation_df, contract_id)
        df_by_contract['churned_amount'] = calculate_churned_amount(df_by_contract)
        data = pd.concat([data, df_by_contract],ignore_index=True)
    return data

if __name__ == '__main__':
    print("Starting Net Revenue and Churned Amount Calculation")
    df=main_function()
    print("-------------------------------------------------")
    print("-----Result Preview-----")
    print(df.head())
    
