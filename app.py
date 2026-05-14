import streamlit as st
import pandas as pd
from database import AllotmentDatabase
from document_generator import AllotmentDocumentGenerator
from datetime import datetime
import os
import json
import shutil

# Initialize database and document generator
db = AllotmentDatabase()
doc_gen = AllotmentDocumentGenerator()

# Page configuration
st.set_page_config(
    page_title="Real Estate Allotment System",
    page_icon="🏢",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 1rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🏢 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "➕ New Project", "📝 New Allotment", "📊 Dashboard", "❌ Manage Allotments"]
)

# HOME PAGE
if page == "🏠 Home":
    st.markdown('<h1 class="main-header">🏢 Real Estate Allotment Automation System</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Welcome to the Allotment Management System
    
    This system helps you automate the creation and management of property allotment letters for your real estate projects.
    
    #### 🎯 Key Features:
    - ✅ **Project Management**: Create and manage multiple building projects
    - ✅ **Automated Allotment Letters**: Generate professional allotment letters in DOCX format
    - ✅ **Sequential Numbering**: Automatic allotment number generation with financial year
    - ✅ **Smart Reassignment**: Automatically reassign cancelled allotments when possible
    - ✅ **Freeze/Unfreeze**: Handle client backouts with freeze functionality
    - ✅ **Multiple Allottees**: Support for multiple allottees per unit
    - ✅ **Parking Management**: Detailed parking allocation tracking
    - ✅ **Dashboard**: View and manage all allotments in one place
    
    #### 📋 Quick Start:
    1. **Create a New Project** - Set up your building/project details
    2. **Issue Allotment** - Create allotment letters for clients
    3. **Manage** - View, freeze, or cancel allotments as needed
    
    ---
    
    #### 📊 System Statistics:
    """)
    
    # Display statistics
    projects = db.get_all_projects()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Projects", len(projects))
    
    with col2:
        total_allotments = 0
        for project in projects:
            allotments = db.get_allotments_by_project(project[0])
            total_allotments += len(allotments)
        st.metric("Total Allotments", total_allotments)
    
    with col3:
        active_count = 0
        for project in projects:
            allotments = db.get_allotments_by_project(project[0])
            active_count += len([a for a in allotments if a[22] == 'Issued'])
        st.metric("Active Allotments", active_count)

# NEW PROJECT PAGE
elif page == "➕ New Project":
    st.markdown('<h1 class="main-header">➕ Create New Project</h1>', unsafe_allow_html=True)
    
    with st.form("new_project_form"):
        st.markdown("### 🏗️ Project Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name *", placeholder="e.g., NEW ASHWIN CHSL / OSSIA CREST")
            mahrera_no = st.text_input("MahaRERA Registration No *", placeholder="e.g., P51800053401")
            survey_no = st.text_input("Survey No.", placeholder="e.g., Survey No. 23")
            hissa_no = st.text_input("Hissa No.", placeholder="e.g., Hissa No. 1/A (Pt.)")
            cts_no = st.text_input("CTS No.", placeholder="e.g., CTS No. 333A/1")
        
        with col2:
            final_plot_no = st.text_input("Final Plot No.", placeholder="e.g., Final Plot No. 222-223")
            tps_details = st.text_input("TPS Details", placeholder="e.g., TPS III, New Final Plot No. 253")
            plot_area = st.text_input("Plot Area", placeholder="e.g., 1138.80 sq. mtrs")
            location = st.text_input("Location *", placeholder="e.g., Borivali West, Mumbai 400 091")
            total_podiums = st.number_input(
                "Total Number of Podiums *",
                min_value=0, max_value=50, value=0, step=1,
                help="Number of podium levels in this building (e.g., 6). Used to populate parking podium options on allotment."
            )
        
        st.markdown("### 🏢 Promoter Information")
        
        col3, col4 = st.columns(2)
        
        with col3:
            promoter_company = st.text_input("Promoter Company Name *", placeholder="e.g., OSSIA BUILDCON PRIVATE LIMITED")
            promoter_account_name = st.text_input("Account Name *", placeholder="e.g., OSSIA BUILDCON PRIVATE LIMITED")
            promoter_account_no = st.text_input("Account Number *", placeholder="e.g., 615011013334")
        
        with col4:
            promoter_bank_name = st.text_input("Bank Name *", placeholder="e.g., KOTAK MAHINDRA BANK")
            promoter_branch = st.text_input("Branch Name *", placeholder="e.g., CHANDAVARKAR ROAD, BORIVALI WEST")
            promoter_ifsc = st.text_input("IFSC Code *", placeholder="e.g., KKBK0000653")
        
        st.markdown("### 📋 Cancellation Policy")
        st.info("Configure the cancellation charges for different time periods")
        
        # Cancellation table
        st.markdown("#### Cancellation Charges Table")
        
        cancellation_data = []
        
        col_a, col_b = st.columns(2)
        with col_a:
            period1 = st.text_input("Period 1", value="within 15 days from issuance of the allotment letter;")
        with col_b:
            deduction1 = st.text_input("Deduction 1", value="Nil")
        cancellation_data.append({"period": period1, "deduction": deduction1})
        
        col_c, col_d = st.columns(2)
        with col_c:
            period2 = st.text_input("Period 2", value="within 16 to 30 days from issuance of the allotment letter;")
        with col_d:
            deduction2 = st.text_input("Deduction 2", value="1% of the cost of the said unit;")
        cancellation_data.append({"period": period2, "deduction": deduction2})
        
        col_e, col_f = st.columns(2)
        with col_e:
            period3 = st.text_input("Period 3", value="within 31 to 60 days from issuance of the allotment letter;")
        with col_f:
            deduction3 = st.text_input("Deduction 3", value="1.5 % of the cost of the said unit;")
        cancellation_data.append({"period": period3, "deduction": deduction3})
        
        col_g, col_h = st.columns(2)
        with col_g:
            period4 = st.text_input("Period 4", value="after 61 days from issuance of the allotment letter")
        with col_h:
            deduction4 = st.text_input("Deduction 4", value="2% of the cost of the said unit.")
        cancellation_data.append({"period": period4, "deduction": deduction4})
        
        submitted = st.form_submit_button("Create Project", type="primary", use_container_width=True)
        
        if submitted:
            if not project_name or not mahrera_no or not location or not promoter_company:
                st.error("Please fill all required fields marked with *")
            else:
                project_data = {
                    'project_name': project_name,
                    'mahrera_no': mahrera_no,
                    'survey_no': survey_no,
                    'hissa_no': hissa_no,
                    'cts_no': cts_no,
                    'final_plot_no': final_plot_no,
                    'tps_details': tps_details,
                    'plot_area': plot_area,
                    'location': location,
                    'promoter_company': promoter_company,
                    'promoter_bank_name': promoter_bank_name,
                    'promoter_account_name': promoter_account_name,
                    'promoter_account_no': promoter_account_no,
                    'promoter_branch': promoter_branch,
                    'promoter_ifsc': promoter_ifsc,
                    'cancellation_table': cancellation_data,
                    'total_podiums': total_podiums
                }
                
                project_id, project_code = db.add_project(project_data)
                
                st.success(f"✅ Project created successfully!")
                st.info(f"📁 Project Code: **{project_code}**")
                st.info(f"📂 Folder created at: **Allotment_Letters/{project_name}**")

    st.markdown("---")
    st.markdown("### 🗑️ Delete Project")

    existing_projects = db.get_all_projects()
    if not existing_projects:
        st.caption("No projects to delete yet.")
    else:
        delete_options = {f"{p[1]} ({p[2]})": p for p in existing_projects}
        selected_label = st.selectbox(
            "Select project to delete",
            options=list(delete_options.keys()),
            key="delete_project_select",
        )
        selected_row = delete_options[selected_label]
        selected_project_id = selected_row[0]
        selected_project_name = selected_row[1]

        existing_allotments = db.get_allotments_by_project(selected_project_id)
        folder_path = os.path.join("Allotment_Letters", selected_project_name)

        st.warning(
            f"This will permanently delete **{selected_project_name}** along with "
            f"**{len(existing_allotments)}** allotment(s) and their allottee records."
        )

        delete_files = st.checkbox(
            f"Also delete generated documents folder (`{folder_path}`)",
            key="delete_files_checkbox",
        )
        confirm = st.checkbox(
            f"I understand this cannot be undone. Delete '{selected_project_name}'.",
            key="delete_confirm_checkbox",
        )

        if st.button(
            "🗑️ Delete Project Permanently",
            type="secondary",
            disabled=not confirm,
            use_container_width=True,
        ):
            name, n = db.delete_project(selected_project_id)
            files_msg = ""
            if delete_files and os.path.isdir(folder_path):
                try:
                    shutil.rmtree(folder_path)
                    files_msg = f" Folder '{folder_path}' removed."
                except OSError as e:
                    files_msg = f" Could not remove folder: {e}"
            st.success(f"✅ Deleted project '{name}' and {n} allotment(s).{files_msg}")
            st.rerun()

# NEW ALLOTMENT PAGE
elif page == "📝 New Allotment":
    st.markdown('<h1 class="main-header">📝 Create New Allotment</h1>', unsafe_allow_html=True)
    
    # Initialize session state for download
    if 'last_generated_file' not in st.session_state:
        st.session_state.last_generated_file = None
    if 'last_generated_filename' not in st.session_state:
        st.session_state.last_generated_filename = None
    
    # Select project
    projects = db.get_all_projects()
    
    if not projects:
        st.warning("⚠️ No projects found. Please create a project first.")
    else:
        project_options = {f"{p[1]} ({p[2]})": p[0] for p in projects}
        selected_project = st.selectbox("Select Project *", options=list(project_options.keys()))
        project_id = project_options[selected_project]
        
        # Get project details
        project_data = db.get_project_by_id(project_id)
        
        # Get next allotment number
        allotment_number, sequence, fy = db.get_next_allotment_number(project_id)
        
        st.info(f"📋 Next Allotment Number: **{allotment_number}**")

        # Parking section is OUTSIDE st.form so cascading selections trigger reruns.
        # Project's total_podiums lives at the end of the projects row.
        project_total_podiums = int(project_data[-1] or 0)

        st.markdown("### 🚗 Parking Information")
        parking_required = st.radio(
            "Parking Required? *", ["No", "Yes"], horizontal=True, key="parking_required"
        )

        parking_type = ""
        parking_size = ""
        parking_location = ""
        parking_ready = True

        if parking_required == "Yes":
            parking_type = st.radio(
                "Parking Type *", ["Stack", "Surface"],
                horizontal=True, index=None, key="parking_type",
            )

            if parking_type:
                parking_size = st.radio(
                    "Parking Size *", ["Big", "Small"],
                    horizontal=True, index=None, key="parking_size",
                )

                if parking_size:
                    if project_total_podiums > 0:
                        podium_options = [f"Podium {i + 1}" for i in range(project_total_podiums)]
                        parking_location = st.selectbox(
                            "Podium *", options=podium_options,
                            index=None, placeholder="Select Podium", key="parking_podium",
                        )
                        parking_ready = parking_location is not None
                    else:
                        st.warning(
                            "⚠️ This project has 0 podiums configured. "
                            "Edit the project and set 'Total Number of Podiums' to enable podium selection."
                        )
                        parking_ready = False
                else:
                    parking_ready = False
            else:
                parking_ready = False

        with st.form("new_allotment_form"):
            st.markdown("### 🏠 Unit Information")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                unit_type = st.selectbox("Unit Type *", ["Shop", "Flat", "Office"])
                unit_number = st.text_input("Unit Number *", placeholder="e.g., 4")
                floor = st.text_input("Floor *", placeholder="e.g., Ground floor")
            
            with col2:
                wing = st.text_input("Wing *", placeholder="e.g., A wing")
                carpet_area_sqm = st.number_input("Carpet Area (sq.mtrs) *", min_value=0.0, step=0.01)
                carpet_area_sqft = st.number_input("Carpet Area (sq.ft) *", min_value=0.0, step=1.0)
            
            with col3:
                total_consideration = st.number_input("Total Consideration (Rs) *", min_value=0.0, step=1000.0)
                gst_amount = st.number_input("GST Amount (Rs) *", min_value=0.0, step=1000.0)
                booking_amount = st.number_input("Booking Amount Paid (Rs) *", min_value=0.0, step=1000.0)
            
            possession_date = st.date_input("Possession Date *")

            st.markdown("### 👥 Allottee Information")
            
            num_allottees = st.number_input("Number of Allottees *", min_value=1, max_value=5, value=1, step=1)
            
            allottees_data = []
            
            for i in range(int(num_allottees)):
                st.markdown(f"#### Allottee {i+1}")
                
                col7, col8 = st.columns(2)
                
                with col7:
                    name = st.text_input(f"Full Name {i+1} *", key=f"name_{i}", placeholder="e.g., MISS. KAVYA HARISH SUVARNA")
                    phone = st.text_input(f"Phone Number {i+1} *", key=f"phone_{i}", placeholder="e.g., +91 9820811207")
                    pan_card = st.text_input(f"PAN Card {i+1} *", key=f"pan_{i}", placeholder="e.g., ISUPS7785A")
                    aadhar_card = st.text_input(f"Aadhar Card {i+1} *", key=f"aadhar_{i}", placeholder="e.g., 9100 0030 8556")
                
                with col8:
                    address = st.text_area(f"Address {i+1} *", key=f"address_{i}", placeholder="Enter full address")
                    email = st.text_input(f"Email {i+1}", key=f"email_{i}", placeholder="e.g., email@example.com")
                
                st.markdown(f"##### Bank Details - Allottee {i+1}")
                
                col9, col10 = st.columns(2)
                
                with col9:
                    account_name = st.text_input(f"Account Name {i+1} *", key=f"acc_name_{i}")
                    account_no = st.text_input(f"Account Number {i+1} *", key=f"acc_no_{i}")
                    bank_name = st.text_input(f"Bank Name {i+1} *", key=f"bank_{i}")
                
                with col10:
                    branch = st.text_input(f"Branch {i+1} *", key=f"branch_{i}")
                    ifsc = st.text_input(f"IFSC Code {i+1} *", key=f"ifsc_{i}")
                
                allottees_data.append({
                    'name': name,
                    'address': address,
                    'phone': phone,
                    'pan_card': pan_card,
                    'aadhar_card': aadhar_card,
                    'email': email,
                    'account_name': account_name,
                    'account_no': account_no,
                    'bank_name': bank_name,
                    'branch': branch,
                    'ifsc': ifsc
                })
            
            submitted = st.form_submit_button("Generate Allotment Letter", type="primary", use_container_width=True)
            
            if submitted:
                # Validate required fields
                if not unit_number or not floor or not wing or carpet_area_sqm <= 0:
                    st.error("Please fill all required unit information fields")
                elif not all([a['name'] and a['phone'] and a['pan_card'] for a in allottees_data]):
                    st.error("Please fill all required allottee information fields")
                elif parking_required == "Yes" and not parking_ready:
                    st.error("Please complete the parking selection (type → size → podium) above the form.")
                else:
                    # Prepare allotment data
                    allotment_data = {
                        'project_id': project_id,
                        'allotment_number': allotment_number,
                        'allotment_sequence': sequence,
                        'financial_year': fy,
                        'unit_type': unit_type,
                        'unit_number': unit_number,
                        'floor': floor,
                        'wing': wing,
                        'carpet_area_sqm': carpet_area_sqm,
                        'carpet_area_sqft': carpet_area_sqft,
                        'total_consideration': total_consideration,
                        'gst_amount': gst_amount,
                        'possession_date': possession_date.strftime("%d/%m/%Y"),
                        'booking_amount': booking_amount,
                        'parking_required': parking_required,
                        'parking_type': parking_type,
                        'parking_location': parking_location,
                        'parking_size': parking_size,
                        'issue_date': datetime.now().strftime("%d/%m/%Y")
                    }
                    
                    # Save to database
                    allotment_id = db.add_allotment(allotment_data, allottees_data)
                    
                    # Generate document
                    project_dict = {
                        'project_name': project_data[1],
                        'mahrera_no': project_data[3],
                        'survey_no': project_data[4],
                        'hissa_no': project_data[5],
                        'cts_no': project_data[6],
                        'final_plot_no': project_data[7],
                        'tps_details': project_data[8],
                        'plot_area': project_data[9],
                        'location': project_data[10],
                        'promoter_company': project_data[11],
                        'promoter_bank_name': project_data[12],
                        'promoter_account_name': project_data[13],
                        'promoter_account_no': project_data[14],
                        'promoter_branch': project_data[15],
                        'promoter_ifsc': project_data[16],
                        'cancellation_table': project_data[17]
                    }
                    
                    # Create output path
                    folder_path = os.path.join("Allotment_Letters", project_data[1])
                    os.makedirs(folder_path, exist_ok=True)
                    
                    filename = f"ALLOTMENT_{allotment_number.replace('/', '_')}_{unit_type}_{unit_number}_{allottees_data[0]['name'].replace(' ', '_')}.docx"
                    output_path = os.path.join(folder_path, filename)
                    
                    # Generate document
                    doc_gen.generate_allotment_letter(project_dict, allotment_data, allottees_data, output_path)
                    
                    st.success(f"✅ Allotment letter generated successfully!")
                    st.info(f"📄 File saved at: **{output_path}**")
                    st.info(f"📋 Allotment Number: **{allotment_number}**")
                    
                    # Store file info in session state for download button outside form
                    st.session_state.last_generated_file = output_path
                    st.session_state.last_generated_filename = filename
        
        # Download button outside the form
        if st.session_state.last_generated_file and os.path.exists(st.session_state.last_generated_file):
            st.markdown("---")
            st.markdown("### 📥 Download Generated Document")
            with open(st.session_state.last_generated_file, 'rb') as f:
                st.download_button(
                    label="📥 Download Allotment Letter",
                    data=f,
                    file_name=st.session_state.last_generated_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

# DASHBOARD PAGE
elif page == "📊 Dashboard":
    st.markdown('<h1 class="main-header">📊 Allotments Dashboard</h1>', unsafe_allow_html=True)
    
    projects = db.get_all_projects()
    
    if not projects:
        st.warning("⚠️ No projects found. Please create a project first.")
    else:
        project_options = {f"{p[1]} ({p[2]})": p[0] for p in projects}
        selected_project = st.selectbox("Select Project", options=list(project_options.keys()))
        project_id = project_options[selected_project]
        
        # Get allotments
        allotments = db.get_allotments_by_project(project_id)
        
        if not allotments:
            st.info("No allotments found for this project.")
        else:
            # Display statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Allotments", len(allotments))
            
            with col2:
                issued = len([a for a in allotments if a[22] == 'Issued'])
                st.metric("Issued", issued)
            
            with col3:
                frozen = len([a for a in allotments if a[22] == 'Frozen'])
                st.metric("Frozen", frozen)
            
            with col4:
                cancelled = len([a for a in allotments if a[22] == 'Cancelled'])
                st.metric("Cancelled", cancelled)
            
            st.markdown("---")
            
            # Display allotments table
            st.markdown("### 📋 All Allotments")
            
            df_data = []
            for allotment in allotments:
                allottees = db.get_allottees_by_allotment(allotment[0])
                allottee_names = ", ".join([a[2] for a in allottees])
                
                df_data.append({
                    "ID": allotment[0],
                    "Allotment No": allotment[2],
                    "Unit": f"{allotment[5]} {allotment[6]}",
                    "Floor": allotment[7],
                    "Wing": allotment[8],
                    "Area (sqft)": allotment[10],
                    "Consideration": f"₹{float(allotment[11]):,.0f}",
                    "Allottees": allottee_names,
                    "Status": allotment[22],
                    "Issue Date": allotment[23]
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

# MANAGE ALLOTMENTS PAGE
elif page == "❌ Manage Allotments":
    st.markdown('<h1 class="main-header">❌ Manage Allotments</h1>', unsafe_allow_html=True)
    
    projects = db.get_all_projects()
    
    if not projects:
        st.warning("⚠️ No projects found. Please create a project first.")
    else:
        project_options = {f"{p[1]} ({p[2]})": p[0] for p in projects}
        selected_project = st.selectbox("Select Project", options=list(project_options.keys()))
        project_id = project_options[selected_project]
        
        # Get allotments
        allotments = db.get_allotments_by_project(project_id)
        
        if not allotments:
            st.info("No allotments found for this project.")
        else:
            st.markdown("### Select Allotment to Manage")
            
            allotment_options = {}
            for allotment in allotments:
                allottees = db.get_allottees_by_allotment(allotment[0])
                allottee_names = ", ".join([a[2] for a in allottees])
                label = f"{allotment[2]} - {allotment[5]} {allotment[6]} - {allottee_names} - [{allotment[22]}]"
                allotment_options[label] = allotment[0]
            
            selected_allotment = st.selectbox("Select Allotment", options=list(allotment_options.keys()))
            allotment_id = allotment_options[selected_allotment]
            
            # Get allotment details
            allotment, allottees = db.get_allotment_details(allotment_id)
            
            # Display details
            st.markdown("---")
            st.markdown("### 📋 Allotment Details")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Allotment Number:** {allotment[2]}")
                st.write(f"**Unit:** {allotment[5]} {allotment[6]}")
                st.write(f"**Floor:** {allotment[7]}")
                st.write(f"**Wing:** {allotment[8]}")
            
            with col2:
                st.write(f"**Carpet Area:** {allotment[10]} sqft")
                st.write(f"**Consideration:** ₹{float(allotment[11]):,.0f}")
                st.write(f"**Booking Amount:** ₹{float(allotment[14]):,.0f}")
                st.write(f"**Possession Date:** {allotment[13]}")
            
            with col3:
                st.write(f"**Status:** {allotment[22]}")
                st.write(f"**Issue Date:** {allotment[23]}")
                st.write(f"**Parking:** {allotment[18]}")
            
            st.markdown("### 👥 Allottees")
            for allottee in allottees:
                st.write(f"- **{allottee[2]}** | {allottee[4]} | {allottee[5]}")
            
            st.markdown("---")
            st.markdown("### 🔧 Actions")

            current_status = allotment[22] or "Unknown"
            status_emoji = {
                "Issued": "🟢",
                "Frozen": "❄️",
                "Cancelled": "❌",
            }.get(current_status, "⚪")
            st.markdown(f"**Current status:** {status_emoji} `{current_status}`")

            available_actions = []
            if current_status == "Issued":
                available_actions = [
                    ("❄️ Freeze Allotment", "freeze", "secondary"),
                    ("❌ Cancel Allotment", "cancel", "secondary"),
                ]
            elif current_status == "Frozen":
                available_actions = [
                    ("🔓 Unfreeze Allotment", "unfreeze", "primary"),
                    ("❌ Cancel Allotment", "cancel", "secondary"),
                ]
            elif current_status == "Cancelled":
                available_actions = [
                    ("♻️ Reactivate Allotment", "reactivate", "primary"),
                ]
            else:
                st.warning(
                    f"Unrecognised status '{current_status}'. "
                    "Use Delete below if this record is corrupted."
                )

            if available_actions:
                action_cols = st.columns(len(available_actions))
                for (label, action, btn_type), col in zip(available_actions, action_cols):
                    with col:
                        if st.button(
                            label,
                            type=btn_type,
                            use_container_width=True,
                            key=f"action_{action}_{allotment_id}",
                        ):
                            if action == "freeze":
                                db.freeze_allotment(allotment_id)
                                st.success("✅ Allotment frozen.")
                                st.rerun()
                            elif action == "unfreeze":
                                db.unfreeze_allotment(allotment_id)
                                st.success("✅ Allotment unfrozen — status set back to Issued.")
                                st.rerun()
                            elif action == "cancel":
                                db.cancel_allotment(allotment_id)
                                st.success("✅ Allotment cancelled.")
                                st.info(
                                    "💡 This allotment number can be reassigned if no higher "
                                    "number has been issued."
                                )
                                st.rerun()
                            elif action == "reactivate":
                                ok, msg = db.reactivate_allotment(allotment_id)
                                if ok:
                                    st.success(f"✅ {msg}")
                                    st.rerun()
                                else:
                                    st.error(f"❌ {msg}")
            
            st.markdown("---")
            st.markdown("### 🗑️ Delete Allotment")
            st.caption(
                "Permanently removes this allotment and its allottee records from the database. "
                "Use Freeze/Cancel above if you only want a status change."
            )

            confirm_delete = st.checkbox(
                f"I understand this cannot be undone. Delete allotment '{allotment[2]}'.",
                key=f"confirm_delete_allotment_{allotment_id}",
            )

            if st.button(
                "🗑️ Delete Allotment Permanently",
                type="secondary",
                disabled=not confirm_delete,
                use_container_width=True,
                key=f"delete_allotment_btn_{allotment_id}",
            ):
                deleted_number = db.delete_allotment(allotment_id)
                st.success(f"✅ Allotment '{deleted_number}' deleted.")
                st.rerun()

            st.markdown("---")
            st.markdown("### ℹ️ Status Information")

            st.info("""
            **Status Definitions:**
            - **Issued**: Allotment letter has been issued to the client
            - **Frozen**: Client backed out after issuing. This number cannot be reassigned.
            - **Cancelled**: Client backed out before next allotment was issued. This number can be reassigned automatically.
            """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📞 Support")
st.sidebar.info("Real Estate Allotment System v1.0\n\nDeveloped for automating allotment letter generation and management.")
