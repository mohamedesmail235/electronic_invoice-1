# Copyright (c) 2023, mariam and contributors
# For license information, please see license.txt

import frappe
from frappe import _, _dict
from frappe.utils import cstr
from erpnext import get_company_currency, get_default_company

def execute(filters=None):
	columns, data = [], []
	validate_filters(filters)
	columns = get_columns(filters)
	#conditions = get_conditions(filters)
	data = get_result(filters)#,conditions
	return columns, data

def validate_filters(filters):
	if not filters.get("company"):
		frappe.throw(_("{0} is mandatory").format(_("Company")))

	if not filters.get("from_date") and not filters.get("to_date"):
		frappe.throw(
			_("{0} and {1} are mandatory").format(frappe.bold(_("From Date")), frappe.bold(_("To Date")))
		)

	if filters.from_date > filters.to_date:
		frappe.throw(_("From Date must be before To Date"))

def get_conditions(filters):
	conditions = []

	if filters.get("company"):
		conditions.append(" company=%(company)s")
	conditions.append(" (posting_date <=%(to_date)s )") #or is_opening = 'Yes'

	if filters.get("mode_of_payment"):
		if filters.get("group_by") == 'Sales Invoice':
			conditions.append(" exists(select name from `tabSales Invoice Payment` where parent=`tabSales Invoice`.name	and ifnull(`tabSales Invoice Payment`.mode_of_payment, '') in %(mode_of_payment)s)")
		elif filters.get("group_by") == 'Payment Entry':
			conditions.append(" mode_of_payment in %(mode_of_payment)s")

	if filters.get("from_date"):
		conditions.append(" posting_date >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append(" posting_date <= %(to_date)s")

	if filters.get("owner"):
		conditions.append(" owner = %(owner)s")

	return "and {}".format(" and ".join(conditions)) if conditions else ""

def get_columns(filters):
	if filters.get("company"):
		currency = get_company_currency(filters["company"])
	else:
		company = get_default_company()
		currency = get_company_currency(company)
	columns = [
		{
			"label": _("Invoice"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": filters.get('group_by'),
			"width": 170,
		},
		{"label": _("Posting Date"), "fieldname": "posting_date", "fieldtype": "Date", "width": 110},
		{
			"label": _("Owner"),
			"fieldname": "owner",
			"fieldtype": "Link",
			"options": "User",
			"width": 150,
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150,
		},

		{
			"label": _("Mode Of Payment"),
			"fieldname": "mode_of_payment",
			"fieldtype": "Data",
			"width": 190,
		},
		{
			"label": _("Paid Amount ({0})").format(currency),
			"fieldname": "paid_amount",
			"fieldtype": "Float",
			"width": 130,
		}]
	if filters.get("group_by")=='Sales Invoice':
		columns.append({
			"label": _("Grand Total ({0})").format(currency),
			"fieldname": "grand_total",
			"fieldtype": "Float",
			"width": 130,
		})
	return columns


def get_result(filters):
	data = []
	invoice_list = get_invoices(filters)
	if filters.get("group_by") == 'Sales Invoice':
		mode_of_payments = get_mode_of_payments([inv.name for inv in invoice_list])
	invoice_data = get_invoices(filters)
	for inv in invoice_data:
		#owner_posting_date = inv["name"]
		if filters.get("group_by") == 'Sales Invoice':
			row = [inv.name,inv.posting_date, inv.owner,inv.customer,", ".join(mode_of_payments.get(inv.name, []),),inv.paid_amount,inv.grand_total]
		elif filters.get("group_by") == 'Payment Entry':
			row = [inv.name, inv.posting_date, inv.owner, inv.customer,inv.mode_of_payment, inv.paid_amount]#, inv.grand_total
		data.append(row)

	return data
def get_mode_of_payments(invoice_list):
	mode_of_payments = {}
	if invoice_list:
		inv_mop = frappe.db.sql("""select parent, mode_of_payment
			from `tabSales Invoice Payment` where parent in (%s) group by parent, mode_of_payment""" %
			', '.join(['%s']*len(invoice_list)), tuple(invoice_list), as_dict=1)

		for d in inv_mop:
			mode_of_payments.setdefault(d.parent, []).append(d.mode_of_payment)

	return mode_of_payments

# def get_mode_of_payments(filters):
# 	mode_of_payments = {}
# 	invoice_list = get_invoices(filters)
# 	invoice_list_names = ",".join('"' + invoice['name'] + '"' for invoice in invoice_list)
# 	print(invoice_list_names)
# 	if invoice_list:
# 		if filters.get("group_by") == 'Sales Invoice':
# 			inv_mop = frappe.db.sql("""select a.name as pname, a.owner,a.posting_date, ifnull(b.mode_of_payment, '') as mode_of_payment
# 				from `tabSales Invoice` a, `tabSales Invoice Payment` b
# 				where a.name = b.parent
# 				and a.docstatus = 1
# 				and a.name in ({invoice_list_names})
# 				""".format(invoice_list_names=invoice_list_names), as_dict=1)
# 			for d in inv_mop:
# 				mode_of_payments.setdefault(d["pname"]+ d["owner"] + cstr(d["posting_date"]), []).append(d.mode_of_payment)
# 		# elif filters.get("group_by") == 'Payment Entry':
# 		# 	inv_mop = frappe.db.sql("""select a.name,a.owner,a.posting_date, ifnull(a.mode_of_payment, '') as mode_of_payment
# 		# 		from `tabPayment Entry` a
# 		# 		where a.name in ({invoice_list_names})
# 		# 		and a.docstatus = 1
# 		# 		""".format(invoice_list_names=invoice_list_names), as_dict=1)
# 		# 	for d in inv_mop:
# 		# 		mode_of_payments.setdefault(d["owner"] + cstr(d["posting_date"]), []).append(d.mode_of_payment)
# 	return mode_of_payments

def get_invoices(filters):
	if filters.get("group_by") == 'Sales Invoice':
		invs =  frappe.db.sql("""
					SELECT * 
					from `tabSales Invoice`
					WHERE is_pos=1
					and docstatus = 1
					{conditions}
					""".format(conditions=get_conditions(filters)),
			filters,
			as_dict=1,
		)
	elif filters.get("group_by") == 'Payment Entry':
		invs = frappe.db.sql("""
					SELECT * ,party as customer
					from `tabPayment Entry`
					WHERE payment_type = 'Receive'
					and docstatus = 1
					{conditions}
					""".format(conditions=get_conditions(filters)),
			filters,
			as_dict=1,
		)
	return invs
