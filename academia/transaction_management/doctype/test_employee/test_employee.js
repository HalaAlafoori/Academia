// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Test Employee", {
// 	refresh(frm) {

// 	},
// });



let previousDesignation = null;
let previousDepartment = null;
let previousCompany = null;


frappe.ui.form.on("Test Employee", {

    refresh: function(frm) {
        // متغير سنحفظ فيه المنصب السابق
 previousDesignation = null;
 previousDepartment = null;
 previousCompany = null;
        if(frm.doc.designation)
            previousDesignation = frm.doc.designation;

        if(frm.doc.department)
            previousDepartment = frm.doc.department;
        if(frm.doc.company)
            previousCompany = frm.doc.department;
        // frappe.msgprint(previousDesignation)

    },
	
    designation: function(frm){
       
    },

    before_save: function(frm) {
        if(previousDesignation || previousDepartment || previousCompany ){
            // المنصب الجديد
            let currentDesignation = frm.doc.designation
            let currentDepartment = frm.doc.department
            let currentCompany = frm.doc.company

            // Log the previous and current designation values
            console.log("Previous Designation:", previousDesignation);
            console.log("Current Designation:", currentDesignation);
            console.log("Previous Department:", previousDepartment);
            console.log("Current Department:", currentDepartment);
            console.log("Previous Company:", previousCompany);
            console.log("Current Company:", currentCompany);

            // نتأكد أن المنصب تغير قبل الدخول في دالة تغيير الصلاحية
            if((previousDesignation !== currentDesignation && currentDesignation) || (previousDepartment!== currentDepartment && currentDepartment) || (previousCompany!== currentCompany && currentCompany)){
            console.log("change");
            frappe.call({
                method: "academia.transaction_management.doctype.test_employee.test_employee.change_share_premission_to_new_user",
                    args: {
                        new_designation: currentDesignation,
                        old_designation: previousDesignation,
                        new_department: currentDepartment,
                        old_department: previousDepartment,
                        new_company:currentCompany,
                        old_company:previousCompany
                    },
                    callback: function(response) {
                        if(response.message)
                        {
                            console.log("message: ", r.message);
                        }
                    }
                });
            }
            else{
                console.log("No change");
            }

        }
    }

});

