# FastAPI-ReactJS-SmartTrade
# PSW-DDS-Project-11.01

Final project for UPV assignatures: PSW & DDS. 
Team 11.01 - Los Pachangas

## Backend setup:

1. Database setup:
Create a `.env` file inside the `Back` directory and paste the following:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=database
DB_USER=postgres
DB_PASSWORD=password
DB_URL=postgresql+psycopg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
```
Customize it with your own postgre's database credentials, but do not modify `DB_URL`.

2. Execute the `create_tables` file:
```
python Back/app/create_tables.py
```

4. In order to start the backend server, run:
```
python Back/app/main.py
```

## Frontend setup

To configure React App frontend:
1. install Nodejs if you haven't already.
2. install npm.
3. Go to '../PSW-DDS-Proyect-11.01/Front' in your console
4. execute ```npm install --force```. This command will install you all the dependeces the proyect has.

To execute React App
1. First go to '../PSW-DDS-Proyect-11.01/Front' in your console
2. Execute ```npm start```
