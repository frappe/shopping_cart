# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from shopping_cart.shopping_cart.doctype.shopping_cart_settings.shopping_cart_settings import ShoppingCartSetupError

def get_quotation(user=None):
	if not user:
		user = frappe.session.user
	if user == "Guest":
		raise frappe.PermissionError
		
	is_shopping_cart_enabled()
	party = get_party(user)
	values = {
		"order_type": "Shopping Cart",
		party.doc.doctype.lower(): party.doc.name,
		"docstatus": 0,
	}

	try:
		quotation = frappe.bean("Quotation", values)
	except frappe.DoesNotExistError:
		quotation = frappe.new_bean("Quotation")
		quotation.doc.fields.update(values)
		quotation.insert(ignore_permissions=True)
		
	return quotation
	
def get_party(user):
	customer = frappe.db.get_value("Contact", {"email_id": user}, "customer")
	if customer:
		return frappe.bean("Customer", customer)
	
	lead = frappe.db.get_value("Lead", {"email_id": user})
	if lead:
		return frappe.bean("Lead", lead)
	
	# create a lead
	lead = frappe.new_bean("Lead")
	lead.doc.fields.update({
		"email_id": user,
		"lead_name": get_fullname(user),
		"territory": guess_territory()
	})
	lead.insert(ignore_permissions=True)
	
	return lead
	
def guess_territory():
	if frappe.session.get("session_country"):
		territory = frappe.db.get_value("Territory", frappe.session.get("session_country"))
		return territory or get_default_territory()
		
	return get_default_territory()
		
def get_default_territory():
	return frappe.db.get_value("Shopping Cart Settings", "Shopping Cart Settings", "default_territory")

def guess_territory():
	territory = None
	geoip_country = frappe.session.get("session_country")
	if geoip_country:
		territory = frappe.db.get_value("Territory", geoip_country)
	
	return territory or \
		frappe.db.get_value("Shopping Cart Settings", None, "territory") or \
		"All Territories"

def is_shopping_cart_enabled():
	if not frappe.db.get_value("Shopping Cart Settings", "Shopping Cart Settings", "enabled"):
		frappe.throw(_("You need to enable Shopping Cart"), ShoppingCartSetupError)