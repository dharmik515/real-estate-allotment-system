# 🏗️ System Architecture

## Overview

The Real Estate Allotment Automation System is built using a modular architecture with clear separation of concerns.

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                    (Streamlit Web App)                      │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   Home   │  │  New     │  │   New    │  │Dashboard │  │
│  │   Page   │  │ Project  │  │Allotment │  │  & Mgmt  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                         │
│                        (app.py)                             │
│                                                             │
│  • Form Validation                                          │
│  • User Input Processing                                    │
│  • Business Logic Coordination                              │
│  • UI State Management                                      │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                ▼                       ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│    DATABASE LAYER        │  │   DOCUMENT LAYER         │
│     (database.py)        │  │  (document_generator.py) │
│                          │  │                          │
│  • Project CRUD          │  │  • DOCX Generation       │
│  • Allotment CRUD        │  │  • Template Formatting   │
│  • Allottee CRUD         │  │  • Currency Formatting   │
│  • Number Generation     │  │  • Number to Words       │
│  • Status Management     │  │  • Table Generation      │
│  • Reassignment Logic    │  │  • Legal Clauses         │
└──────────────────────────┘  └──────────────────────────┘
                │                         │
                ▼                         ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│   DATA PERSISTENCE       │  │   FILE SYSTEM            │
│   (SQLite Database)      │  │   (DOCX Files)           │
│                          │  │                          │
│  • allotments.db         │  │  • Allotment_Letters/    │
│    - projects            │  │    - Project_1/          │
│    - allotments          │  │      - Letter_1.docx     │
│    - allottees           │  │      - Letter_2.docx     │
│                          │  │    - Project_2/          │
└──────────────────────────┘  └──────────────────────────┘
```

---

## 🔄 Data Flow

### 1. Project Creation Flow
```
User Input (Form)
    ↓
Validation (app.py)
    ↓
generate_project_code() (database.py)
    ↓
add_project() (database.py)
    ↓
SQLite INSERT (projects table)
    ↓
Create Folder (File System)
    ↓
Success Message (UI)
```

### 2. Allotment Creation Flow
```
User Selects Project
    ↓
get_next_allotment_number() (database.py)
    ├─ Check for cancelled allotments
    ├─ Check max sequence number
    └─ Apply reassignment logic
    ↓
Display Next Number (UI)
    ↓
User Fills Form
    ↓
Validation (app.py)
    ↓
add_allotment() (database.py)
    ├─ INSERT into allotments table
    └─ INSERT into allottees table
    ↓
generate_allotment_letter() (document_generator.py)
    ├─ Create DOCX document
    ├─ Format content
    ├─ Add tables
    └─ Save to file system
    ↓
Download Link (UI)
```

### 3. Allotment Management Flow
```
User Selects Allotment
    ↓
get_allotment_details() (database.py)
    ↓
Display Details (UI)
    ↓
User Action (Freeze/Cancel/Unfreeze)
    ↓
Update Status (database.py)
    ├─ freeze_allotment()
    ├─ cancel_allotment()
    └─ unfreeze_allotment()
    ↓
SQLite UPDATE (allotments table)
    ↓
Refresh UI
```

---

## 🗄️ Database Schema

### Projects Table
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    project_code TEXT NOT NULL UNIQUE,
    mahrera_no TEXT,
    survey_no TEXT,
    hissa_no TEXT,
    cts_no TEXT,
    final_plot_no TEXT,
    tps_details TEXT,
    plot_area TEXT,
    location TEXT,
    promoter_company TEXT,
    promoter_bank_name TEXT,
    promoter_account_name TEXT,
    promoter_account_no TEXT,
    promoter_branch TEXT,
    promoter_ifsc TEXT,
    cancellation_table TEXT,  -- JSON
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Allotments Table
```sql
CREATE TABLE allotments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    allotment_number TEXT UNIQUE,
    allotment_sequence INTEGER,
    financial_year TEXT,
    unit_type TEXT,
    unit_number TEXT,
    floor TEXT,
    wing TEXT,
    carpet_area_sqm REAL,
    carpet_area_sqft REAL,
    total_consideration REAL,
    gst_amount REAL,
    possession_date TEXT,
    booking_amount REAL,
    payment_dates TEXT,
    payment_modes TEXT,
    parking_required TEXT,
    parking_type TEXT,
    parking_location TEXT,
    parking_size TEXT,
    status TEXT DEFAULT 'Active',  -- Issued/Frozen/Cancelled
    issue_date TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id)
)
```

### Allottees Table
```sql
CREATE TABLE allottees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    allotment_id INTEGER,
    name TEXT,
    address TEXT,
    phone TEXT,
    pan_card TEXT,
    aadhar_card TEXT,
    email TEXT,
    bank_name TEXT,
    account_name TEXT,
    account_no TEXT,
    branch TEXT,
    ifsc TEXT,
    FOREIGN KEY (allotment_id) REFERENCES allotments (id)
)
```

### Relationships
```
projects (1) ──────< (many) allotments
allotments (1) ─────< (many) allottees
```

---

## 🧩 Component Details

### 1. app.py (Application Layer)
**Responsibilities:**
- User interface rendering
- Form handling and validation
- Navigation and routing
- State management
- Coordination between database and document layers

**Key Functions:**
- Page rendering (Home, New Project, New Allotment, Dashboard, Manage)
- Form submission handling
- Data display and formatting
- User action processing

### 2. database.py (Data Layer)
**Responsibilities:**
- Database initialization
- CRUD operations
- Business logic for allotment numbering
- Status management
- Reassignment logic

**Key Functions:**
- `init_database()`: Create tables
- `add_project()`: Create new project
- `add_allotment()`: Create new allotment
- `get_next_allotment_number()`: Smart number generation
- `freeze_allotment()`: Freeze allotment
- `cancel_allotment()`: Cancel with reassignment
- `get_allotments_by_project()`: Retrieve allotments

### 3. document_generator.py (Document Layer)
**Responsibilities:**
- DOCX document generation
- Content formatting
- Currency and number formatting
- Table generation
- Legal clause insertion

**Key Functions:**
- `generate_allotment_letter()`: Main generation function
- `format_currency()`: Indian currency formatting
- `number_to_words_indian()`: Number to words conversion
- `_add_standard_clauses()`: Add legal clauses
- `_add_cancellation_table()`: Generate cancellation table
- `_add_bank_details()`: Generate bank details table

---

## 🔐 Security Considerations

### Data Security
- ✅ Local SQLite database (no cloud exposure)
- ✅ No external API calls
- ✅ File system access restricted to application directory
- ✅ No sensitive data transmission

### Input Validation
- ✅ Required field validation
- ✅ Data type validation
- ✅ Numeric range validation
- ✅ SQL injection prevention (parameterized queries)

---

## 🚀 Performance Optimization

### Database
- Indexed primary keys
- Foreign key relationships
- Efficient queries with WHERE clauses
- Minimal JOIN operations

### Document Generation
- Lazy loading of templates
- Efficient string formatting
- Minimal memory footprint
- Fast DOCX generation

### UI
- Streamlit caching for database queries
- Efficient state management
- Minimal re-renders
- Fast page navigation

---

## 📈 Scalability

### Current Capacity
- **Projects**: Unlimited
- **Allotments per Project**: Unlimited
- **Allottees per Allotment**: 5 (configurable)
- **Document Size**: ~50KB per allotment letter

### Growth Considerations
- SQLite can handle millions of records
- File system can store thousands of documents
- Streamlit can handle multiple concurrent users
- No external dependencies or rate limits

---

## 🔄 Allotment Number Logic

### Algorithm
```python
def get_next_allotment_number(project_id):
    # Get financial year
    fy = calculate_financial_year()
    
    # Check for cancelled allotments that can be reassigned
    cancelled = get_cancelled_before_max_issued(project_id, fy)
    
    if cancelled:
        # Reassign cancelled number
        sequence = cancelled.sequence
    else:
        # Get next sequential number
        max_sequence = get_max_sequence(project_id, fy)
        sequence = max_sequence + 1
    
    # Format: NN/YY-YY/CODE
    return f"{sequence:02d}/{fy}/{project_code}"
```

### States
```
┌─────────┐
│ Issued  │ ──┐
└─────────┘   │
              │ Client backs out
              │ AFTER next issued
              ▼
         ┌─────────┐
         │ Frozen  │ (Cannot reassign)
         └─────────┘
              │
              │ Manual unfreeze
              ▼
         ┌─────────┐
         │ Active  │
         └─────────┘

┌─────────┐
│ Issued  │ ──┐
└─────────┘   │
              │ Client backs out
              │ BEFORE next issued
              ▼
         ┌───────────┐
         │ Cancelled │ (Can reassign)
         └───────────┘
              │
              │ Auto-reassign
              ▼
         ┌─────────┐
         │ Issued  │ (New client)
         └─────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Streamlit | Web UI framework |
| Backend | Python 3.9+ | Application logic |
| Database | SQLite | Data persistence |
| Document | python-docx | DOCX generation |
| Data Processing | Pandas | Data manipulation |
| Styling | Custom CSS | UI enhancement |

---

## 📦 Deployment Options

### Option 1: Local Desktop
- Run on Windows/Mac/Linux
- No internet required
- Full control over data
- **Recommended for single user**

### Option 2: Local Network
- Deploy on local server
- Access via LAN
- Multiple users
- **Recommended for small teams**

### Option 3: Cloud Deployment
- Deploy on Streamlit Cloud / AWS / Azure
- Internet access required
- Remote access
- **Recommended for distributed teams**

---

## 🔮 Future Architecture Enhancements

### Phase 2
- [ ] PostgreSQL for multi-user support
- [ ] Redis for caching
- [ ] Celery for background tasks
- [ ] REST API for integrations

### Phase 3
- [ ] Microservices architecture
- [ ] Message queue for async processing
- [ ] Document versioning system
- [ ] Audit logging

### Phase 4
- [ ] Machine learning for data extraction
- [ ] OCR for document scanning
- [ ] Blockchain for document verification
- [ ] Mobile app

---

## 📚 Design Patterns Used

1. **MVC Pattern**: Separation of UI, logic, and data
2. **Repository Pattern**: Database abstraction
3. **Factory Pattern**: Document generation
4. **Singleton Pattern**: Database connection
5. **Strategy Pattern**: Allotment number generation

---

## ✅ Best Practices Followed

- ✅ **DRY**: Don't Repeat Yourself
- ✅ **SOLID**: Single Responsibility, Open/Closed, etc.
- ✅ **Clean Code**: Readable, maintainable
- ✅ **Error Handling**: Graceful failures
- ✅ **Documentation**: Comprehensive comments
- ✅ **Type Safety**: Type hints where applicable
- ✅ **Testing Ready**: Modular, testable code

---

**Architecture Version**: 1.0  
**Last Updated**: April 2026
