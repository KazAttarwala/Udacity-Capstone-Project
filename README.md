## Chitown Casting Agency 

# Motivation
This is a Flask Backend API with a React frontend to manage actors and movies in a casting agency. The motivation for this project was to demonstrate proficiency in building/deploying a Postgres-backed Flask web application with a user-friendly UI.

# Prerequisites
- Python3
- Pip
- Node
- Npm
- Postgres
- Venv

# Setting up Local Development
1. Clone the Github repo at https://github.com/KazAttarwala/Udacity-Trivia-Project.git
2. Create a virtual python environment by running `python3 -m venv env` in your native cli from the root directory. Afterwards, run `source env/bin/activate`; this will activate your virtual environment and provide a way to store your project dependencies.
3. Run `pip install -r requirements.txt` from the root directory of your cloned repo. This will pull in the required dependencies for the Flask API.
4. Open the models.py file in the root directory and comment out the code that sets the db path for Heroku (lines 13-15). Then uncomment the code that sets the local db path (lines 9 and 10). This will set up the path to your local postgres database.
5. Make sure your local Postgres server is running and run `createdb casting-agency` from your cli
6. Run `flask db upgrade` from the root directory. This will create the movie and actor tables in the casting-agency database.
7. Run the following commands from the root directory:
```
source setup.sh
export FLASK_APP=app.py
export FLASK_ENV=development
```
8. Run `flask run --reload`
9. Navigate into the frontend directory and open the package.json file. Scroll to the bottom of the file and change the proxy property to the url for your flask application. This ensures that api requests are routed to your local flask app instead of the production app on Heroku.
10. Run `npm install`.
11. Run `npm run start`. This will open a window to the React interface.
12. Start developing/testing the application!!!


# API Reference
- Click [here](https://chitown-casting.herokuapp.com) to visit the production app hosted on Heroku.
- The following table lists the available roles for people who work at Chitown Casting Agency, along with their credentials.
<br>
| Role | Username | Password |

| --- | --- | --- |     
     
| Casting Assistant | castingassistant@chitown.com | castingassistant#1 |
| Casting Director | castingdirector@chitown.com | castingdirector#1 |
| Executive Producer | execproducer@chitown.com | execproducer#1 |

- The following table lists what actions each role can perform.
| Role                   | Actions  | 

| ----|-------|         
| Casting Assistant      | Read from actors and movies                                               |
| Casting Director       | Casting Assistant actions + add/delete actors + update actors and movies  |
| Executive Producer     | Casting Director actions + add/delete movies                              | 

- Logging in sends a request to the Auth0 authentication service for the JWT token. To access the token, open a Chrome Dev Tools window and log in as one of the roles. Go to the Network tab on the Dev Tools window, locate the request to Auth0, and copy the token from the Response tab. You must use this token 

## Error Handling
Errors are returned as JSON objects
-General errors:
```
{
    "success": False, 
    "error": 500,
    "message": "Something went wrong! Please try again."
}
```
-Authentication errors:
```
{
    "code": "authorization_header_missing", 
    "description": "Authorization header is expected"
}
```
-Error types:
  - 400: bad request
  - 404: not found
  - 422: unprocessable 
  - 500: server error

## Endpoints 
GET /movies
- Returns a list of movies
- Sample Request: 
curl https://chitown-casting.herokuapp.com/movies --header 'authorization: Bearer insert_token_here'
-Sample Response:
```
{
   "movies":[
      {
         "id":4,
         "release_date":"08/20/2021",
         "title":"Sweet Girl"
      }
   ]
}
```

GET /movies/{movie_id}
-Returns the specified movie
-Sample Request:
curl https://chitown-casting.herokuapp.com/movies/4 --header 'authorization: Bearer insert_token_here'
-Sample Response:
```
{
   "movie":
   {
      "id":4,
      "release_date":"08/20/2021",
      "title":"Sweet Girl"
   }
}
```

GET /actors
-Returns a list of actors
-Sample Request:
curl https://chitown-casting.herokuapp.com/actors --header 'authorization: Bearer insert_token_here'
-Sample Response:
```
{
   "actors":[
      {
         "age":42,
         "gender":"Male",
         "id":5,
         "name":"Jason Momoa"
      },
      {
         "age":20,
         "gender":"Female",
         "id":6,
         "name":"Isabella Merced"
      }
   ]
}
```

GET /actors/{actor_id}
-Returns the specified actor
-Sample Request:
curl https://chitown-casting.herokuapp.com/actors/6 --header 'authorization: Bearer insert_token_here'
-Sample Response:
```
{
   "actor":
   {
      "age":20,
      "gender":"Female",
      "id":6,
      "name":"Isabella Merced"
   }
}
```

POST /movies
-Adds a new movie
-Sample Request:
curl https://chitown-casting.herokuapp.com/movies -X POST --header 'authorization: Bearer insert_token_here' --header 'Content-Type: application/json' -d '{"title":"Black Widow", "release_date":"2021/07/09"}'
-Sample Response:
```
{
    "success": true
}
```

POST /actors
-Adds a new actor
-Sample Request:
curl https://chitown-casting.herokuapp.com/actors -X POST --header 'authorization: Bearer insert_token_here' --header 'Content-Type: application/json' -d '{"name":"Scarlet Johansson", "gender":"Female", "age": 36}'
-Sample Response:
```
{
    "success": true
}
```

PATCH /movies/{movie_id}
-Updates a movie
-Sample Request:
curl https://chitown-casting.herokuapp.com/movies/4 -X PATCH --header 'authorization: Bearer insert_token_here' --header 'Content-Type: application/json' -d '{"title":"Black Swan", "release_date":"2010/12/03"}'
-Sample Response:
```
{
    "success": true
}
```

PATCH /actors/{actor_id}
-Updates an actor
-Sample Request:
curl https://chitown-casting.herokuapp.com/actors/9 -X PATCH --header 'authorization: Bearer insert_token_here' --header 'Content-Type: application/json' -d '{"name":"Natalie Portman", "age":40, "gender": "Female"}'
-Sample Response:
```
{
    "success": true
}
```

DELETE /movies/{movie_id}
-Deletes the specified movie
-Sample Request:
curl https://chitown-casting.herokuapp.com/movies/4 -X DELETE --header 'authorization: Bearer insert_token_here'
-Sample Response:
```
{
    "success": true
}
```

DELETE /actors/{actor_id}
-Deletes the specified actor
-Sample Request:
curl https://chitown-casting.herokuapp.com/actors/6 -X DELETE --header 'authorization: Bearer insert_token_here'
-Sample Response:
```
{
    "success": true
}
```

## Testing
To run the tests, run the following commands from the root directory (make sure you are in your virtual environment)
```
source setup.sh
dropdb casting-agency-test
createdb casting-agency-test
psql casting-agency-test < casting-agency.psql
python test_flaskr.py
```


