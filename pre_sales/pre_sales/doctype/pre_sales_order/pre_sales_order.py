# Copyright (c) 2022, Shahzad Naser and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class PreSalesOrder(Document):
	def on_update(self):
		self.make_sales_order()

	def make_sales_order(self):
		so = frappe.new_doc("Sales Order")
		if self.transaction_date:
			so.transaction_date = self.transaction_date

		so.company = self.company
		so.customer = self.customer
		so.pso = self.name
		items = False
		for item in self.items:
			if item.quarter and frappe.db.exists("Item",item.item_code+"-Quarter"):
				so.append("items", {
					"item_code": item.item_code+"-Quarter",
					"qty": item.quarter,
				})
				items = True
			if item.gallon and frappe.db.exists("Item",item.item_code+"-Gallon"):
				so.append("items", {
					"item_code": item.item_code+"-Gallon",
					"qty": item.gallon,
				})
				items = True

			if item.drum and frappe.db.exists("Item",item.item_code+"-Drum"):
				so.append("items", {
					"item_code": item.item_code+"-Drum",
					"qty": item.drum,
				})
				items = True

		so.delivery_date = self.delivery_date
		meta = frappe.get_meta("Sales Order")
		if meta.has_field('pre_sales_order'):
			so.pre_sales_order = self.name
		so.flags.ignore_permissions = True
		so.flags.ignore_mandatory = True
		so.set_missing_values(for_validate=True)
		if items:
			so.save()