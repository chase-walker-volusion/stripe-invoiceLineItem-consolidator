from google.cloud import bigquery
import json
import config
import stripe
import key
stripe.api_key = key.key
client = bigquery.Client()
backupDataSet = client.dataset('dev_chasew')
backupTable = backupDataSet.table('stripe_lineItem_backup')

# adds any number of kwargs to replace variables in a given query
# TAKES:
# query (string)
# **kwargs
# RETURNS:
# query (string) w/ updated parameters from **kwargs
def addParams(query, **kwargs):
    for key, value in kwargs.items():
        query = str.replace(query, key, value)
    return query

# sends SQL query string to BQ and returns the result
# TAKES:
# query (string)
# RETURNS:
# queryResult (list)
def queryJob(query):
    query_job = client.query(query) 
    queryResult = list(query_job.result())
    return queryResult

# sends JSON file to provided BQ table
# TAKES:
# uploadFileName (string)
# table (google.cloud.bigquery.table.TableReference) 
# RETURNS:
# jobResult (list)
def uploadJob(uploadFileName, table):
    table.reload() # pulls the table schema (needs to have already been created)

    with open(uploadFileName, 'rb') as uploadFile:
        job = table.upload_from_file(uploadFile, source_format='NEWLINE_DELIMITED_JSON')
        
    jobResult = list(job.result())
    return jobResult

# list of all invoices that have 5 or more (inclusive) shipping label invoice items
qualifyingInvoices = queryJob(config.qualifyingInvoicesQuery)

# loops through each invoice in qualifyingInvoices and creates a parameterizedQuery with the subscriptionID and invoiceID provided in the invoice
# parameterizedQuery is then sent to stripe to grab a backup of the invoice, which is then saved to backup.json
for invoice in qualifyingInvoices:
    parameterizedQuery = addParams(config.invoiceItemQuery, subscriptionID=invoice[0], invoiceID=invoice[1])
    invoiceItem = queryJob(parameterizedQuery)
    invoiceItemID = invoiceItem[0][0]
    stripeBackup = stripe.InvoiceItem.retrieve(invoiceItemID)

    with open('backup.json', 'a') as f:
        json.dump(stripeBackup, f)

    # stripe.InvoiceItem.delete(invoiceItemID)

# uploads the backup.json file to the backupTable
uploadJob('backup.json', backupTable)