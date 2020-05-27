from google.cloud import bigquery
import config
client = bigquery.Client()

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

query1 = queryJob(config.QUERY)

# loops through each row in query1 and adds the returned params (subscriptionID, invoiceID)
# to QUERY2, resulting in newQuery. Each instance of newQuery is then sent to queryJob
for row in query1:
    newQuery = addParams(config.QUERY2, subscriptionID=row[0], invoiceID=row[1])
    query2  =  queryJob(newQuery)

    # for rows in query2:
    #   retrive invoice item record from stripe
    #   write record to BQ dataset
    #   request delete from stripe
    #   

print("Total Shipping Cost (in cents): " + str(lineItemTotal))