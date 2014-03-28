# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import cint, formatdate

no_cache = 1
no_sitemap = 1

def get_context(context):
	return {
		"title": "My Tickets",
		"method": "shopping_cart.templates.pages.tickets.get_tickets",
		"icon": "icon-ticket",
		"empty_list_message": "No Tickets Raised",
		"page": "ticket"
	}

@frappe.whitelist()
def get_tickets(start=0):
	tickets = frappe.db.sql("""select name, subject, status, creation 
		from `tabSupport Ticket` where raised_by=%s 
		order by modified desc
		limit %s, 20""", (frappe.session.user, cint(start)), as_dict=True)
	for t in tickets:
		t.creation = formatdate(t.creation)
	
	return tickets
	
@frappe.whitelist()
def make_new_ticket(subject, message):
	if not (subject and message):
		raise frappe.throw(_("Please write something in subject and message!"))
		
	from erpnext.support.doctype.support_ticket.get_support_mails import add_support_communication
	ticket = add_support_communication(subject, message, frappe.session.user)
	
	return ticket.name