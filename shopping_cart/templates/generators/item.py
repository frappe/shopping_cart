# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
from shopping_cart.shopping_cart.product import get_parent_item_groups
from frappe.website.doctype.website_slideshow.website_slideshow import get_slideshow

doctype = "Item"
condition_field = "show_in_website"

def get_context(context):
	item_context = context.bean.doc.fields
	item_context["parent_groups"] = get_parent_item_groups(context.bean.doc.item_group) + \
		[{"name":context.bean.doc.name}]
	if context.bean.doc.slideshow:
		item_group_context.update(get_slideshow(context.bean))
	
	return item_context
