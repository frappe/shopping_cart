# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import webnotes
from shopping_cart.shopping_cart.product import get_product_list_for_group, \
	get_parent_item_groups, get_group_item_count
from webnotes.webutils import render_blocks
from webnotes.website.doctype.website_slideshow.website_slideshow import get_slideshow

doctype = "Item Group"
condition_field = "show_in_website"

def get_context(context):
	bean = webnotes.bean(context.ref_doctype, context.docname)
	item_group_context = bean.doc.fields
	item_group_context.update({
		"sub_groups": webnotes.conn.sql("""select name, page_name
			from `tabItem Group` where parent_item_group=%s
			and ifnull(show_in_website,0)=1""", context.docname, as_dict=1),
		"items": get_product_list_for_group(product_group = context.docname, limit=100),
		"parent_groups": get_parent_item_groups(context.docname),
		"title": context.docname
	})
	
	if bean.doc.slideshow:
		item_group_context.update(get_slideshow(bean))
	
	for d in item_group_context.sub_groups:
		d.count = get_group_item_count(d.name)
	
	item_group_context.update(context)
	
	return render_blocks(item_group_context)