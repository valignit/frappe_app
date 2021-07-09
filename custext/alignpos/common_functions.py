##################################################
# Application: alignPOS
# Installation: AFSM
# Hook Program: common_functions
# Description: Commonly used functions across the module
# Version: 1.0
# 1.0.0 - 04-05-2021: New program
##################################################

from __future__ import unicode_literals
import frappe
import json
import frappe.utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form, strip_html
from frappe import _
from six import string_types
from frappe.model.utils import get_fetch_values
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
def update_loyalty_points(doc, target_doc=None):

    doc_customer = frappe.get_doc("Customer", doc.customer)

    points_list = frappe.db.get_list(
            'Loyalty Point Entry',
                filters={'customer': doc.customer },
                    fields=['customer', 'loyalty_points']
                    )

    total_loyalty_points = 0
    for point in points_list:
        total_loyalty_points = total_loyalty_points + int(point['loyalty_points'])
    doc_customer.loyalty_points = total_loyalty_points
    doc_customer.customer_sync_date_time = frappe.utils.get_datetime()
    doc_customer.save()


@frappe.whitelist()
def create_exchange_adjustment(docname):

    doc_sales_invoice = frappe.get_doc('Sales Invoice', docname)

    #msgstr = 'whitelist:'
    msgstr = 'whitelist:' + str(doc_sales_invoice.grand_total)
    frappe.msgprint(msgstr)

    doc_payment_entry = frappe.get_doc({
        'doctype' : "Payment Entry",
        'company' : doc_sales_invoice.company,
        'payment_type' : "Pay",
        'posting_date' : frappe.utils.nowdate(),
        'party_type' : "Customer",
        'party' : doc_sales_invoice.customer, 
        'mode_of_payment' : "Exchange Adjustment",
        'paid_from' : "Exchange Adjustment - AFSM",
        'paid_to' : "Debtors - AFSM",
        'paid_amount' : doc_sales_invoice.rounded_total,
        'received_amount' : doc_sales_invoice.rounded_total
    })
    allocated_amount = doc_sales_invoice.grand_total  -1
    #allocated_amount = doc_sales_invoice.grand_total * -1
    frappe.msgprint(str(allocated_amount))
    doc_payment_entry.append("references", {
        'reference_doctype': "Sales Invoice",
        'reference_name': doc_sales_invoice.return_against,
        'allocated_amount': allocated_amount 
    })
    frappe.msgprint('here2')
    doc_payment_entry.insert()
    frappe.msgprint('here3')

