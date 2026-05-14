import sqlite3
import os
from datetime import datetime
import json

class AllotmentDatabase:
    def __init__(self, db_path="allotments.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
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
                cancellation_table TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_podiums INTEGER DEFAULT 0
            )
        ''')

        cursor.execute("PRAGMA table_info(projects)")
        existing_cols = {row[1] for row in cursor.fetchall()}
        if 'total_podiums' not in existing_cols:
            cursor.execute('ALTER TABLE projects ADD COLUMN total_podiums INTEGER DEFAULT 0')

        # Allotments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS allotments (
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
                allottees TEXT,
                parking_required TEXT,
                parking_type TEXT,
                parking_location TEXT,
                parking_size TEXT,
                status TEXT DEFAULT 'Active',
                issue_date TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )
        ''')
        
        # Allottees table (for multiple allottees per unit)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS allottees (
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
        ''')

        # Heal legacy 'Active' status left over from the old buggy unfreeze.
        # Must run after the allotments table has been created.
        cursor.execute("UPDATE allotments SET status = 'Issued' WHERE status = 'Active'")

        conn.commit()
        conn.close()
    
    def generate_project_code(self, project_name):
        """Generate 2-letter code from project name"""
        words = project_name.upper().split()
        if len(words) == 1:
            return words[0][:2]
        else:
            return ''.join([word[0] for word in words[:2]])
    
    def add_project(self, project_data):
        """Add new project to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        project_code = self.generate_project_code(project_data['project_name'])
        
        cursor.execute('''
            INSERT INTO projects (
                project_name, project_code, mahrera_no, survey_no, hissa_no,
                cts_no, final_plot_no, tps_details, plot_area, location,
                promoter_company, promoter_bank_name, promoter_account_name,
                promoter_account_no, promoter_branch, promoter_ifsc, cancellation_table,
                total_podiums
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            project_data['project_name'],
            project_code,
            project_data.get('mahrera_no', ''),
            project_data.get('survey_no', ''),
            project_data.get('hissa_no', ''),
            project_data.get('cts_no', ''),
            project_data.get('final_plot_no', ''),
            project_data.get('tps_details', ''),
            project_data.get('plot_area', ''),
            project_data.get('location', ''),
            project_data.get('promoter_company', ''),
            project_data.get('promoter_bank_name', ''),
            project_data.get('promoter_account_name', ''),
            project_data.get('promoter_account_no', ''),
            project_data.get('promoter_branch', ''),
            project_data.get('promoter_ifsc', ''),
            json.dumps(project_data.get('cancellation_table', [])),
            int(project_data.get('total_podiums', 0) or 0)
        ))
        
        conn.commit()
        project_id = cursor.lastrowid
        conn.close()
        
        # Create project folder
        folder_path = os.path.join("Allotment_Letters", project_data['project_name'])
        os.makedirs(folder_path, exist_ok=True)
        
        return project_id, project_code
    
    def get_all_projects(self):
        """Get all projects"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects ORDER BY created_date DESC')
        projects = cursor.fetchall()
        conn.close()
        return projects
    
    def get_project_by_id(self, project_id):
        """Get project details by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        project = cursor.fetchone()
        conn.close()
        return project
    
    def get_next_allotment_number(self, project_id):
        """Get next available allotment number for a project"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get project code
        cursor.execute('SELECT project_code FROM projects WHERE id = ?', (project_id,))
        project_code = cursor.fetchone()[0]
        
        # Get current financial year
        today = datetime.now()
        if today.month >= 4:  # April onwards
            fy = f"{str(today.year)[-2:]}-{str(today.year + 1)[-2:]}"
        else:
            fy = f"{str(today.year - 1)[-2:]}-{str(today.year)[-2:]}"
        
        # Check for cancelled/frozen allotments that can be reassigned
        cursor.execute('''
            SELECT allotment_sequence FROM allotments 
            WHERE project_id = ? AND financial_year = ? AND status = 'Cancelled'
            AND allotment_sequence < (
                SELECT MAX(allotment_sequence) FROM allotments 
                WHERE project_id = ? AND financial_year = ? AND status = 'Issued'
            )
            ORDER BY allotment_sequence ASC
            LIMIT 1
        ''', (project_id, fy, project_id, fy))
        
        cancelled = cursor.fetchone()
        
        if cancelled:
            # Reassign cancelled number
            sequence = cancelled[0]
        else:
            # Get max sequence number
            cursor.execute('''
                SELECT MAX(allotment_sequence) FROM allotments 
                WHERE project_id = ? AND financial_year = ?
            ''', (project_id, fy))
            
            max_seq = cursor.fetchone()[0]
            sequence = (max_seq or 0) + 1
        
        allotment_number = f"{sequence:02d}/{fy}/{project_code}"
        
        conn.close()
        return allotment_number, sequence, fy
    
    def add_allotment(self, allotment_data, allottees_data):
        """Add new allotment with allottees"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert allotment
        cursor.execute('''
            INSERT INTO allotments (
                project_id, allotment_number, allotment_sequence, financial_year,
                unit_type, unit_number, floor, wing, carpet_area_sqm, carpet_area_sqft,
                total_consideration, gst_amount, possession_date, booking_amount,
                payment_dates, payment_modes, parking_required, parking_type,
                parking_location, parking_size, status, issue_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            allotment_data['project_id'],
            allotment_data['allotment_number'],
            allotment_data['allotment_sequence'],
            allotment_data['financial_year'],
            allotment_data['unit_type'],
            allotment_data['unit_number'],
            allotment_data['floor'],
            allotment_data['wing'],
            allotment_data['carpet_area_sqm'],
            allotment_data['carpet_area_sqft'],
            allotment_data['total_consideration'],
            allotment_data['gst_amount'],
            allotment_data['possession_date'],
            allotment_data['booking_amount'],
            allotment_data.get('payment_dates', ''),
            allotment_data.get('payment_modes', ''),
            allotment_data.get('parking_required', 'No'),
            allotment_data.get('parking_type', ''),
            allotment_data.get('parking_location', ''),
            allotment_data.get('parking_size', ''),
            'Issued',
            allotment_data['issue_date']
        ))
        
        allotment_id = cursor.lastrowid
        
        # Insert allottees
        for allottee in allottees_data:
            cursor.execute('''
                INSERT INTO allottees (
                    allotment_id, name, address, phone, pan_card, aadhar_card,
                    email, bank_name, account_name, account_no, branch, ifsc
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                allotment_id,
                allottee['name'],
                allottee['address'],
                allottee['phone'],
                allottee['pan_card'],
                allottee['aadhar_card'],
                allottee['email'],
                allottee['bank_name'],
                allottee['account_name'],
                allottee['account_no'],
                allottee['branch'],
                allottee['ifsc']
            ))
        
        conn.commit()
        conn.close()
        return allotment_id
    
    def get_allotments_by_project(self, project_id):
        """Get all allotments for a project"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM allotments 
            WHERE project_id = ? 
            ORDER BY allotment_sequence DESC
        ''', (project_id,))
        allotments = cursor.fetchall()
        conn.close()
        return allotments
    
    def get_allottees_by_allotment(self, allotment_id):
        """Get all allottees for an allotment"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM allottees WHERE allotment_id = ?', (allotment_id,))
        allottees = cursor.fetchall()
        conn.close()
        return allottees
    
    def freeze_allotment(self, allotment_id):
        """Freeze an allotment (client backs out after issuing)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE allotments SET status = ? WHERE id = ?', ('Frozen', allotment_id))
        conn.commit()
        conn.close()
    
    def cancel_allotment(self, allotment_id):
        """Cancel an allotment (can be reassigned if no higher number issued)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE allotments SET status = ? WHERE id = ?', ('Cancelled', allotment_id))
        conn.commit()
        conn.close()
    
    def unfreeze_allotment(self, allotment_id):
        """Unfreeze an allotment (back to Issued)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE allotments SET status = ? WHERE id = ?', ('Issued', allotment_id))
        conn.commit()
        conn.close()

    def reactivate_allotment(self, allotment_id):
        """Bring a Cancelled allotment back to Issued.

        Refuses if the allotment's sequence number has been reassigned to another
        active allotment in the same project + financial year. Returns (ok, message).
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            'SELECT project_id, allotment_sequence, financial_year, status FROM allotments WHERE id = ?',
            (allotment_id,),
        )
        row = cursor.fetchone()
        if not row:
            conn.close()
            return False, "Allotment not found."

        project_id, sequence, fy, status = row
        if status != 'Cancelled':
            conn.close()
            return False, f"Allotment is not Cancelled (current status: {status})."

        cursor.execute(
            '''SELECT id FROM allotments
               WHERE project_id = ? AND financial_year = ? AND allotment_sequence = ?
                 AND id != ? AND status IN ('Issued', 'Frozen')''',
            (project_id, fy, sequence, allotment_id),
        )
        if cursor.fetchone():
            conn.close()
            return False, "This sequence number has already been reassigned to another active allotment."

        cursor.execute('UPDATE allotments SET status = ? WHERE id = ?', ('Issued', allotment_id))
        conn.commit()
        conn.close()
        return True, "Allotment reactivated."
    
    def delete_allotment(self, allotment_id):
        """Delete a single allotment and its allottees. Returns the allotment_number, or None if not found."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT allotment_number FROM allotments WHERE id = ?', (allotment_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        allotment_number = row[0]

        cursor.execute('DELETE FROM allottees WHERE allotment_id = ?', (allotment_id,))
        cursor.execute('DELETE FROM allotments WHERE id = ?', (allotment_id,))
        conn.commit()
        conn.close()
        return allotment_number

    def delete_project(self, project_id):
        """Delete a project and all its allotments + allottees. Returns (project_name, allotments_deleted)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT project_name FROM projects WHERE id = ?', (project_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None, 0
        project_name = row[0]

        cursor.execute('SELECT id FROM allotments WHERE project_id = ?', (project_id,))
        allotment_ids = [r[0] for r in cursor.fetchall()]

        if allotment_ids:
            placeholders = ','.join('?' for _ in allotment_ids)
            cursor.execute(
                f'DELETE FROM allottees WHERE allotment_id IN ({placeholders})',
                allotment_ids,
            )
            cursor.execute(
                f'DELETE FROM allotments WHERE id IN ({placeholders})',
                allotment_ids,
            )

        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        conn.commit()
        conn.close()
        return project_name, len(allotment_ids)

    def get_allotment_details(self, allotment_id):
        """Get complete allotment details with allottees"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM allotments WHERE id = ?', (allotment_id,))
        allotment = cursor.fetchone()
        
        cursor.execute('SELECT * FROM allottees WHERE allotment_id = ?', (allotment_id,))
        allottees = cursor.fetchall()
        
        conn.close()
        return allotment, allottees
