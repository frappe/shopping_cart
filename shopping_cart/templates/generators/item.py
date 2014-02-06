# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import webnotes
from shopping_cart.shopping_cart.product import get_parent_item_groups
from webnotes.website.doctype.website_slideshow.website_slideshow import get_slideshow
from webnotes.webutils import render_blocks

doctype = "Item"
condition_field = "show_in_website"

def get_context(context):
	bean = webnotes.bean(context.ref_doctype, context.docname)
	item_context = bean.doc.fields
	item_context.update({
		"parent_groups": get_parent_item_groups(bean.doc.item_group) + [{"name":bean.doc.name}],
		"title": bean.doc.item_name
	})
	if bean.doc.slideshow:
		item_group_context.update(get_slideshow(bean))
	item_context["obj"] = bean
	item_context.update(context)
	
	return render_blocks(item_context)
