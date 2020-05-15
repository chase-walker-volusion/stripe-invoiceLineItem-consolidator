"""
Stripe Shipping Label LineItem Reducer
"""

"""
flask
"""

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import datetime

# setup flask and it's URI
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoices.db'

# root index page
@app.route('/', methods=['POST', 'GET'])
def index():

    # POST method to add invoices to the db
    if request.method == 'POST':

        # grabs invoice IDs from the form
        invoice_content = request.form['invoice_content']
        new_invoices = Invoices(content=invoice_content)

        # attempts to add invoice to db
        try:
            dbAdd(invoice_content)
            return redirect('/')
        except:
            return 'Unable to commit new invoices from POST request'
    
    # GET method to return all invoices in the db
    else:
        invoices = Invoices.query.order_by(Invoices.date_added).all()
        return render_template('index.html', invoices=invoices)

    return render_template('index.html')

# revert page
@app.route('/revert/<int:id>')
def revert():

    # attempts to find the invoice in the db and returns 404 if not found
    invoice_to_revert = Invoices.query.get_or_404(id)

    # attempts to revert the changes made to the invoice
    try:
        dbRevert(id)
        return redirect('/')
    
    except:
        return 'Unable to commit revert of invoice: %r' % id
    
# starts the app
if __name__ == '__main__':
    app.run(debug=True)

"""
Stripe
"""
import stripe

stripe.api_key = ""

# returns invoice that matches given id
def getInvoiceItems(id):
    return invoiceItems

# updates a given invoice. Takes invoice ID, and the items to add to the invoice. Returns the items that were added
def updateInvoiceItems(id, invoiceItems):
    return updatedInvoiceItems

"""
SQL
"""

db = SQLAlchemy(app)

# sets up the Invoices db model
class Invoices(db.Model):

    # columns for the db with id being the primary key
    id = db.Column(db.String(30), primary_key=True)
    customer = db.Column(db.String(30), nullable=False)
    originalInvoiceJSON, currentInvoiceJSON = db.Column(db.JSON())
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime)

    # string representation of the object
    def __repr__(self):
            return '<Invoice %r>' % self.id