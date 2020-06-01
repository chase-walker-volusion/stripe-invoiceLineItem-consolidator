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
# key should be the same as the text variable within the query
def addParams(query, **kwargs):
    for key, value in kwargs.items():
        query = str.replace(query, key, value)
    return query


# take a SQL query string and returns the query result from BQ
# also prints out each row returned, and adds the amount for the row to lineItemTotal
def queryJob(query):
    query_job = client.query(query) 
    rows = list(query_job.result())
    return rows

def uploadJob(uploadFileName, table):
    table.reload()

    with open(uploadFileName, 'rb') as uploadFile:
        job = table.upload_from_file(uploadFile, source_format='NEWLINE_DELIMITED_JSON')
        
    jobResult = list(job.result())
    return jobResult

qualifyingInvoices = queryJob(config.qualifyingInvoicesQuery)

# loops through each row in query1 and adds the returned params (subscriptionID, invoiceID)
# to QUERY2, resulting in newQuery. Each instance of newQuery is then sent to queryJob

for invoice in qualifyingInvoices:
    newQuery = addParams(config.invoiceItemQuery, subscriptionID=invoice[0], invoiceID=invoice[1])
    invoiceItem = queryJob(newQuery)
    invoiceItemID = invoiceItem[0][0]
    stripeBackup = stripe.InvoiceItem.retrieve(invoiceItemID)
    with open('backup.json', 'a') as f:
        json.dump(stripeBackup, f)
    # for rows in query2:
    #   retrive invoice item record from stripe
    #   write record to BQ dataset
    #   request delete from stripe
    #   
for backup in stripeBackup:
    uploadJob('backup.json', backupTable)