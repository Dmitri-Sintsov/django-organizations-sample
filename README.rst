===========================
django-organizations-sample
===========================

Before running::

    pip3 install -r requirements.txt
    rm db.sqlite3
    python3 manage.py makemigrations org_permissions
    python3 manage.py migrate
    python3 manage.py create_organizations_permissions
