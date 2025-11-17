// Copyright (c) 2023, mariam and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["VanSales Report"] = {
	"filters": [
		{
			"fieldname":"group_by",
			"label": __("Doc Type"),
			"fieldtype": "Select",
			"options": "Sales Invoice\nPayment Entry",
			"default": "Sales Invoice",
			// on_change: function() {
			// 	let group_by = frappe.query_report.get_filter_value('group_by');
			// 	//frappe.query_report.toggle_filter_display('customer_group_list', group_by !== 'Customer Group');
			// 	frappe.query_report.refresh();
			// }
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"owner",
			"label": __("Owner"),
			"fieldtype": "Link",
			"options": "User"
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"mode_of_payment",
			"label": __("Mode of Payment"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Mode of Payment', txt);
			},
			//"options": "Mode of Payment"
		},

	]
};
