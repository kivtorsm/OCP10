# OCP10 : SoftDesk

Projet OpenClassrooms - Programme développeur d'applications Python

**Objectif** : Create API for issue management software back-end.

## Functions
- Sign-up, Log-in (get token), Refresh token
- Projects : get list, create, get detail, update, delete
- Project Issues : get list, create, get detail, update, delete
- Project Comments : get list, create, get detail, update, delete
- Project users : get list, create, get detail, update, delete
- 

## Installing and running

### 1. Install Software requirements
- Install Python 3.11+

### 2. Create Python project environment
1. In your terminal/IDLE, position yourself in the directory where you want
to create your project folder
```shell
$ cd //path//
```

2. Create your project folder 
```shell
$ mkdir *Project_Name*
```

3. Create your project environment 
```shell
$ python -m venv env
```

### 3. Activate virtual environment
- From your project folder (this commande may change depending on your OS):
```shell
$ ./env/Scripts/activate
```

### 4. Install Pyhton packages
- From your terminal or IDLE, install all packages listed in requirements.txt
```shell
$ pip install -r requirements.txt
```

### 5. Create database
- You can use existing example database provided :
`db.sqlite3`
- Or you can create a new database. From your terminal or IDLE, from the manage.py location folder, migrate DB:```shell
```shell
$ python manage.py migrate
```

### 6. Run Server
- From your terminal or IDLE, from the manage.py location folder, migrate DB:
```shell
$ python manage.py runserver
```

### 7. Navigate
- Go to your favorite API browser and consult any API endpoint on :
```text 
https//:127.0.0.1:8000/api/
```

## API Documentation 
Extensive API documentation can be found on:
[SoftData API Documentation](https://documenter.getpostman.com/view/26004028/2s93m91MSx)

## Test Data

### Users
| username       | Password        | Contributor to project |
|----------------|-----------------|------------------------|
| ocp10          | ocp10SoftDesk   | 2                      |
| ocp10_postman  | opc10SoftDesk   | 2                      |
| ocp10_postman2 | opc10SoftDesk   | 2                      |

### Database
Initialised data in `db.sqlite3`


