import requests
import pandas as pd

def parse_url(base_url, page_number):
    """
    Get the request object 
    """
  
    return requests.get(base_url+str(page_number))


def main():
    """
    Store the json data in a list . If the json data is empty, stop loop.
    """
    base_url = 'https://nookdtmzylu7w75p7atatnzom40zmdpz.lambda-url.eu-central-1.on.aws/invoices?page='
    data_content = []
    page_number = 1
    new_content = True

    while new_content:
        html_content = parse_url(base_url, page_number)
        new_content = html_content.json()['body']['data']
        data_content.extend(new_content)
        page_number +=1
    df = pd.DataFrame(data_content)
    return df

if __name__ == '__main__':
    df=main()
    file_path = "data/invoice_data.csv"
    df.to_csv(file_path, index=False)
    print("-----Invoice Data Extract Preview-----")
    print(df.head())
    print("-------------------")
    print(f"Data saved in {file_path}")
