.. _django-organizations: https://github.com/bennylope/django-organizations
.. _django-organizations-permissions: https://github.com/Dmitri-Sintsov/django-organizations-permissions

===========================
django-organizations-sample
===========================

Sample to use custom auth backend / DRF Permissions class from `django-organizations-permissions`_ with `django-organizations`_.

Before running::

    python3 -m pip install -r requirements.txt
    rm db.sqlite3
    python3 manage.py makemigrations org_permissions
    python3 manage.py migrate
    python3 manage.py create_organizations_permissions
