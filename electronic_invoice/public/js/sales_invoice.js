// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
erpnext.sales_common.setup_selling_controller();
// frappe.provide("erpnext.accounts");

frappe.ui.form.on("Sales Invoice", {
    /*refresh: function (frm) {
        var me = this;
        if (!frm.doc.qr_code_data) {
            $(frm.fields_dict['qr_code'].wrapper).html('');
        }

        if (frm.doc.qr_code_data) {
            // let qrcode = <img src='data:image/svg+xml;base64,${qrcode_code}'  style='width:30%;padding:10px;float:left;'>
            let qrcode = `<div><img src='data:image/svg+xml;base64,${frm.doc.qr_code_data}' style='width:200px;height:200px;display:block;'></div>`
            $(frm.fields_dict['qr_code'].wrapper).html(qrcode);
        }

    }*/
    discount_amount: function (frm){
        var apply_discount_on = frm.doc.apply_discount_on
        var discount_amount = frm.doc.discount_amount
        var additional_discount_percentage_added
        var grand_total = frm.doc.grand_total
        var net_total = frm.doc.net_total
        if(apply_discount_on == 'Grand Total'){
            additional_discount_percentage_added = flt(flt(discount_amount/grand_total)*100)
        }else if (apply_discount_on == 'Net Total'){
            additional_discount_percentage_added = flt(flt(discount_amount/net_total)*100)
        }
        frm.set_value('additional_discount_percentage_added',additional_discount_percentage_added);
    }

})