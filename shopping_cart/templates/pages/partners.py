# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import frappe.website.render

def get_context(context):
	return {
		"partners": frappe.conn.sql("""select * from `tabSales Partner`
			where show_in_website=1 order by name asc""", as_dict=True),
		"title": "Partners"
	}

def clear_cache(bean, trigger):
	if bean.doc.page_name:
		frappe.website.render.clear_cache("partners")
	