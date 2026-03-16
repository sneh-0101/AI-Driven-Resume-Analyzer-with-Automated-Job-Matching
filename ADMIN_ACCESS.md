# Admin Page Access Guide

To access the admin page of your Resume Builder application, follow these steps:

### 1. Identify the Admin URL
The admin dashboard is located at:
`http://localhost:5000/admin/`

### 2. Login Credentials
**IMPORTANT:** You must use the **Email Address** (not username) and the password below:

**Option A:**
- **Email:** `admin@demo.com`
- **Password:** `admin123`

**Option B:**
- **Email:** `admin@example.com`
- **Password:** `admin123`

### 3. Verification of Admin Status
The admin page is protected and requires a user account with the `is_admin` flag set to `True`.
If you need to create a new admin account or reset the existing one, you can run the following script from your terminal:

```powershell
python create_admin.py
```

### 4. Database Check (Optional)
You can verify existing admin users by running your `check_admin.py` script:
```powershell
python check_admin.py
```

Currently, the following admin users exist in your database:
- `admin` (`admin@example.com`)
- `demo_admin` (`admin@demo.com`)
