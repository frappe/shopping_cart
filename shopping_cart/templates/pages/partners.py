# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import webnotes
import webnotes.webutils

def get_context(context):
	partner_context = {
		"partners": webnotes.conn.sql("""select * from `tabSales Partner`
			where show_in_website=1 order by name asc""", as_dict=True),
		"title": "Partners"
	}
	partner_context.update(context)
	return webnotes.webutils.render_blocks(partner_context)
	
def clear_cache(bean, trigger):
	if bean.doc.page_name:
		webnotes.webutils.clear_cache("partners")
	