# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TransactionTempShare(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		company: DF.Link | None
		department: DF.Link | None
		designation: DF.Link | None
		document_name: DF.DynamicLink | None
		document_type: DF.Link | None
		everyone_ch: DF.Check
		notify_by_email_ch: DF.Check
		read_ch: DF.Check
		share_ch: DF.Check
		submit_ch: DF.Check
		write_ch: DF.Check
	# end: auto-generated types
	pass
