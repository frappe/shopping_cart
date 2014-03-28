# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
from frappe.utils import cstr, cint, fmt_money
from frappe.website.render import clear_cache
from shopping_cart.shopping_cart.cart import _get_cart_quotation

@frappe.whitelist(allow_guest=True)
def get_product_info(item_code):
	"""get product price / stock info"""
	if not cint(frappe.db.get_default("shopping_cart_enabled")):
		return {}
	
	cart_quotation = _get_cart_quotation()
	
	price_list = frappe.local.request.cookies.get("selling_price_list")

	warehouse = frappe.db.get_value("Item", item_code, "website_warehouse")
	if warehouse:
		in_stock = frappe.db.sql("""select actual_qty from tabBin where
			item_code=%s and warehouse=%s""", (item_code, warehouse))
		if in_stock:
			in_stock = in_stock[0][0] > 0 and 1 or 0
	else:
		in_stock = -1
		
	price = price_list and frappe.db.sql("""select price_list_rate, currency from
		`tabItem Price` where item_code=%s and price_list=%s""", 
		(item_code, price_list), as_dict=1) or []
	
	price = price and price[0] or None
	qty = 0

	if price:
		price["formatted_price"] = fmt_money(price["price_list_rate"], currency=price["currency"])
		
		price["currency"] = not cint(frappe.db.get_default("hide_currency_symbol")) \
			and (frappe.db.get_value("Currency", price.currency, "symbol") or price.currency) \
			or ""
		
		if frappe.session.user != "Guest":
			item = cart_quotation.doclist.get({"item_code": item_code})
			if item:
				qty = item[0].qty

	return {
		"price": price,
		"stock": in_stock,
		"uom": frappe.db.get_value("Item", item_code, "stock_uom"),
		"qty": qty
	}

@frappe.whitelist(allow_guest=True)
def get_product_list(search=None, start=0, limit=10):
	# base query
	query = """select name, item_name, page_name, website_image, item_group, 
			web_long_description as website_description
		from `tabItem` where docstatus = 0 and show_in_website = 1 """
	
	# search term condition
	if search:
		query += """and (web_long_description like %(search)s or
				item_name like %(search)s or name like %(search)s)"""
		search = "%" + cstr(search) + "%"
	
	# order by
	query += """order by weightage desc, modified desc limit %s, %s""" % (start, limit)

	data = frappe.db.sql(query, {
		"search": search,
	}, as_dict=1)
	
	return [get_item_for_list_in_html(r) for r in data]

def get_item_for_list_in_html(context):
	return frappe.get_template("templates/includes/product_in_grid.html").render(context)
	
def get_product_list_for_group(product_group=None, start=0, limit=10):
	child_groups = ", ".join(['"' + i[0] + '"' for i in get_child_groups(product_group)])

	# base query
	query = """select name, item_name, page_name, website_image, item_group, 
			web_long_description as website_description
		from `tabItem` where docstatus = 0 and show_in_website = 1
		and (item_group in (%s)
			or name in (select parent from `tabWebsite Item Group` where item_group in (%s))) """ % (child_groups, child_groups)
	
	query += """order by weightage desc, modified desc limit %s, %s""" % (start, limit)

	data = frappe.db.sql(query, {"product_group": product_group}, as_dict=1)

	return [get_item_for_list_in_html(r) for r in data]

def get_child_groups(item_group_name):
	item_group = frappe.get_doc("Item Group", item_group_name)
	return frappe.db.sql("""select name 
		from `tabItem Group` where lft>=%(lft)s and rgt<=%(rgt)s
			and show_in_website = 1""", item_group.fields)

def scrub_item_for_list(r):
	if not r.website_description:
		r.website_description = "No description given"
	if len(r.website_description.split(" ")) > 24:
		r.website_description = " ".join(r.website_description.split(" ")[:24]) + "..."

def get_group_item_count(item_group):
	child_groups = ", ".join(['"' + i[0] + '"' for i in get_child_groups(item_group)])
	return frappe.db.sql("""select count(*) from `tabItem` 
		where docstatus = 0 and show_in_website = 1
		and (item_group in (%s)
			or name in (select parent from `tabWebsite Item Group` 
				where item_group in (%s))) """ % (child_groups, child_groups))[0][0]

def get_parent_item_groups(item_group_name):
	item_group = frappe.get_doc("Item Group", item_group_name)
	return frappe.db.sql("""select name, page_name from `tabItem Group`
		where lft <= %s and rgt >= %s 
		and ifnull(show_in_website,0)=1
		order by lft asc""", (item_group.lft, item_group.rgt), as_dict=True)
		
def invalidate_cache_for(bean, trigger, item_group=None):
	if not item_group:
		item_group = bean.name
	
	for i in get_parent_item_groups(item_group):
		if i.page_name:
			clear_cache(i.page_name)

def invalidate_cache_for_item(bean, trigger):
	invalidate_cache_for(bean, trigger, bean.item_group)
	for d in bean.doclist.get({"doctype":"Website Item Group"}):
		invalidate_cache_for(bean, trigger, d.item_group)
		
def update_website_page_name(bean, trigger):
	if bean.page_name:
		invalidate_cache_for_item(bean, trigger)
		clear_cache(bean.page_name)
