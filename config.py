QUERY = ("""
    SELECT line_item_subscription,id, invoice_date, count(distinct line_item_id) as line_item_count, sum(total) as total FROM `v1-dev-main.stripe.vw_LatestInvoices_lineitems` 
    WHERE lower(line_item_description) like '%ship%cost%label%'
    AND invoice_date >= '2020-05-01'
    GROUP BY
    line_item_subscription,id, invoice_date
    HAVING count(distinct line_item_id) >= 5
""")

# TODO > 
#  return subscriptionID, invoiceID, invoiceItemID
QUERY2 = ("""
    SELECT * FROM `v1-dev-main.stripe.vw_LatestInvoices_lineitems`
    WHERE id = 'invoiceID'
    AND line_item_subscription = 'subscriptionID'
    ORDER BY line_item_id
""")