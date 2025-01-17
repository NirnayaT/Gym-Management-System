
# Gym Management System

A modern desktop application for managing gym operations efficiently. Built with Python and Tkinter, this system provides a clean interface for handling members, payments, attendance, and generating insightful reports.

## Features

- **Member Management**
  - Add, update, and delete member profiles
  - Track membership types and status
  - Real-time search functionality
  - Detailed member history

- **Payment Tracking**
  - Record and manage payments
  - Multiple payment types support
  - Payment history with filtering
  - Financial reporting

- **Attendance System**
  - Check-in/Check-out functionality
  - Attendance history
  - Duration tracking
  - Daily attendance reports

- **Reports & Analytics**
  - Attendance trends visualization
  - Membership plan distribution
  - Payment analysis charts
  - Exportable reports

## Project Structure
```
Gym-Management-System/
│
├── database/
│   ├── __init__.py
│   ├── excel_handler.py
│   └── gym_database.xlsx
│
├── ui/
│   ├── __init__.py
│   ├── root_ui.py
│   ├── members_ui.py
│   ├── payments_ui.py
│   ├── attendance_ui.py
│   └── reports_ui.py
│
├── utils/
│   ├── __init__.py
│   ├── assets.py
│   ├── constants.py
│   ├── theme.py
│   └── validators.py
│
├── logs/
│   ├── gym_management.log
│   
├── assets/
│   ├── images/
│   │   ├── logo.png
│   │   ├── background.png
│   │   └── user_avatar.png
│   └── icons/
│       ├── members.png
│       ├── payments.png
│       ├── attendance.png
│       └── reports.png
│
├── main.py
├── requirements.txt
└── gym_management.log

```

## Technical Requirements

- Python 3.8+
- Required packages:
  - tkinter
  - pandas
  - matplotlib
  - openpyxl
  - others inside requirements.txt

## Installation
1. Clone the repository
```bash
git clone https://github.com/NirnayaT/Gym-Management-System
```
2. Create a virtual environment
```bash
python -m venv venv
```
3. Activate virtual environment
```bash
venv\Scripts\activate
```

4. Install dependencies
```bash
pip install -r requirements.txt
```
5. Run the application
```bash
python main.py
```
## System Requirements
- Operating System: Windows/Mac/Linux
- Python 3.8+
- RAM: 4GB minimum recommended
- Storage: 500MB free space
- Display: 1024x768 minimum resolution

## Database Structure
### Excel Sheets Layout
- Members Sheet: member_id, name, contact, email, membership_type, joining_date, status
- Payments Sheet: payment_id, member_name, amount, payment_date, payment_type, status
- Attendance Sheet: id, member_id, check_in, check_out, date, duration

### Backup Procedures
- Database Location: database/gym_database.xlsx
- Recommended backup frequency: Daily
- Backup path: Create 'backups' folder in root directory

## Security Features
- Data Storage: Local Excel database
- Access Control: Single admin interface
- Data Validation: Input verification for all forms
- Error Handling: Comprehensive error logging

## Troubleshooting Guide
Common Issues:
1. Database Access Error
   - Verify database/gym_database.xlsx exists
   - Check file permissions
   
2. Image Loading Issues
   - Confirm assets/images/ directory contains required images
   - Verify image file names match code references

3. Report Generation Errors
   - Ensure matplotlib and pandas are properly installed
   - Check write permissions for export directory

## Configuration
### Theme Customization
- Color scheme defined in utils/theme.py
- Font settings configurable in GymTheme class
- Button styles customizable via ttk styles

### Database Configuration
- Default path: database/gym_database.xlsx
- Logs path: logs/gym_management.log
- Assets path: assets/images/

## Performance Optimization
- Regular database maintenance recommended
- Clear old logs periodically
- Optimize image sizes in assets folder
- Regular data backup implementation

## User Interface
### Main Features
- Clean, intuitive navigation
- Responsive form controls
- Real-time search functionality
- Interactive data visualization

### Data Management
- Efficient member tracking
- Automated payment recording
- Attendance monitoring
- Dynamic report generation

## Usage

### Members
- **Adding New Members**
  - Click on "Add Member" button
  - Fill in required fields: Name, Contact, Email, Membership Type
  - Submit to add member to database
  - System automatically assigns member ID

- **Updating Members**
  - Select member from the list
  - Modify desired information
  - Click "Update" to save changes
  - Real-time database update


- **Member Status**
  - View active/inactive status
  - Check membership duration
  - Monitor membership type
  - Track joining date

### Payments
- **Recording Payments**
  - Select member from dropdown
  - Enter payment amount
  - Choose payment type
  - Click "Add Payment" to record

- **Payment Tracking**
  - View all transactions
  - Filter by date range
  - Sort by payment type
  - Check payment status

- **Payment Reports**
  - Generate detailed reports
  - View payment summaries
  - Analyze payment trends
  - Track revenue statistics

- **Data Export**
  - Export to Excel format
  - Save payment history
  - Download detailed reports
  - Backup payment data

### Attendance
- **Check-in/Check-out**
  - Select member name
  - Click "Check In" for entry
  - Click "Check Out" when leaving
  - System records timestamps

- **Attendance History**
  - View daily attendance
  - Check member frequency
  - Track timing patterns
  - Monitor attendance trends

- **Duration Tracking**
  - Automatic duration calculation
  - View session lengths
  - Track workout times
  - Monitor facility usage

- **Attendance Reports**
  - Generate daily reports
  - View monthly summaries
  - Analyze peak hours
  - Track member regularity

### Reports
- **Attendance Analysis**
  - View daily trends
  - Track peak hours
  - Monitor member frequency
  - Analyze patterns

- **Membership Overview**
  - Plan distribution charts
  - Member growth trends
  - Active member ratio
  - Plan popularity analysis

- **Payment Analytics**
  - Revenue trends
  - Payment method distribution
  - Monthly comparisons
  - Financial forecasting

- **Export Options**
  - Excel reports
  - PDF generation
  - Data visualization
  
## License

This project is under Nirnaya's Group.

## Acknowledgments

### Modern UI Design Principles
- Clean and minimalist interface
- Consistent typography and spacing  
- Intuitive navigation flow

### Data Visualization Best Practices
- Clear and readable charts
- Meaningful data representation
- Interactive graphical elements

### Efficient Database Management
- Optimized data storage
- Fast query processing
- Data integrity maintenance 

### User-Friendly Interface Design
- Responsive controls
- Real-time search functionality
- Streamlined workflows

