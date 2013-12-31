# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import webnotes

def get_context():
	return {
		"partners": webnotes.conn.sql("""select * from `tabSales Partner`
			where show_in_website=1 order by name asc""", as_dict=True),
	}