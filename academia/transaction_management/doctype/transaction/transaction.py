# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document


class Transaction(Document):
    def before_save(self):
        if self.outgoing:
            self.from_party = "Department"
            department = frappe.get_doc("Department", "Accounts")
            if department:
                self.from_department = department.name	
        if self.incoming:
            self.to_party = "Department"
            department = frappe.get_doc("Department", "Accounts")
            if department:
                self.to_department = department.name
    
        frappe.msgprint('here')
        for row in self.attachments:
            if not row.attachment_name:
                row.attachment_name = row.attachment_label.replace(" ", "_").lower() + "_file"
		   
           
@frappe.whitelist()
def get_associated_transactions(associated_transaction):
    linked_transactions = []
    get_linked_transactions(associated_transaction, linked_transactions)
    linked_transactions.reverse()  # Reverse the list to get the oldest transactions first
    return linked_transactions

def get_linked_transactions(associated_transaction, linked_transactions):
    transactions = frappe.get_all('Transaction',
                                  filters={'name': associated_transaction},
                                  fields=['*'],)

    if transactions:
        transaction = transactions[0]
        linked_transactions.append(transaction)
        associ_trans = transaction.get('associated_transaction')

        if associ_trans:
            get_linked_transactions(associ_trans, linked_transactions)