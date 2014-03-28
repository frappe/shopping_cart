# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import today

no_cache = 1
no_sitemap = 1

def get_context(context):
	bean = frappe.bean("Support Ticket", frappe.form_dict.name)
	if bean.raised_by == frappe.session.user:
		ticket_context = {
			"title": bean.name,
			"bean": bean
		}
	else:
		ticket_context = {"title": "Not Allowed"}
		
	return ticket_context

@frappe.whitelist()
def add_reply(ticket, message):
	if not message:
		raise frappe.throw(_("Please write something"))
	
	bean = frappe.bean("Support Ticket", ticket)
	if bean.raised_by != frappe.session.user:
		raise frappe.throw(_("You are not allowed to reply to this ticket."), frappe.PermissionError)
	
	from frappe.core.doctype.communication.communication import _make
	_make(content=message, sender=bean.raised_by, subject = bean.subject,
		doctype="Support Ticket", name=bean.name,
		date=today())