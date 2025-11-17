from . import __version__ as app_version

app_name = "electronic_invoice"
app_title = "electronic invoice"
app_publisher = "mariam"
app_description = "sales invoice with QRCode"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "eng.mariam87@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
jinja = {
    "methods": [
     	"electronic_invoice.events.accounts.printformat_utils.getTotalInWordsAr",
		"electronic_invoice.events.accounts.printformat_utils.getTotalInWordsEn",
      	"electronic_invoice.events.accounts.printformat_utils.formatDate"
   ]
}
# include js, css files in header of desk.html
# app_include_css = "/assets/electronic_invoice/css/electronic_invoice.css"
# app_include_js = "/assets/electronic_invoice/js/electronic_invoice.js"

# include js, css files in header of web template
# web_include_css = "/assets/electronic_invoice/css/electronic_invoice.css"
# web_include_js = "/assets/electronic_invoice/js/electronic_invoice.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "electronic_invoice/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
		"Sales Invoice" :"public/js/sales_invoice.js"
}
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "electronic_invoice.install.before_install"
# after_install = "electronic_invoice.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "electronic_invoice.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }
#override_doctype_class = {
#	"Num2Word_AR": "electronic_invoice.overrides.CustomNum2Word_AR"
#}

# Document Events
# ---------------
# Hook on document methods and events
doc_events = {
	"Stock Entry": {
		"validate": "electronic_invoice.utils.warehouse_items.stock_entry_check_warehouseItem"
	},
	"Material Request": {
		"validate": "electronic_invoice.utils.warehouse_items.material_request_check_warehouseItem"
	},
    "Sales Invoice": {
        "validate": ["electronic_invoice.events.accounts.sales_invoice.create_qr_code","electronic_invoice.events.accounts.sales_invoice.update_is_return_reason"],
        "on_trash": "electronic_invoice.events.accounts.sales_invoice.delete_qr_code_file",
    }
}
# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"electronic_invoice.tasks.all"
# 	],
# 	"daily": [
# 		"electronic_invoice.tasks.daily"
# 	],
# 	"hourly": [
# 		"electronic_invoice.tasks.hourly"
# 	],
# 	"weekly": [
# 		"electronic_invoice.tasks.weekly"
# 	]
# 	"monthly": [
# 		"electronic_invoice.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "electronic_invoice.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "electronic_invoice.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "electronic_invoice.task.get_dashboard_data"
# }


# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"electronic_invoice.auth.validate"
# ]

fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            ["name", "in",
             [
                 "Sales Invoice-additional_discount_percentage_added"
             ]
             ]
        ]
    }
]

