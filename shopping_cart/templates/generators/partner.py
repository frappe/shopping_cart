# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import webnotes

doctype = "Sales Partner"
condition_field = "show_in_website"

def get_context(controller, method):
	address = webnotes.conn.get_value("Address", 
		{"sales_partner": controller.doc.name, "is_primary_address": 1}, 
		"*", as_dict=True)
	if address:
		city_state = ", ".join(filter(None, [address.city, address.state]))
		address_rows = [address.address_line1, address.address_line2,
			city_state, address.pincode, address.country]
			
		controller.doc.fields.update({
			"email": address.email_id,
			"partner_address": filter_strip_join(address_rows, "\n<br>"),
			"phone": filter_strip_join(cstr(address.phone).split(","), "\n<br>")
		})