# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Endpoints
GET /categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

GET /questions
- Fetches paginated questions in the groups of 10 questions per page.
- Request Arguments: page /questions?page=1 - In case /questions, default is 1
- Returns: An object with questions for the page specified in the request along with categories and total number of questions
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "success": true, 
  "total_questions": 20
}
```

DELETE /questions/<int:question_id>
- Delete a specific question based on it's id
- Request Arguments: None
- Returns: An object with deleted question's id.

```json
{
  "deleted": 4, 
  "success": true, 
}
```

GET /categories/<int:category_id>/questions
- Fetches paginated questions in the groups of 10 questions per page filtered by category.
- Request Arguments: page /categories/1/questions?page=1 - In case /categories/1/questions, default is 1
- Returns: An object with questions for the page specified in the request along with current category and total number of questions
```json
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

POST /questions
- Searches the database for questions containing the term provided as part of request payload
- Request Payload: Takes a json object with a property searchTerm which holds a string for searching the questions containing that search term
```json
{
    "searchTerm":"who"
}
```
- Returns: An object with a list of questions macthing the search term along with categories they belong to and total number of questions.
```json
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}
```

POST /questions
- Creates a new question in the database based on the request payload
- Request Payload: A JSON object containing question text, answer text, difficulty number and category id
```json
{
  "question": "Indian national anthem was composed by",
  "answer": "Rabindranath Tagore",
  "difficulty": "2",
  "category": "4"
}
```
Returns: success as true.
```json
{
  "success": true
}
```
  
POST /quizzes
- Fetches questions to play the quiz.
- Takes category and previous question parameters
- Returns a random questions within the given category and which is not one of the previous questions
- Request Payload: list of ids of previous questions and quiz category object
```json
{
  "previous_questions": [
    23
  ],
  "quiz_category": {
    "type": "History",
    "id": "4"
  }
}
```
- Returns: An object with question
```json
{
  "question": {
    "answer": "Muhammad Ali", 
    "category": 4, 
    "difficulty": 1, 
    "id": 9, 
    "question": "What boxer's original name is Cassius Clay?"
  }, 
  "success": true
}
```


Errors
404 RESOURCE NOT FOUND
```json
{
    "message": "resource not found",
    "success": false
}
```
500 INTERNAL SERVER ERROR
```json
{
    "message": "internal server error",
    "success": false
}
```
400 BAD REQUEST
```json
{
    "message": "bad request",
    "success": false
}
```
405 METHOD NOT ALLOWED
```json
{
    "message": "method not allowed",
    "success": false
}
```
422 UNPROCESSABLE
```json
{
    "message": "unprocessable",
    "success": false
}
```



## Testing
To run the tests, run
```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```

