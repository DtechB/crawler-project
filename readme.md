# Alpha Project - Subdomain finder, Crawler and find broken links

This is the undergraduate project of Mr. Daniyal Bayati and myself, who have developed this project in cooperation with each other.<br />
The description of this project is as follows:<br />
First, an internet address or link is taken from the user. Then its subdomains are checked first. The subdomains are checked based on a huge dictionary that consists of different possible types of words and phrases. (Also, this process is done using multi-threads in programming so that the checking time can be saved).<br />
After finding subdomain links, SSL certificates of these subdomains are checked. In this process, the details of the prepared SSL certificate are checked by using information databases and checking existing certificates.<br />
In the next step, the crawler comes into action and starts crawling all the links on the pages. This crawler is designed so that it can crawl up to several levels of the site. The description of the crawling process is like this, first the links on the main page are received, the crawler divides these links into internal and external categories. External links that are no longer related to the desired site are separated using its base link and there is no need to crawl more in that link!<br />
Internal links, which are a subset of the site, are crawled again as in the previous step and form a tree, the root of each node being the link on the first crawled page.<br />
Also, if we have a link that is duplicated during the crawling process, it will not be saved and crawled again for optimal performance.<br />

**NOTE:**
You can use any part of the project that has been implemented in a modular way. Each of these facilities are implemented completely separately in the <strong>modules</strong> folder.

---

<details>
<summary>Installation</summary>
To install and start working with this project, you must first install Python.
You can download and install the latest version of Python from the:
<a href="https://www.python.org/downloads">Downlaod Python</a>

**NOTE:**
For better compatibility of the program and to avoid errors, it is recommended to install a version before the latest version, because some modules used in the project may not be compatible with the new version of Python and this causes interference. Let it be!

---

<br />

After installing Python, you need to install Django:
If you have a Linux operating system, you can use this command:
```bash
python -m pip install Django
```
And if you have a Windows operating system, using this command:
```bash
py -m pip install Django
```
You can install the latest version of Django on your system.


---

<br />

In the next step, you need to install the Postgres database, to install this database you can install the latest version using the following link:
<a href="https://www.postgresql.org/download">Downlaod PostgreSQL</a>
<br />
Note: You can also use your favorite database, for example sqlite3 or Mysql, but for this you need to modify the parts related to connecting to the database and tables again!


---

<br />

From now on, your work will be easy! You can create a Python virtual environment using the following command:
```bash
python -m venv venv
```
Note: The last argument used in the command is the name of the folder for which it is created!

and activate it using the following command in the Windows environment:

```bash
.\venv\Scripts\activate
```

Or use the following command to activate it in the Linux environment:
```bash
source venv/bin/activate
```
Note: Be aware that when you type this command, the name of the folder you created for the virtual environment must be venv and you must be in its parent folder.

After activating the virtual environment, use the following command to install all the packages needed to use this program at once:
```bash
pip install -r requirements.txt
```
Note: Like the previous command, you must use this command in a place where the requirements.txt file is available.


---

<br />

If you want to use the postgresql database, you need to install its special module to connect to the database. To install this module, you can use the following command:
```bash
pip install postgres
```
And also the command:
```bash
pip install psycopg2
```

If you want to use the postgresql database, you need to install its special module to connect to the database. To install this module, you can use the following command:
```bash
pip install mysql-connector-python
```
</details>
<details>
<summary>Usage</summary>

To use this program, you can easily go through three processes after going through the steps mentioned in the installation section

Apply the approved changes to the database using the following command:
```bash
python manage.py makemigrations
```

And then send the files to the server using the following command:
```bash
python manage.py migrate
```

And finally run the program with the following command:
```bash
python manage.py runserver
```
</details>

<details>
<summary>Contributing</summary>
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
Please make sure to update tests as appropriate.
</details>

<details>
<summary>License</summary>
Copyright (C) 2023 <a href="https://github.com/DtechB">Danial Bayati</a> and <a href="https://github.com/MosFazli">Mostafa Fazli</a> - All rights reserved <br />
Licenced By <a href="https://choosealicense.com/licenses/mit/">MIT</a>
</details>

## API Description:
### Get Subdomains

For getting all subdomains advanced, you can use this structure:<br />
GET Request: http://127.0.0.1:8000/subdomains/

### Get SSLs

For getting all ssls, you can use this structure:<br />
GET Request: http://127.0.0.1:8000/ssls/