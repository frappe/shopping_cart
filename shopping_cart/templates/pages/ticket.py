# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import webnotes
from webnotes import _
from webnotes.utils import today

no_cache = 1
no_sitemap = 1

def get_context(context):
	bean = webnotes.bean("Support Ticket", webnotes.form_dict.name)
	if bean.doc.raised_by == webnotes.session.user:
		ticket_context = {
			"title": bean.doc.name,
			"bean": bean
		}
	else:
		ticket_context = {"title": "Not Allowed"}
		
	return ticket_context

@webnotes.whitelist()
def add_reply(ticket, message):
	if not message:
		raise webnotes.throw(_("Please write something"))
	
	bean = webnotes.bean("Support Ticket", ticket)
	if bean.doc.raised_by != webnotes.session.user:
		raise webnotes.throw(_("You are not allowed to reply to this ticket."), webnotes.PermissionError)
	
	from webnotes.core.doctype.communication.communication import _make
	_make(content=message, sender=bean.doc.raised_by, subject = bean.doc.subject,
		doctype="Support Ticket", name=bean.doc.name,
		date=today())