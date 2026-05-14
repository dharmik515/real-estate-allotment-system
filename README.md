# 🏢 Real Estate Allotment Automation System

A comprehensive Streamlit-based application for automating property allotment letter generation and management for real estate companies in India.

## 🎯 Features

### Core Functionality
- ✅ **Project Management**: Create and manage multiple building projects with complete details
- ✅ **Automated Allotment Letters**: Generate professional allotment letters in DOCX format matching exact legal format
- ✅ **Sequential Numbering**: Automatic allotment number generation in format: `NN/YY-YY/CODE`
  - Example: `06/25-26/HA` (Allotment 6, FY 2025-26, Hanuman building)
- ✅ **Smart Reassignment Logic**: 
  - If client backs out AFTER next allotment issued → **Freeze** (cannot reassign)
  - If client backs out BEFORE next allotment issued → **Auto-reassign** to next client
- ✅ **Multiple Allottees**: Support for multiple allottees per unit
- ✅ **Detailed Parking Management**: 
  - Type: Stack/Surface
  - Location: Ground/Pith/Podium
  - Size: Big/Small
- ✅ **Dashboard**: View and manage all allotments with status tracking
- ✅ **Configurable Cancellation Policy**: Per-project cancellation charge tables

### Smart Features
- 🔄 **Automatic Project Code Generation**: 
  - "Hanuman" → HA
  - "New Mandar" → NM
- 📁 **Organized File Structure**: Each project gets its own folder
- 💰 **Indian Currency Formatting**: Proper lakh/crore formatting
- 📅 **Financial Year Tracking**: Automatic FY calculation (April-March)
- 🔢 **Number to Words Conversion**: Indian format (Crore, Lakh, Thousand)

## 📋 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup Steps

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the Application**
```bash
streamlit run app.py
```

3. **Access the Application**
The application will open in your default browser at `http://localhost:8501`

## 🚀 Usage Guide

### Step 1: Create a New Project

1. Navigate to **➕ New Project** from the sidebar
2. Fill in the project details:
   - **Project Information**: Name, MahaRERA No., Survey details, Location
   - **Promoter Information**: Company name, bank details
   - **Cancellation Policy**: Configure cancellation charges table
3. Click **Create Project**
4. A folder will be created automatically: `Allotment_Letters/[Project Name]/`

### Step 2: Issue Allotment Letter

1. Navigate to **📝 New Allotment**
2. Select the project
3. The system will show the next available allotment number
4. Fill in:
   - **Unit Information**: Type, number, floor, wing, area, consideration
   - **Parking Information**: Required? Type, location, size
   - **Allottee Information**: Name, address, PAN, Aadhar, bank details
   - Support for multiple allottees
5. Click **Generate Allotment Letter**
6. Download the generated DOCX file

### Step 3: Manage Allotments

1. Navigate to **📊 Dashboard** to view all allotments
2. Navigate to **❌ Manage Allotments** to:
   - **Freeze**: When client backs out after next allotment issued
   - **Cancel**: When client backs out before next allotment issued (enables auto-reassignment)
   - **Unfreeze**: Reactivate a frozen allotment

## 🏗️ System Architecture

### Database Schema

#### Projects Table
- Project details (name, code, MahaRERA, survey details)
- Promoter information
- Bank details
- Cancellation policy

#### Allotments Table
- Allotment number and sequence
- Unit details
- Financial information
- Parking details
- Status tracking (Issued/Frozen/Cancelled)

#### Allottees Table
- Personal information
- Contact details
- Bank details
- Linked to allotments (many-to-one)

### File Structure
```
.
├── app.py                          # Main Streamlit application
├── database.py                     # Database operations
├── document_generator.py           # DOCX generation logic
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── allotments.db                   # SQLite database (auto-created)
└── Allotment_Letters/              # Generated documents (auto-created)
    ├── Project_Name_1/
    │   ├── ALLOTMENT_01_25-26_XX_Shop_4_Client_Name.docx
    │   └── ...
    └── Project_Name_2/
        └── ...
```

## 🔄 Allotment Number Logic

### Scenario 1: Freeze (Cannot Reassign)
```
Allotment 1 → Issued ✅
Allotment 2 → Issued ✅
Allotment 3 → Issued ✅
Client 2 backs out → FREEZE #2 ❄️
Next allotment → #4 (cannot use #2)
```

### Scenario 2: Auto-Reassign
```
Allotment 1 → Issued ✅
Allotment 2 → Issued ✅
Client 2 backs out → CANCEL #2 ❌
Next allotment → #2 (auto-reassigned) 🔄
```

## 📄 Generated Document Format

The system generates allotment letters in the exact format required, including:

1. **Header**: Allotment number and date
2. **Allottee Details**: Names, address, PAN, Aadhar
3. **Subject Line**: Project and MahaRERA details
4. **15 Standard Clauses**:
   - Allotment of unit
   - Parking allocation
   - Payment receipt
   - Disclosures
   - Encumbrances
   - Further payments
   - Possession
   - Interest payment
   - Cancellation policy
   - Other payments
   - Agreement proforma
   - Execution and registration
   - Validity
   - Headings
5. **Cancellation Charges Table**
6. **Bank Details Schedule** (Promoter & Allottee)
7. **Signature Sections**

## 🛠️ Technical Details

### Technologies Used
- **Streamlit**: Web application framework
- **SQLite**: Database for storing project and allotment data
- **python-docx**: DOCX document generation
- **Pandas**: Data manipulation and display

### Key Functions

#### Database Operations
- `add_project()`: Create new project
- `add_allotment()`: Create new allotment with allottees
- `get_next_allotment_number()`: Smart number generation with reassignment logic
- `freeze_allotment()`: Freeze allotment (cannot reassign)
- `cancel_allotment()`: Cancel allotment (can reassign)

#### Document Generation
- `generate_allotment_letter()`: Create DOCX in exact format
- `format_currency()`: Indian currency formatting
- `number_to_words_indian()`: Convert numbers to words (Crore/Lakh format)

## 📊 Dashboard Features

- **Statistics**: Total projects, allotments, active/frozen/cancelled counts
- **Allotment Table**: Sortable, filterable view of all allotments
- **Status Tracking**: Real-time status updates
- **Quick Actions**: Freeze, unfreeze, cancel operations

## 🔐 Data Security

- All data stored locally in SQLite database
- No external API calls
- Documents saved in local file system
- No cloud dependencies

## 🎨 Customization

### Modify Cancellation Policy
Edit the cancellation charges table when creating a new project. Each project can have its own policy.

### Change Document Format
Modify `document_generator.py` to adjust:
- Font sizes and styles
- Paragraph spacing
- Table formatting
- Additional clauses

### Add New Fields
1. Update database schema in `database.py`
2. Add form fields in `app.py`
3. Update document generation in `document_generator.py`

## 📞 Support & Troubleshooting

### Common Issues

**Issue**: Application won't start
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Database error
- **Solution**: Delete `allotments.db` and restart the application

**Issue**: Document generation fails
- **Solution**: Check that all required fields are filled

**Issue**: Allotment number not reassigning
- **Solution**: Ensure the allotment is marked as "Cancelled" not "Frozen"

## 🚀 Future Enhancements

- [ ] PDF generation support
- [ ] Email integration for sending allotment letters
- [ ] Payment tracking and installment management
- [ ] Document templates for other legal documents
- [ ] Multi-language support
- [ ] Advanced reporting and analytics
- [ ] Bulk allotment generation
- [ ] Document version control

## 📝 License

This system is developed for internal use by real estate companies. All rights reserved.

## 👨‍💻 Developer Notes

- Built with Python 3.9+
- Uses SQLite for zero-configuration database
- Streamlit for rapid UI development
- python-docx for document generation matching exact legal format
- Follows Indian real estate documentation standards

---

**Version**: 1.0.0  
**Last Updated**: April 2026  
**Developed for**: Real Estate Companies in Mumbai, India
