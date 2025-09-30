@workspace I need to refactor the create_biological_vm() method in this BioXen-client to fix the workflow order and terminology.

PROBLEM: The current workflow shows "Select VM Type" first, then "Select Chassis" second. This should be reversed - chassis selection should come FIRST after the user chooses "Create Biological VM" from the main menu.

CORRECT WORKFLOW ORDER:
1. User selects "Create Biological VM" from main menu
2. FIRST: Select Chassis (E. coli, Yeast, Orthogonal) 
3. SECOND: Select VM Type (Basic, XCP-ng)
4. Get VM ID and create

SPECIFIC CHANGES NEEDED:
1. Move the "Select Chassis" section to come BEFORE "Select VM Type"
2. Update the print statements to show "Step 1: Select Chassis" and "Step 2: Select VM Type"
3. Keep all chassis choices and placeholder warnings exactly as they are
4. Keep all VM type choices and placeholder warnings exactly as they are
5. The final create_bio_vm(vm_id, biological_type, vm_type) call should use the chassis selection as biological_type
6. Update any display text to use "chassis" terminology for user-facing messages
7. Preserve all existing functionality, error handling, and VM management features

The goal is to make chassis selection the primary/first choice in the VM creation workflow, which better aligns with the biological focus of the system.