# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import webnotes
from shopping_cart.shopping_cart.product import get_product_list_for_group, \
	get_parent_item_groups, get_group_item_count

doctype = "Item Group"
condition_field = "show_in_website"

def get_context(controller, method):
	controller.doc.sub_groups = webnotes.conn.sql("""select name, page_name
		from `tabItem Group` where parent_item_group=%s
		and ifnull(show_in_website,0)=1""", controller.doc.name, as_dict=1)

	for d in controller.doc.sub_groups:
		d.count = get_group_item_count(d.name)
		
	controller.doc.items = get_product_list_for_group(product_group = controller.doc.name, limit=100)
	controller.parent_groups = get_parent_item_groups(controller.doc.name)
	controller.doc.title = controller.doc.name

	if controller.doc.slideshow:
		from webnotes.website.doctype.website_slideshow.website_slideshow import get_slideshow
		get_slideshow(controller)