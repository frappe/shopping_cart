# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import webnotes
import webnotes.defaults
from webnotes.utils import cint

def set_cart_count(login_manager):
	if webnotes.conn.get_value("Profile", webnotes.session.user, "user_type") == "Website User":
		from shopping_cart.shopping_cart.cart import set_cart_count
		set_cart_count()
		
def clear_cart_count(login_manager):
	webnotes._response.set_cookie("cart_count", "")
	
def update_website_context(context):
	post_login = []
	cart_enabled = cint(webnotes.conn.get_default("shopping_cart_enabled"))
	context["shopping_cart_enabled"] = cart_enabled
	
	if cart_enabled:
		post_login += [
			{"label": "Cart", "url": "cart", "icon": "icon-shopping-cart", "class": "cart-count"},
			{"class": "divider"}
		]

	post_login += [
		{"label": "Profile", "url": "profile", "icon": "icon-user"},
		{"label": "Addresses", "url": "addresses", "icon": "icon-map-marker"},
		{"label": "My Orders", "url": "orders", "icon": "icon-list"},
		{"label": "My Tickets", "url": "tickets", "icon": "icon-tags"},
		{"label": "Invoices", "url": "invoices", "icon": "icon-file-text"},
		{"label": "Shipments", "url": "shipments", "icon": "icon-truck"},
		{"class": "divider"}
	]
	
	context["post_login"] = post_login + context.get("post_login", [])

