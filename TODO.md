# TODO List for Admin Panel Implementation

## 1. Add CompanyType Model
- [x] Edit `clientes/models.py` to add CompanyType model.
- [x] Update Cliente model to use CompanyType foreign key instead of CharField for empresa.

## 2. Create Admin Views
- [x] Edit `clientes/views.py` to add views for user management and company type management.
- [x] Ensure views are protected with @user_passes_test for superusers.

## 3. Update URLs
- [x] Edit `clientes/urls.py` to add URLs for admin panel.

## 4. Update Templates
- [x] Create templates for admin panel: user list, company type list, etc.
- [x] Edit `templates/base.html` to add admin link in navbar if user.is_superuser.

## 5. Register Models in Admin
- [x] Edit `clientes/admin.py` to register CompanyType and customize User admin.

## 6. Run Migrations
- [x] Execute `python manage.py makemigrations` and `python manage.py migrate`.
- [ ] Note: Migrations and superuser creation failed due to PostgreSQL connection issues. User needs to fix database connection first.

## 7. Create Superuser
- [ ] Execute `python manage.py createsuperuser --username admin --email fonsecasteep@gmail.com` and set password to 1234567890.
- [ ] Note: Superuser creation failed due to database connection issues.

## 8. Test Admin Panel
- [ ] Verify that only superusers can access the admin panel.
- [ ] Check user management and company type management functionality.
- [ ] Note: Testing requires database connection to be fixed.
