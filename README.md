# Trading App - Django REST Framework

This Repo contains APIs of Trade App.

## Prerequisites
- [Docker](https://docs.docker.com/install/)

## Commands
To use this project, run this commands:

1. `make up` to build the project and starting containers.
2. `make build` to build the project.
3. `make start` to start containers if project has been up already.
4. `make stop` to stop containers.
5. `make restart` to restart containers.
5. `make run` to build the project and starting containers in background.

## To get up and running

1. `git clone` this repository && `cd` into the project directory.
2. run command `make build` to build the project.
3. run command `make up` to start docker container.
4. Test apis on [localhost](http://0.0.0.0:8000/api/)

## APIs
| Name | End Point | Request Type | Body | Description |
|------|-----------|--------------|-------|-------------|
| Registration | /api/register | POST |  {<br>  "username": "XXXX",<br>  "email": "XXXX",<br>  "password": "XXXX" <br>} | User Registration |
| Login | /api/login | POST |   {<br>  "username": "XXXX",<br>  "password": "XXXX" <br>} | User Login |
| Add Bond | /api/add-bond | POST |   {<br>  "bond_type": "XXXX",<br>  "no_of_bonds": "XXXX" <br> "password": "XXXX"<br>} | To add new Bond, All fields are Required |
| Get List of Bonds | /api/add-bond | GET | | To get list of all Bond. |
| Get a Bond | /api/bonds/:id | GET | | To get a Bond by bond id. |
| Puchase Bond | /api/bonds/:id | PUT | | To purchase a bond. |
| USD Rate | /api/usd-rate/ | PUT | | To get bond price in current USD rates. |