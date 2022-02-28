// Copyright (c) 2022, Shahzad Naser and contributors
// For license information, please see license.txt

frappe.ui.form.on('Pre Sales Order', {
	refresh: function(frm) {
		frm.set_query('item_code','items', function () {
			return {
			  filters: {
				  "has_variants": 1
			  }		  
		  }
		});
	}
});
