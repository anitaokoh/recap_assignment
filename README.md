# Recap Assignement

## Goal 
The goal is in two part
- Fetch all the invoice data from the invoice endpoint and save them to a file.
- Calculate the net revenue and the churned amount

## File categories
The code file categories can be grouped into three
- Source code files
- Test file
- Build files 

1. ### Source codes files
  There are two source code files
  - `get_data.py` - This python script gets all the data from all the invoice endpoints and stores in a csv file called `data/invoice_data.csv`
  - `get_data_stats.py` - This python script gets the data extracted calling get_data.py and calculates the net revenue and churned amount for each contract id for each month.

  Note:
  - Although `get_data_stats.py` runs get_data.py directly without accessing the saved data csv, this can be changed to access the file instead


2. ### Test file
  Five cases are tested in `test_data_checks.py`
  - Check if the invoice endpoint request was successful
  - Check if the dataframe/data returned is not empty
  - Check if the  net_revenue calculation logic works as expected
  - Check if the churned amount  calculation logic works as expected
  - Check if the main function that runs the net_revenue and churned amount returns the expected dataframe results

  
**Calculation Definitions** 
  - Net Revenue - The net revenue of contract A in month t is the sum of
original_billing_amount of all its invoices with invoice_date in month t.
For example, contract A could have had two invoices of $50 and $150 in December
2021. That would result in a net revenue of $200 as shown in the table above.
  - Churned Amount - Contract C churns in month t if C has net revenue
Rt−1 > 0 in month t − 1 and net revenue Rt ≤ 0 in month t. The churned
amount in month t is Rt−1.
Consider again the table above. Contract A churned in January 2022 because it
generated positive revenue in December 2021 but no revenue in January 2022.
The churned amount is $200.

_Note_
- The churned amount logic and test only takes account if Rt−1 > 0 and Rt <=0 . I.e other cases like Rt <= 0 and Rt-1 <=0  etc return 0 as the churned amount

3. ## Build file
- Requirement.txt - Contains all the python libraries required to run the source and test files successfully
- Makefile - Helps to automate the library installations and test coverages
- Dockerfile - Helps to containerize the scripts and the environment for reproducibility

## Requirement
You must already have docker installed to run the instructions before successfully or use github codespace 

## Instructions on how to run the scripts 
1. git clone this respository using the code 
```
git clone
```
2. Create a docker image named `anita_test` using the code 
```
docker build -t anita_test .
```
 ( You need to have docker in your mackine or use codespace to run the instructions)
3. Optional, check if the image named **anita_test** was created successfully using 
```
docker image
``` 
4. Run an interactive bash terminal in the container by using the code 
```
docker run -it anita_test bash
```
You would be prompted to a bash interface

5. You can either run each of the source code seperately to see the output results i.e
    - Run `python get_data.py` to see the preview of the data extracted from all  the invoice endpoints or you can also check the full content of the data located at data/invoice_data.csv.
    - Then run `python get_data.py` to see the preview of the calculated net revenue , churned amount for each contract id for each month
    - Finally , you can run `pytest test_data_check.py` to check if all test listed above runs succesfully

Alternative and preferably, you can run both source code scripts and view their results using 
```
make source_code 
```
and then  to get the tests validation and  coverage, run 
```
make test
```

# Good luck