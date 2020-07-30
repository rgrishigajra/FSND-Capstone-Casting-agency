# Full Stack Casting Agency API Backend

## Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Motivation for project

This is the capstone project of Udacity fullstack nanodegree program, which demonstrate the skillset of using Flask, SQLAlchemy, Auth0, gunicorn and heroku to develop and deploy a RESTful API.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:

```bash
psql casting_agency<casting_agency.psql
```

more info here:
https://www.linode.com/docs/databases/postgresql/how-to-back-up-your-postgresql-database/#:~:text=PostgreSQL%20provides%20the%20pg_dump%20utility,you%20intend%20to%20back%20up.&text=Dump%20the%20contents%20of%20a,database%20to%20be%20backed%20up.

## Running the server

From within the directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
. ./setup.sh
flask run
```

#### Flask run tests the token headers set for the enviroment. If they have expired, you need to login using the crededntials below and replace them in setup.sh and run setup.sh again

setup.sh has all the environment variables needed for the project. The app may fail if they are not set properly. If that happens just copy paste lines from setup.sh on you CLI.

# Project deployed at

https://fsnd-casting-agency-udacity.herokuapp.com/

###### To test live APIs the only way right now to do this is curl requests. Add Auth token headers from logins below to test.

OATH login url

```
https://dev-fc34y9lq.us.auth0.com/authorize?audience=CastingAgencyAPI&response_type=token&client_id=XeqwOu6PsAeC0bwm2dd6giNP0JJaaxIe&redirect_uri=http://localhost:8080/login-results
```

casting Assistant token castingassistant@example.com Qwerty1234

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJWRXNSUnYwWUZRUDdtU3g5VGJ0TSJ9.eyJpc3MiOiJodHRwczovL2Rldi1mYzM0eTlscS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMjAzYzNjMTNiMTMwMjI4ZjgxM2FhIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeUFQSSIsImlhdCI6MTU5NjE0MTQ2NSwiZXhwIjoxNTk2MjI3ODY0LCJhenAiOiJYZXF3T3U2UHNBZUMwYndtMmRkNmdpTlAwSkphYXhJZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.U39-EK_wkLbqrUnfsTWb7ih1Djn9L30GwdZwanfKVNyXIsa9BDcxd5yUxH8HD_owfAZWxcqqf2hCjJ_wcQDhuFD_Z8jDYvECtFx_KYWncmf2P4vhm_mNf6ENS2Hi2nNUV6YE7X4Mv3rsktI3GrZFppiMVKfNODRf3EbfAOw5VwqQCE8u3Paiurfyoya7frltSOeuf8pU6o3hVkJXwPSlnpN6Rvos_JL1JvodoZFJQJmtWn4CObJ-Nut-17aFjH1gm9ZsZzUfq-ECfcD74e7RKU28y_Rw_0BS6nFO9OVFVJGHuT3JyoCfxfuneNr5Ao6RYedGBqAw4R5l6TtQuxKQhw

```

Casting director token castingdirector@example.com Qwerty1234

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJWRXNSUnYwWUZRUDdtU3g5VGJ0TSJ9.eyJpc3MiOiJodHRwczovL2Rldi1mYzM0eTlscS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMjA2MjI1Yzg0OGYwMDM3YzQxNTJmIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeUFQSSIsImlhdCI6MTU5NjE0MTU2MCwiZXhwIjoxNTk2MjI3OTU5LCJhenAiOiJYZXF3T3U2UHNBZUMwYndtMmRkNmdpTlAwSkphYXhJZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.Zf0BsuoZdBFrkHjIEuPDW5Udt6aJn6qUMWIDpOaoTBxhALV2wRt1aV9qMn9PHihG8RZ_N8rEjpOm6AJGzT-MsDfKUTuF0Ah7CAME8hJ_AdWR0egsjoqb7bosn-cu6VSQNtb7O039dOgm0uX23G95nrbobbfeLg8S3ipSmsyO3IB1B78ebV2NCM8J64DXMCsQwvkJl4OKsNjc0nzxBk6fcjVVkUfftZJW45V6H-NU8Ljc15At1lxQ4SRbdQ3AEpH9lbptCKpKGY-QdAeEgD_gP3uffJbIGfjPEDWy-NMRTt-2ika134hnDvTXEspALVAKHchcp6pRw9pMr8LFmRvLPA

```

Executive Producer executiveproducer@example.com Qwerty1234

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJWRXNSUnYwWUZRUDdtU3g5VGJ0TSJ9.eyJpc3MiOiJodHRwczovL2Rldi1mYzM0eTlscS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyMjRkNGQ1Yzg0OGYwMDM3YzQxNzFkIiwiYXVkIjoiQ2FzdGluZ0FnZW5jeUFQSSIsImlhdCI6MTU5NjE0MTUwNCwiZXhwIjoxNTk2MjI3OTAzLCJhenAiOiJYZXF3T3U2UHNBZUMwYndtMmRkNmdpTlAwSkphYXhJZSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.BgIe6xAaR5YqxM7j0NFjjLLctZnAKIp2x_q93sZPH8rBkCp3HjSDRLlqmz0KyeEwPyBMjLxQabbr3InJQk8OTq8S7rjoepgPs_zHF3mJrjUqZ3V3JaRX5_IvDf5J_-PfV-I6vxz42q1Mb1wMTBOHxOxj7MvtZ0JSycNGy3aRg1h0RsslV1Zyrcsx5cWk6xstpBylBEhaOTwbqHQTWZklWDE2eRnRAC3YYWrHpIy_xepcn8HNxfBoIFWr11SYxGMkYXEMqRDbQ8UqnUcUpOzxqMJXG913cf9YZegljhEiyZwPtsdlW92KNLNYKkLEPbTPXBwEQl_UmsD769fKc_egvA
```

## Testing

To run the tests, run

```
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test<casting_agency_test.psql
python test_flaskr.py
```

The tests print data returned from the APIs along with API logs.

#### The rests also use the Auth token set in env variables and will give an error if the tokens are expired.

## API Reference

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}

```

### Endpoints

GET '/actors'
POST '/actors'
PATCH '/actors/<actor_id>'
DELETE '/actors/<actor_id>'
GET '/movies'
GET '/actors'
POST '/actors'
PATCH '/actors/<actor_id>'
DELETE '/actors/<actor_id>'

GET '/movies'
Fetches an array of movies
Required URL Arguments: None
Required Data Arguments: None
Returns: Returns Json data about movies
Success Response:

```
{
   "movies":[
      {
         "genre":"SuperHero",
         "id":9,
         "release_date":"2019-01-02",
         "title":"Avengers"
      },
      {
         "genre":"SuperHero",
         "id":10,
         "release_date":"2019-01-02",
         "title":"Avengers"
      }
   ],
   "success":True
}
```

GET '/actors'
Fetches an array of actors
Required Data Arguments: None
Returns: Json data about actors
Success Response:

```
  {
   "actors":[
      {
         "age":22,
         "gender":"male",
         "id":10,
         "name":"rish"
      }
   ],
   "success":True
}
```

DELETE '/movies/<int:movie_id>'
Deletes the movie_id of movie
Required URL Arguments: movie_id: movie_id_integer
Required Data Arguments: None
Returns: deleted movie's ID
Success Response:

```
{'deleted': 8, 'success': True}
```

DELETE '/actors/<int:actor_id>'
Deletes the actor_id of actor
Required URL Arguments: actor_id: actor_id_integer
Required Data Arguments: None
Returns:the deleted actor's ID
Success Response:

```
{'deleted': 9, 'success': True}
```

POST '/movies'
Post a new movie in a database.
Required URL Arguments: None
Required Data Arguments: Json data
Success Response:

```
{'movie_id': 11, 'success': True}
```

POST '/actors'
Post a new actor in a database.

Required URL Arguments: None

Required Data Arguments: Json data

Success Response:

```
{'actor_id': 11, 'success': True}
```

PATCH '/movies/<int:movie_id>'
Updates the movie_id of movie
Required URL Arguments: movie_id: movie_id_integer
Required Data Arguments: None
Returns: Json data about the updated movie
Success Response:

```
{
   "movie":{
      "genre":"SuperHero",
      "id":9,
      "release_date":"2019-01-02",
      "title":"Avengers 2"
   },
   "success":True
}
```

PATCH '/actors/<int:actor_id>'
Updates the actor_id of actor
Required URL Arguments: actor_id: actor_id_integer
Required Data Arguments: None
Returns: Json data about the modified actor's ID
Success Response:

```
{
   "actor":{
      "age":22,
      "gender":"male",
      "id":10,
      "name":"gopi"
   },
   "success":True
}
```

## Authors

Rishabh Gajra and The udacity team that made the starter code and Project tasks.
