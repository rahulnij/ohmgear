Installation of kinbow application on server:

1) Create the virutal env:
   
   mkvirtualenv kinbow

2) Now install the packages in this env :

   pip install -r requirements/base.txt  -- file name will change according envionment   
   
3) Create all tables in database according env setting :

   ./manage.py migrate --run-syncdb --settings='ohmgear.settings.dev' or  --settings='ohmgear.settings.aws' according server

4) Now insert initial data for table:

   ./manage.py loaddata default  --settings='ohmgear.settings.dev'  
   ./manage.py loaddata usersetting  --settings='ohmgear.settings.dev'  
   ./manage.py loaddata feedback  --settings='ohmgear.settings.dev'   

   


