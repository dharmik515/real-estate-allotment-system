# 👤 User Guide: Real Estate Allotment System

## 📖 Table of Contents
1. [Getting Started](#getting-started)
2. [Creating Your First Project](#creating-your-first-project)
3. [Issuing Allotment Letters](#issuing-allotment-letters)
4. [Managing Allotments](#managing-allotments)
5. [Understanding Allotment Numbers](#understanding-allotment-numbers)
6. [Common Scenarios](#common-scenarios)
7. [Tips & Best Practices](#tips--best-practices)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Getting Started

### Step 1: Launch the Application

Open your terminal/command prompt and run:
```bash
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`

### Step 2: Understand the Interface

The application has **5 main pages** accessible from the sidebar:

| Page | Purpose |
|------|---------|
| 🏠 **Home** | Overview and statistics |
| ➕ **New Project** | Create new building projects |
| 📝 **New Allotment** | Issue allotment letters |
| 📊 **Dashboard** | View all allotments |
| ❌ **Manage Allotments** | Freeze/Cancel/Unfreeze |

---

## 🏗️ Creating Your First Project

### What is a Project?
A project represents a building or real estate development. Each project has its own:
- Unique project code (auto-generated)
- Folder for storing allotment letters
- Cancellation policy
- Promoter details

### Step-by-Step Guide

1. **Click "➕ New Project"** in the sidebar

2. **Fill in Project Information**:
   ```
   Project Name: Hanuman Tower
   → System generates code: HA
   
   Project Name: New Mandar Complex
   → System generates code: NM
   ```

3. **Enter MahaRERA Details**:
   - MahaRERA Registration No: P51800053401
   - Survey No: Survey No. 23
   - Hissa No: Hissa No. 1/A (Pt.)
   - CTS No: CTS No. 333A/1
   - Final Plot No: Final Plot No. 222-223
   - TPS Details: TPS III, New Final Plot No. 253
   - Plot Area: 1138.80 sq. mtrs
   - Location: Borivali West, Mumbai 400 091

4. **Enter Promoter Information**:
   - Company Name: OSSIA BUILDCON PRIVATE LIMITED
   - Bank Details: Account name, number, bank, branch, IFSC

5. **Configure Cancellation Policy**:
   - Default policy is pre-filled
   - Modify if needed for your project
   - Each project can have different policies

6. **Click "Create Project"**

✅ **Result**: 
- Project created in database
- Folder created: `Allotment_Letters/Hanuman Tower/`
- Project code assigned: HA

---

## 📝 Issuing Allotment Letters

### When to Issue?
Issue an allotment letter when a client books a unit in your project.

### Step-by-Step Guide

1. **Click "📝 New Allotment"** in the sidebar

2. **Select Project**:
   - Choose from dropdown: "Hanuman Tower (HA)"
   - System shows next allotment number: **01/25-26/HA**

3. **Fill Unit Information**:
   ```
   Unit Type: Shop / Flat / Office
   Unit Number: 4
   Floor: Ground floor
   Wing: A wing
   Carpet Area (sq.mtrs): 18.21
   Carpet Area (sq.ft): 196
   Total Consideration: 7840000
   GST Amount: 1411200
   Booking Amount: 2000000
   Possession Date: Select from calendar
   ```

4. **Configure Parking** (if required):
   
   **Option 1: No Parking**
   - Select "No"
   - Standard clause will be added to letter
   
   **Option 2: With Parking**
   - Select "Yes"
   - Choose Type: Stack / Surface
   - Choose Location: Ground / Pith / Podium
   - Choose Size: Big / Small

5. **Enter Allottee Information**:
   
   **Number of Allottees**: 1, 2, 3, 4, or 5
   
   **For Each Allottee**:
   ```
   Full Name: MISS. KAVYA HARISH SUVARNA
   Address: B/19, Om Satyavinayak CHS LTD
            Behind Suvarna Hospital
            Kastur Park, Shimpoli road
            Borivali (West) Maharashtra
   Phone: +91 9820811207
   PAN Card: ISUPS7785A
   Aadhar Card: 9100 0030 8556
   Email: kavya@example.com
   
   Bank Details:
   Account Name: KAVYA SUVARNA
   Account Number: 1004031300237009
   Bank Name: SHAMRAO VITTHAL CO-OP BANK
   Branch: BORIVALI (EAST)
   IFSC Code: SVCB0000004
   ```

6. **Click "Generate Allotment Letter"**

7. **Download the Document**:
   - Click "📥 Download Allotment Letter"
   - File saved in: `Allotment_Letters/Hanuman Tower/`
   - Filename: `ALLOTMENT_01_25-26_HA_Shop_4_MISS._KAVYA_HARISH_SUVARNA.docx`

✅ **Result**: 
- Allotment letter generated in exact legal format
- Saved to project folder
- Ready to print and give to client

---

## 📊 Managing Allotments

### Viewing All Allotments

1. **Click "📊 Dashboard"** in the sidebar
2. **Select Project** from dropdown
3. **View Statistics**:
   - Total Allotments
   - Issued
   - Frozen
   - Cancelled

4. **View Allotment Table**:
   - Allotment Number
   - Unit Details
   - Allottee Names
   - Status
   - Issue Date

### Managing Individual Allotments

1. **Click "❌ Manage Allotments"** in the sidebar
2. **Select Project** from dropdown
3. **Select Allotment** from dropdown
4. **View Complete Details**:
   - Allotment information
   - Unit details
   - Allottee information
   - Current status

5. **Available Actions**:

   **❄️ Freeze Allotment**
   - Use when: Client backs out AFTER next allotment issued
   - Effect: Number cannot be reassigned
   - Status: Issued → Frozen
   
   **❌ Cancel Allotment**
   - Use when: Client backs out BEFORE next allotment issued
   - Effect: Number can be auto-reassigned
   - Status: Issued → Cancelled
   
   **🔓 Unfreeze Allotment**
   - Use when: Want to reactivate a frozen allotment
   - Effect: Allotment becomes active again
   - Status: Frozen → Active

---

## 🔢 Understanding Allotment Numbers

### Format: `NN/YY-YY/CODE`

**Example**: `06/25-26/HA`

| Part | Meaning | Example |
|------|---------|---------|
| **NN** | Sequential number | 06 = 6th allotment |
| **YY-YY** | Financial year | 25-26 = FY 2025-2026 |
| **CODE** | Project code | HA = Hanuman |

### Financial Year Calculation

- **April to March**: Indian financial year
- **Example**:
  - Date: 15th May 2025 → FY: 25-26
  - Date: 15th February 2026 → FY: 25-26
  - Date: 15th April 2026 → FY: 26-27

### Project Code Generation

| Project Name | Code | Logic |
|--------------|------|-------|
| Hanuman | HA | First 2 letters |
| New Mandar | NM | First letter of each word |
| Ossia Crest | OC | First letter of each word |
| Ashwin Tower | AS | First 2 letters |

---

## 🎯 Common Scenarios

### Scenario 1: Normal Allotment Flow

```
Step 1: Issue Allotment #1 to Client A
        → Status: Issued
        → File: ALLOTMENT_01_25-26_HA_...

Step 2: Issue Allotment #2 to Client B
        → Status: Issued
        → File: ALLOTMENT_02_25-26_HA_...

Step 3: Issue Allotment #3 to Client C
        → Status: Issued
        → File: ALLOTMENT_03_25-26_HA_...

✅ All allotments active and issued
```

### Scenario 2: Client Backs Out (Freeze)

```
Step 1: Allotment #1, #2, #3 issued ✅

Step 2: Client B (Allotment #2) backs out
        → Already issued #3 to Client C
        → Action: FREEZE #2
        → Status: Frozen ❄️

Step 3: Issue next allotment
        → Next number: #4 (not #2)
        → #2 cannot be reassigned

Result: #1 ✅, #2 ❄️, #3 ✅, #4 ✅
```

### Scenario 3: Client Backs Out (Auto-Reassign)

```
Step 1: Allotment #1, #2 issued ✅

Step 2: Client B (Allotment #2) backs out
        → Have NOT issued #3 yet
        → Action: CANCEL #2
        → Status: Cancelled ❌

Step 3: Issue next allotment to Client D
        → System auto-assigns: #2 (reassigned!) 🔄
        → Client D gets #2

Result: #1 ✅, #2 ✅ (Client D), #3 (next)
```

### Scenario 4: Multiple Allottees

```
Example: Husband and Wife buying together

Allottee 1:
- Name: MR. HARISH SUVARNA
- PAN: XXXXX0000X
- Bank: His account

Allottee 2:
- Name: MRS. PRITI SUVARNA
- PAN: YYYYY0000Y
- Bank: Her account

Result: Both names appear on allotment letter
```

### Scenario 5: Parking Allocation

```
Example 1: No Parking
- Select: No
- Letter includes: "Allottee does not require parking..."

Example 2: With Parking
- Select: Yes
- Type: Stack
- Location: Podium
- Size: Big
- Letter includes: "Allottee has been allotted Stack parking at Podium (Big size)..."
```

---

## 💡 Tips & Best Practices

### ✅ DO:

1. **Always fill required fields** (marked with *)
2. **Double-check amounts** before generating
3. **Use proper PAN format**: XXXXX0000X
4. **Use proper Aadhar format**: 0000 0000 0000
5. **Keep project names clear**: "Hanuman Tower" not "HT"
6. **Use Cancel instead of Freeze** when possible (enables reassignment)
7. **Review generated document** before giving to client
8. **Keep backup** of allotments.db file regularly

### ❌ DON'T:

1. **Don't delete allotments.db** (contains all your data)
2. **Don't manually edit generated DOCX** (regenerate instead)
3. **Don't use special characters** in project names
4. **Don't freeze unnecessarily** (use cancel when possible)
5. **Don't skip required fields** (validation will fail)
6. **Don't close browser** while generating document

### 🎯 Best Practices:

1. **Create one project at a time** and test with sample allotment
2. **Use consistent naming** for units (Shop 1, Shop 2, etc.)
3. **Keep allottee information accurate** (legal document)
4. **Review cancellation policy** before creating project
5. **Use Dashboard regularly** to track allotments
6. **Backup database weekly** (copy allotments.db)

---

## 🔧 Troubleshooting

### Problem: Application won't start

**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
pip install -r requirements.txt
```

---

### Problem: "No projects found"

**Cause**: No projects created yet

**Solution**:
1. Go to "➕ New Project"
2. Create your first project
3. Then proceed to create allotments

---

### Problem: Document not generating

**Possible Causes**:
1. Required fields not filled
2. Invalid data format
3. File permission issue

**Solution**:
1. Check all required fields (marked with *)
2. Verify PAN/Aadhar format
3. Check folder permissions
4. Try again with valid data

---

### Problem: Wrong allotment number

**Cause**: Previous allotment is Frozen instead of Cancelled

**Solution**:
1. Go to "❌ Manage Allotments"
2. Check status of previous allotments
3. If should be reassigned, use "Cancel" not "Freeze"
4. Try creating allotment again

---

### Problem: Can't download document

**Cause**: Browser blocking download

**Solution**:
1. Check browser download settings
2. Allow downloads from localhost
3. Check if file exists in Allotment_Letters folder
4. Try different browser

---

### Problem: Database error

**Error**: `database is locked` or `unable to open database`

**Solution**:
1. Close all instances of the application
2. Restart the application
3. If persists, delete allotments.db and start fresh

---

### Problem: Allotment number not incrementing

**Cause**: Cancelled allotments exist

**Explanation**: System is reassigning cancelled numbers (this is correct behavior!)

**Solution**: This is working as designed. Cancelled numbers are reassigned before incrementing.

---

## 📞 Getting Help

### Quick Reference

| Issue | Page to Check |
|-------|---------------|
| Setup problems | QUICK_START.md |
| Feature questions | README.md |
| Technical details | ARCHITECTURE.md |
| Project overview | PROJECT_SUMMARY.md |

### Common Questions

**Q: Can I edit a generated allotment letter?**  
A: Yes, but regenerate instead of manually editing. Go to "📝 New Allotment" and create again with correct data.

**Q: Can I delete an allotment?**  
A: No, but you can Cancel or Freeze it. This maintains audit trail.

**Q: How many projects can I create?**  
A: Unlimited. The system can handle any number of projects.

**Q: Can I change project details after creation?**  
A: Currently no. Create a new project if needed. (Future enhancement)

**Q: What if I make a mistake in allottee name?**  
A: Cancel the allotment and create a new one with correct details.

**Q: Can I export allotment data?**  
A: Currently no. View in Dashboard. (Future enhancement)

---

## 🎓 Training Checklist

Use this checklist to ensure you understand all features:

- [ ] I can launch the application
- [ ] I can create a new project
- [ ] I understand project code generation
- [ ] I can issue an allotment letter
- [ ] I can add multiple allottees
- [ ] I can configure parking details
- [ ] I can download generated documents
- [ ] I can view the dashboard
- [ ] I understand Freeze vs Cancel
- [ ] I can manage allotments
- [ ] I understand allotment number format
- [ ] I know when to use Freeze
- [ ] I know when to use Cancel
- [ ] I understand auto-reassignment logic

---

## 🎉 You're Ready!

Congratulations! You now know how to use the Real Estate Allotment Automation System.

**Remember**:
- Start with creating a project
- Issue allotments one by one
- Use Dashboard to track everything
- Use Cancel (not Freeze) when possible
- Keep backups of your database

**Need Help?**
- Check README.md for detailed documentation
- Check QUICK_START.md for quick reference
- Check ARCHITECTURE.md for technical details

---

**User Guide Version**: 1.0  
**Last Updated**: April 2026  
**For**: Real Estate Allotment System v1.0
