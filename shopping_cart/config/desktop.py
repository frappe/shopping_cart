from __future__ import unicode_literals
from frappe import _

def get_data():
	return {
		"Shopping Cart": {
			"color": "#B7E090",
			"icon": "icon-shopping-cart",
			"label": _("Shopping Cart"),
			"link": "Form/Shopping Cart Settings",
			"type": "module"
		}
	}
