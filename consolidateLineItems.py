
import copy
import datetime
import json
import os
import time

# consolidates all shipping label invoice line items into a single line item
# and returns the consolidated invoice
def consolidateLineItems(invoiceID):
    
    # grabs the invoice from the db and converts it to a list. 
    # Also grabs the customer ID / currency used by the invoice, and stores the line
    # items list in originalLineItems

    # TESTING
    with open('originalInvoice.json') as f:
        originalInvoice = json.load(f)

    #invoice = db.session.query.filter_by(id=invoiceID).first()
    #originalInvoice = json.loads(invoice.originalInvoiceJSON)
    consolidatedInvoice = copy.deepcopy(originalInvoice)
    originalLineItems = originalInvoice['lines']['data']
    consolidatedLineItems = consolidatedInvoice['lines']['data']
    currency = originalLineItems[0]['currency']
    consolidateLineItems = []
    totalByDate = {}

    # traverses originalLineItems, storing the first id found for a given date and totaling
    # the the amounts of all matching dates. If it is not a Shipping label line item,
    # it will just append it to the 
    for item in originalLineItems:

        startDate = item['period']['start']

        if item['description'].startswith("Shipping Cost for Label"):

            if startDate not in totalByDate:
                
                totalByDate[startDate] = [item['id'], 0]

            totalByDate[startDate][1] += item['amount']

        else:

            consolidatedLineItems.append(item)
        

    # creates the new lineItem entry for each date and appends it to consolidatedLineItems 
    for date, value in totalByDate.items():

        dateString = datetime.datetime.fromtimestamp(date).strftime('%m-%d-%y')
        newLineItem = {
            'id':value[0],
            'currency':currency,
            'description':'Shipping Cost for ' + dateString,
            'amount':value[1]
        }

        consolidatedLineItems.append(newLineItem)
    
    # TESTING
    with open('consolidatedInvoice.json', 'w', encoding='utf-8') as f2:
        json.dump(consolidatedInvoice, f2, ensure_ascii=False, indent=4)

#    return consolidatedInvoice

