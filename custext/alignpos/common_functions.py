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

