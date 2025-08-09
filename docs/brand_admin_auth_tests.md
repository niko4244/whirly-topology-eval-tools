# Tests: Admin Authentication and Secure Reports

## What is tested

- **Admin dashboard and report download endpoints** require admin login.
- **Technician login** cannot access admin dashboard or reports.
- **Technician upload page** requires login.
- **Secure CSV downloads:** Only admin can download leaderboard, badge events, feedback reports.

## Example Results

- Unauthenticated user redirected to login for admin/upload.
- Technician denied admin access.
- Admin can access dashboard and download all reports.

## Compliance

- Prevents unauthorized access to sensitive analytics and engagement data.
- Ensures business and privacy compliance for brand-filtered reporting.

---