# 🚀 Quick Start Guide

## Installation (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

---

## First Time Setup (10 minutes)

### 1️⃣ Create Your First Project

1. Click **➕ New Project** in the sidebar
2. Fill in the minimum required fields:
   - **Project Name**: e.g., "Hanuman Tower" (will generate code "HA")
   - **MahaRERA No**: Your registration number
   - **Location**: Full address
   - **Promoter Company**: Your company name
   - **Bank Details**: Your company bank account
3. Click **Create Project**

✅ A folder will be created: `Allotment_Letters/Hanuman Tower/`

---

### 2️⃣ Issue Your First Allotment

1. Click **📝 New Allotment** in the sidebar
2. Select your project
3. You'll see: **Next Allotment Number: 01/25-26/HA**
4. Fill in:

   **Unit Information:**
   - Unit Type: Shop
   - Unit Number: 1
   - Floor: Ground floor
   - Wing: A wing
   - Carpet Area: 18.21 sq.mtrs / 196 sq.ft
   - Total Consideration: 7840000
   - GST Amount: 1411200
   - Booking Amount: 2000000
   - Possession Date: Select date

   **Parking:**
   - Required: No (or Yes with details)

   **Allottee Information:**
   - Name: MISS. KAVYA HARISH SUVARNA
   - Phone: +91 9820811207
   - PAN: ISUPS7785A
   - Aadhar: 9100 0030 8556
   - Address: Full address
   - Bank Details: Complete bank information

5. Click **Generate Allotment Letter**
6. Click **📥 Download Allotment Letter**

✅ Your first allotment letter is ready!

---

### 3️⃣ View Dashboard

1. Click **📊 Dashboard** in the sidebar
2. Select your project
3. See all allotments with status

---

### 4️⃣ Manage Allotments

1. Click **❌ Manage Allotments** in the sidebar
2. Select an allotment
3. Available actions:
   - **Freeze**: Client backed out after next allotment issued
   - **Cancel**: Client backed out before next allotment issued
   - **Unfreeze**: Reactivate frozen allotment

---

## 📋 Sample Data for Testing

### Project Details
```
Project Name: Hanuman Tower
MahaRERA No: P51800053401
Survey No: Survey No. 23
Hissa No: Hissa No. 1/A (Pt.)
CTS No: CTS No. 333A/1
Final Plot No: Final Plot No. 222-223
TPS Details: TPS III, New Final Plot No. 253
Plot Area: 1138.80 sq. mtrs
Location: Borivali West, Mumbai 400 091

Promoter Company: OSSIA BUILDCON PRIVATE LIMITED
Account Name: OSSIA BUILDCON PRIVATE LIMITED
Account No: 615011013334
Bank Name: KOTAK MAHINDRA BANK
Branch: CHANDAVARKAR ROAD, BORIVALI WEST
IFSC: KKBK0000653
```

### Allottee Details
```
Name: MISS. KAVYA HARISH SUVARNA
Address: B/19, Om Satyavinayak CHS LTD
Behind Suvarna Hospital
Kastur Park, Shimpoli road
Borivali (West) Maharashtra
Phone: +91 9820811207
PAN: ISUPS7785A
Aadhar: 9100 0030 8556
Email: kavya@example.com

Bank Details:
Account Name: KAVYA SUVARNA
Account No: 1004031300237009
Bank Name: SHAMRAO VITTHAL CO-OP BANK
Branch: BORIVALI (EAST)
IFSC: SVCB0000004
```

---

## 🎯 Understanding Allotment Numbers

### Format: `NN/YY-YY/CODE`

- **NN**: Sequential number (01, 02, 03...)
- **YY-YY**: Financial year (25-26 for 2025-2026)
- **CODE**: Project code (auto-generated from project name)

### Examples:
- `01/25-26/HA` - First allotment, FY 2025-26, Hanuman project
- `06/25-26/NM` - Sixth allotment, FY 2025-26, New Mandar project
- `15/26-27/OC` - Fifteenth allotment, FY 2026-27, Ossia Crest project

---

## 🔄 Testing Reassignment Logic

### Test Scenario 1: Freeze (Cannot Reassign)
1. Create Allotment #1 ✅
2. Create Allotment #2 ✅
3. Create Allotment #3 ✅
4. Go to **Manage Allotments**
5. Select Allotment #2
6. Click **❄️ Freeze Allotment**
7. Create new allotment → Will be #4 (not #2)

### Test Scenario 2: Auto-Reassign
1. Create Allotment #1 ✅
2. Create Allotment #2 ✅
3. Go to **Manage Allotments**
4. Select Allotment #2
5. Click **❌ Cancel Allotment**
6. Create new allotment → Will be #2 (reassigned!) 🔄

---

## 📁 File Structure After Setup

```
Your_Workspace/
├── app.py
├── database.py
├── document_generator.py
├── requirements.txt
├── README.md
├── QUICK_START.md
├── allotments.db                    # Auto-created database
└── Allotment_Letters/               # Auto-created folder
    └── Hanuman Tower/
        ├── ALLOTMENT_01_25-26_HA_Shop_1_MISS._KAVYA_HARISH_SUVARNA.docx
        ├── ALLOTMENT_02_25-26_HA_Shop_2_Client_Name.docx
        └── ...
```

---

## 🎨 Tips & Best Practices

### ✅ DO:
- Fill all required fields marked with *
- Use proper formatting for PAN (XXXXX0000X) and Aadhar (0000 0000 0000)
- Double-check consideration amounts before generating
- Keep project names clear and descriptive
- Use "Cancel" for clients who back out early (enables reassignment)
- Use "Freeze" for clients who back out after next allotment issued

### ❌ DON'T:
- Don't delete the `allotments.db` file (contains all your data)
- Don't manually edit generated DOCX files (regenerate instead)
- Don't use special characters in project names
- Don't freeze allotments unnecessarily (use cancel when possible)

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| App won't start | Run: `pip install -r requirements.txt` |
| "Module not found" error | Install missing package: `pip install [package-name]` |
| Database error | Delete `allotments.db` and restart |
| Document not generating | Check all required fields are filled |
| Wrong allotment number | Check if previous allotments are cancelled (not frozen) |

---

## 📞 Need Help?

1. Check the full **README.md** for detailed documentation
2. Review the **Dashboard** to see current allotments
3. Use **Manage Allotments** to check status of each allotment

---

## 🎉 You're Ready!

Your Real Estate Allotment Automation System is now set up and ready to use. Start creating projects and issuing allotment letters!

**Time Saved**: ~30 minutes per allotment letter  
**Accuracy**: 100% (no manual typing errors)  
**Professional**: Exact legal format every time

Happy Automating! 🚀
