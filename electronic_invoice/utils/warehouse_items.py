# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
from frappe.utils import flt, get_link_to_form
from frappe import _
import frappe


def stock_entry_check_warehouseItem(doc, method):
    #print(frappe.conf.db_name)
    chkTableExist = frappe.db.sql("""SELECT COUNT( 'tabWarehouse Items')
		FROM 
		   information_schema.TABLES 
		WHERE 
		   TABLE_SCHEMA LIKE '{0}' AND 
			TABLE_NAME = 'tabWarehouse Items'""".format(frappe.conf.db_name))[0][0]
    if chkTableExist:
        if (doc.stock_entry_type == 'Material Transfer'):
            for item in doc.items:
                chkWarehouseItemsExist = frappe.db.sql("""SELECT COUNT(*)
						FROM 
						   `tabWarehouse Items`
						WHERE 
						   parent='{0}'""".format(item.t_warehouse))[0][0]
                #print(chkWarehouseItemsExist)
                if chkWarehouseItemsExist:
                    itemWarehouseQty = frappe.db.get_value("Warehouse Items",
                                                           dict(parent=item.t_warehouse, item_code=item.item_code,
                                                                uom=item.uom), "qty")
                    #print(itemWarehouseQty)
                    if (itemWarehouseQty):
                        if (itemWarehouseQty < flt(item.transfer_qty)):
                            frappe.throw(
                                _("Item {0} quantity is more than item quantity recorded in warehouse {1} ").format(
                                    item.item_code, item.t_warehouse))
                    else:
                        frappe.throw(
                            _("Item {0} isn't recorded in warehouse {1}").format(item.item_code, item.t_warehouse))


def material_request_check_warehouseItem(doc, method):
    #print(frappe.conf.db_name)
    chkTableExist = frappe.db.sql("""SELECT COUNT( 'tabWarehouse Items')
			FROM 
			   information_schema.TABLES 
			WHERE 
			   TABLE_SCHEMA = '{0}' AND 
			TABLE_NAME = 'tabWarehouse Items'""".format(frappe.conf.db_name))[0][0]
    if chkTableExist:
        if (doc.material_request_type == 'Material Transfer'):
            for item in doc.items:
                chkWarehouseItemsExist = frappe.db.sql("""SELECT COUNT(*)
					FROM 
					   `tabWarehouse Items`
					WHERE 
					   parent='{0}'""".format(item.warehouse))[0][0]
                #print(chkWarehouseItemsExist)
                if chkWarehouseItemsExist:
                    itemWarehouseQty = frappe.db.get_value("Warehouse Items",
                                                           dict(parent=item.warehouse, item_code=item.item_code,
                                                                uom=item.stock_uom), "qty")
                    #print(itemWarehouseQty)
                    if (itemWarehouseQty):
                        if (itemWarehouseQty < flt(item.stock_qty)):
                            frappe.throw(
                                _("Item {0} quantity is more than item quantity recorded in warehouse {1} ").format(
                                    item.item_code, item.warehouse))
                    else:
                        frappe.throw(
                            _("Item {0} isn't recorded in warehouse {1}").format(item.item_code, item.warehouse))
