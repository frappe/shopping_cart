# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import today

no_cache = 1
no_sitemap = 1

def get_context(context):
	doc = frappe.get_doc("Support Ticket", frappe.form_dict.name)
	if doc.raised_by == frappe.session.user:
		ticket_context = {
			"title": doc.name,
			"doc": doc
		}
	else:
		ticket_context = {"title": "Not Allowed", "doc": {}}

	return ticket_context

@frappe.whitelist()
def add_reply(ticket, message):
	if not message:
		raise frappe.throw(_("Please write something"))

	doc = frappe.get_doc("Support Ticket", ticket)
	if doc.raised_by != frappe.session.user:
		raise frappe.throw(_("You are not allowed to reply to this ticket."), frappe.PermissionError)

	from frappe.core.doctype.communication.communication import _make
	_make(content=message, sender=doc.raised_by, subject = doc.subject,
		doctype="Support Ticket", name=doc.name,
		date=today())
