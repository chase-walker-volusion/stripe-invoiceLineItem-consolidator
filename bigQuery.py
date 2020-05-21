from google.cloud import bigquery

client = bigquery.Client()

lineItemTotal = 0

QUERY = ("""
    SELECT line_item_subscription,id, invoice_date, count(distinct line_item_id) as line_item_count FROM `v1-dev-main.stripe.vw_LatestInvoices_lineitems` 
    WHERE lower(line_item_description) like '%ship%cost%label%'
    AND invoice_date >= '2020-05-01'
    GROUP BY
    line_item_subscription,id, invoice_date
    HAVING count(distinct line_item_id) >= 5
""")
QUERY2 = ("""
    SELECT * FROM `v1-dev-main.stripe.vw_LatestInvoices_lineitems`
    WHERE id = 'invoiceID'
    AND line_item_subscription = 'subscriptionID'
    ORDER BY line_item_id
""")

# adds any number of kwargs to replace variables in a given query
# key should be the same as the text variable within the query
def addParams(query, **kwargs):
    for key, value in kwargs.items():
        query = str.replace(query, key, value)
    return query


# take a SQL query string and returns the query result from BQ
# also prints out each row returned, and adds the amount for the row to lineItemTotal
def queryJob(query):
    global lineItemTotal
    query_job = client.query(query) 
    rows = list(query_job.result())
    for row in rows:
        print(row)
        if len(row) > 4: # query1 is only len 4, so anything larger is query2
            lineItemTotal += row[2] # row[2] is amount in query2
    return rows

query1 = queryJob(QUERY)

# loops through each row in query1 and adds the returned params (subscriptionID, invoiceID)
# to QUERY2, resulting in newQuery. Each instance of newQuery is then sent to queryJob
for row in query1:
    newQuery = addParams(QUERY2, subscriptionID=row[0], invoiceID=row[1])
    queryJob(newQuery)

print("Total Shipping Cost (in cents): " + str(lineItemTotal))