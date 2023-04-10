import pytest
from get_data_stats import calculate_net_revenue, calculate_churned_amount, main_function, group_by_contract_id
from get_data import main, parse_url
import pandas as pd


def test_parse_url():
    """
    Check if the request was successfull i.e response results is 200
    """
    base_url = 'https://nookdtmzylu7w75p7atatnzom40zmdpz.lambda-url.eu-central-1.on.aws/invoices?page='
    html_content = parse_url(base_url, 1)
    assert html_content.status_code == 200


def test_main_empty_data():
    """
    Check if the data extracted is 
    """
    df = main()
    assert df.shape[0] > 0
    assert list(df.columns) == ["original_billing_amount", "contract_id","invoice_id", "invoice_date"]

def test_calculate_net_revenue():
    df = pd.DataFrame([{"original_billing_amount":20, "contract_id": "a123", "invoice_date": "2020-08-01"},
                        {"original_billing_amount":30, "contract_id": "a123", "invoice_date": "2020-08-02"},
                        {"original_billing_amount":-30, "contract_id": "b123", "invoice_date": "2020-09-03"},
                        {"original_billing_amount":50, "contract_id": "b123", "invoice_date": "2020-09-22"}])
    assert calculate_net_revenue(df).shape[0] == 2
    assert calculate_net_revenue(df)['net_revenue'][0] ==50
    assert calculate_net_revenue(df)['net_revenue'][1] == 20


def test_calculate_churned_amount():
    df = pd.DataFrame([{ "month": "2020-08-01", "net_revenue": 20}, {"month": "2020-09-01", "net_revenue": 30 }, {"month": "2020-08-03", "net_revenue": -10 }, {"month": "2020-08-04","net_revenue": 0 }])
    df["churned_amount"] = calculate_churned_amount(df)
    assert df["churned_amount"][1] == 0.0
    assert df["churned_amount"][2] == 30.0
    assert df["churned_amount"][3] == 0.0

def test_main_function():
    df = pd.DataFrame([{"original_billing_amount":20, "contract_id": "a123", "invoice_date": "2020-08-01"},
                        {"original_billing_amount":30, "contract_id": "a123", "invoice_date": "2020-08-02"},
                        {"original_billing_amount":20, "contract_id": "a123", "invoice_date": "2020-09-01"},
                        {"original_billing_amount":30, "contract_id": "a123", "invoice_date": "2020-09-30"},
                        {"original_billing_amount":30, "contract_id": "b123", "invoice_date": "2020-09-03"},
                        {"original_billing_amount":50, "contract_id": "b123", "invoice_date": "2020-09-22"},
                        {"original_billing_amount":-70, "contract_id": "b123", "invoice_date": "2020-10-01"},
                        {"original_billing_amount":30, "contract_id": "b123", "invoice_date": "2020-10-10"}])

    data = pd.DataFrame(columns=["month", "contract_id", "net_revenue", "churned_amount"])
    aggregation_df = calculate_net_revenue(df)
    contracts = list(aggregation_df['contract_id'].unique())
    for contract_id in contracts:
        df_by_contract = group_by_contract_id(aggregation_df, contract_id)
        df_by_contract['churned_amount'] = calculate_churned_amount(df_by_contract)
        data = pd.concat([data, df_by_contract],ignore_index=True)
    assert data[(data['contract_id']=='a123') & (data['month']=='2020-09-01')]['churned_amount'].values[0] == 0
    assert data[(data['contract_id']=='b123') & (data['month']=='2020-10-01')]['churned_amount'].values[0] == 80
