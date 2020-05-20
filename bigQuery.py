from google.cloud import bigquery

client = bigquery.Client()

# Perform a query.
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
    WHERE id = 'in_1GjB9nJXC8AX4nQMj9z2PnNJ'
    AND line_item_subscription = 'sub_ELeCi1zPEqGisC'
    ORDER BY line_item_id
""")
query_job = client.query(QUERY)  # API request
rows = query_job.result()  # Waits for query to finish

for row in rows:
    print(row)
