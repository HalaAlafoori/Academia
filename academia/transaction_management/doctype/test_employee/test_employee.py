# Copyright (c) 2024, SanU and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TestEmployee(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		company: DF.Link | None
		department: DF.Link | None
		designation: DF.Link | None
		employee_name: DF.Data | None
		user_id: DF.Data | None
	# end: auto-generated types
	pass


@frappe.whitelist()
def change_share_premission_to_new_user(new_designation, old_designation,new_department,old_department,new_company,old_company):
    user_id = get_employee_by_designation(new_designation,new_department,new_company)
    new_user = get_employee_by_designation(old_designation,old_department,old_company)
    if user_id and new_user:
         return get_user_share_permissions(user_id, new_user,new_designation,new_department,new_company)
    else:
        return None
    

# تعطينا اليوزر حسب المنصب
@frappe.whitelist()
def get_employee_by_designation(designation,department,company):
    employee = frappe.get_all(
        "Test Employee",
        filters={"designation": designation,"department":department,"company":company},
        fields=["user_id"],
    )
    if employee:
        user_id = employee[0].user_id
        # designation_empty = set_designation_empty(user_id)
        # return designation_empty
        return user_id
    else:
        return None


# تعطينا كل صلاحيات ال مشاركة الخاصة بيوزر معين، تنأكد ان المعاملة خاصة أولا، ثم نغير اليوزر الى اليوز الجديد
@frappe.whitelist()
def get_user_share_permissions(user_id, new_user,new_designation,new_department,new_company):
    #1- get old shares in Transaction Temp Share
     temp_docshares = frappe.get_all(
        "Transaction Temp Share",
        filters={"document_type": "Transaction","company": new_company, "department": new_department, "designation": new_designation},
        fields=["document_name", "read_ch","write_ch","share_ch","submit_ch","everyone_ch","notify_by_email_ch"]
    )
    # add share to docshare from temp_docshare
    #
    #
    #
    #
    #

    #2- get old position transactions and share with new
    new_docshares = frappe.get_all(
        "DocShare",
        filters={"share_doctype": "Transaction", "user": user_id,},
        fields=["name", "share_name"]
    )
    
	   
    # share_name: (document name) هو اسم المعاملة

    # هذه المصفوفات فقط للتأكد في console ولا نحتاجها في بناء العمل
    non_private_transactions = []
    share_names = []
    share_users = []
	
    if new_docshares:
        for docsh in new_docshares:
            is_non_private = get_non_private_transactions(docsh.share_name)
            if(is_non_private):
                #  change_user_of_share_permission(docsh.name, new_user)
                 non_private_transactions.append(docsh.share_name)
                 share_names.append(docsh.name)
                 share = frappe.get_doc("DocShare", docsh.name)
                 if(share):
                      share.user = new_user
                      share.save(ignore_permissions=True)
                      
                      share_users.append(share.user)
				 
	#3- Delete new shares and save details in temp share 
    old_docshares = frappe.get_all(
        "DocShare",
        filters={"share_doctype": "Transaction", "user": new_user,},
        fields=["name", "share_name"]
    ) 

   if old_docshares:
    for docsh in new_docshares:
        is_non_private = get_non_private_transactions(docsh.share_name)
        if is_non_private:
            share = frappe.get_doc("DocShare", docsh.name)
            if share:
                #save share details in temp share
                temp_share = frappe.new_doc("Transaction Temp Share")
                temp_share.company = share.document_type
                temp_share.department = share.document_type
                temp_share.designation = share.document_type
                temp_share.document_type = share.share_doctype
                temp_share.document_name = share.share_name
                temp_share.read_ch = share.read
                temp_share.write_ch = share.write
                temp_share.share_ch = share.share
                temp_share.submit_ch = share.submit_ch
                temp_share.everyone_ch = share.everyone
                temp_share.notify_by_email_ch = share.notify_by_email
                temp_share.save()


                #delete share
                frappe.delete_doc("DocShare", docsh.name)
	 

	      
            
        return user_id,non_private_transactions, share_names, share_users, new_user

#  تتأكد من ان المعاملة خاصة ام لا
@frappe.whitelist()
def get_non_private_transactions(transaction_name):
     
     transaction = frappe.get_doc("Transaction", transaction_name)
     if(transaction.private):
          return True
     else:
          return False
     



#  this function is not used
@frappe.whitelist()
def set_designation_empty(user_id):
    employees = frappe.get_all(
        "Test Employee",
        filters={"user_id": user_id},
    )
    if employees:
        docname = employees[0].name
        test_emp = frappe.get_doc("Test Employee", docname)
        if(test_emp):
             test_emp.designation = None
             test_emp.save()
             return "Designation Has Emptied"
        else:
             return "No Test Employee"
    else:
        return "No employee found with the given user_id"

    