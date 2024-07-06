// Copyright (c) 2024, SanU and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transaction Action", {
    transaction: function (frm) {
        // if(frm.doc.transaction)
        //     // console.log(frm.doc.transaction);
        // frappe.call({
        //     method: "frappe.client.get_list",
        //     args: {
        //       doctype: "Transaction",
        //       filters: { 
        //             name: frm.doc.transaction , 
        //         },
        //       fields: [
        //         "transaction_scope", 
        //         "company",
        //         "department", 
        //         "designation", 
        //     ]
        //     },
        //     callback: (response) => {
        //         var main_transaction = response.message
        //     }
        // });
    },

    // Advance Get members Dialog
    get_recipients: function (frm) {
      var all_companies = frm.doc.transaction_scope === "Among Companies";
      var setters = {
        employee_name: null,
        department: null,
        designation: null
      };
    
      if (all_companies) {
        setters.company = null;
      }
    
      let existingRecipients = frm.doc.recipients || [];
      let existingRecipientIds = existingRecipients.map(r => r.recipient_email);
    
      frappe.call({
        method: "academia.transaction_management.doctype.transaction_action.transaction_action.get_recipients",
        args: {
          transaction_name: frm.doc.transaction,
        },
        callback: function(response) {
          var recipientEmails = response.message;
          if (recipientEmails && recipientEmails.length > 0) {
            // Add recipient emails from transaction actions to existingRecipientIds
            existingRecipientIds.push(...recipientEmails);
          }
    
          // Add the current user to the existing recipient IDs
          existingRecipientIds.push(frappe.session.user);
    
          new frappe.ui.form.MultiSelectDialog({
            doctype: "Employee",
            target: frm,
            setters: setters,
    
            // add_filters_group: 1,
            date_field: "transaction_date",
    
            get_query() {
              let filters = {
                docstatus: ['!=', 2],
                department: ['!=', null],
                designation: ['!=', null],
                user_id: ['not in', existingRecipientIds], // don't show Employee of current user
              };
    
              if (!all_companies) {
                filters.company = frm.doc.company;
              }
    
              return {
                filters: filters
              };
            },
    
            primary_action_label: "Get Recipients",
            action(selections) {
              // Fetch the selected employees with specific fields
              frappe.call({
                method: "frappe.client.get_list",
                args: {
                  doctype: "Employee",
                  filters: { name: ["in", selections] },
                  fields: ["employee_name", "designation", "department", "company", "user_id"]
                },
                callback: (response) => {
                  var selectedEmployees = response.message;
    
                  // Clear existing recipients
                  frm.doc.recipients = [];
    
                  selectedEmployees.forEach((employee) => {
                    frm.add_child("recipients", {
                      recipient_name: employee.employee_name,
                      recipient_company: employee.company,
                      recipient_department: employee.department,
                      recipient_designation: employee.designation,
                      recipient_email: employee.user_id,
                      // member_role: "Council Member"
                    })
                  })
    
                  // Refresh recipients field
                  frm.refresh_field("recipients");
    
                  this.dialog.hide();
                }
              });
            }
          });
        }
      });
    },

    clear_recipients: function(frm) {
      frm.clear_table("recipients");
      frm.refresh_field("recipients");
    },
    refresh:
    function(frm) {
    if(frappe.session.user !== "Administrator"){

      frappe.call({
        method: "academia.transaction_management.doctype.transaction.transaction_action.get_next_through_route",
        args: {
          
        },
        callback: function(response) {
          
          
        }
      });


    }}

    



});