# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import json

import webnotes
from webnotes.utils import cint

from shopping_cart.shopping_cart.cart import get_lead_or_customer

no_cache = 1
no_sitemap = 1

def get_context():
	def _get_fields(fieldnames):
		return [webnotes._dict(zip(["label", "fieldname", "fieldtype", "options"], 
				[df.label, df.fieldname, df.fieldtype, df.options]))
			for df in webnotes.get_doctype("Address", processed=True).get({"fieldname": ["in", fieldnames]})]
	
	bean = None
	if webnotes.form_dict.name:
		bean = webnotes.bean("Address", webnotes.form_dict.name)
	
	return {
		"doc": bean.doc if bean else None,
		"meta": webnotes._dict({
			"left_fields": _get_fields(["address_title", "address_type", "address_line1", "address_line2",
				"city", "state", "pincode", "country"]),
			"right_fields": _get_fields(["email_id", "phone", "fax", "is_primary_address",
				"is_shipping_address"])
		}),
		"cint": cint
	}
	
@webnotes.whitelist()
def save_address(fields, address_fieldname=None):
	party = get_lead_or_customer()
	fields = json.loads(fields)
	
	if fields.get("name"):
		bean = webnotes.bean("Address", fields.get("name"))
	else:
		bean = webnotes.bean({"doctype": "Address", "__islocal": 1})
	
	bean.doc.fields.update(fields)
	
	party_fieldname = party.doctype.lower()
	bean.doc.fields.update({
		party_fieldname: party.name,
		(party_fieldname + "_name"): party.fields[party_fieldname + "_name"]
	})
	bean.ignore_permissions = True
	bean.save()
	
	if address_fieldname:
		update_cart_address(address_fieldname, bean.doc.name)
	
	return bean.doc.name
	
