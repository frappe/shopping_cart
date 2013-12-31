# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import webnotes

doctype = "Item"
condition_field = "show_in_website"

def get_context(controller, method):
	from erpnext.setup.doctype.item_group.item_group import get_parent_item_groups
	controller.parent_groups = get_parent_item_groups(controller.doc.item_group) + [{"name":controller.doc.name}]
	controller.doc.title = controller.doc.item_name

	if controller.doc.slideshow:
		from webnotes.website.doctype.website_slideshow.website_slideshow import get_slideshow
		get_slideshow(controller)