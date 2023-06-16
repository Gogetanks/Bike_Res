# Bike Reservation System
Python version: 3.10.7

Django version: 4.1.5


Known Issues:

Hong 2023-04-03:
    All changes to user groupings on django's admin site results in integrity errors with failed FOREIGN KEY constraints. I tested with many different implementations of the grouping structures and tried to manually modify the database, but none of them worked. I think the cause might be the django's admin site implementations conflicting with our db schema so there will probably be no fix.
    As for now, the work around is to use management command scripts (as exampled in bike/management/commands) or use similar codes in other files and run them.
    Later if necessary, we can add our own admin page.