#---------Imports-----------
import os
from flask import Flask, request, abort, jsonify

from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
def paginate_questions(request,selection):
  page = request.args.get("page",1,type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app,resources={r"/api/*": {"origins": "*"}})
  
  '''
  Set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Origin","*")
    response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods","GET,PUT,POST,DELETE,OPTIONS")
    return response

  '''
  Endpoint to handle GET requests for all available categories.
  '''
  @app.route("/categories", methods=['GET'])
  def available_categories():
    try:
      categories = Category.query.order_by(Category.id).all()
      if len(categories) == 0:
        abort(404)
      return jsonify({
        "success":True,
        "categories": { category.id : category.type for category in categories }
      })
    except:
      abort(405)

  '''
  Endpoint to handle GET requests for questions
  '''
  @app.route("/questions")
  def get_all_questions():
    selection = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request,selection)
    if len(current_questions) == 0:
        abort(404)

    categories = Category.query.order_by(Category.id).all()
    if len(categories) == 0:
        abort(404)

    return jsonify({
      "success":True,
      "questions":current_questions,
      "total_questions": len(selection),
      "categories": { category.id : category.type for category in categories },
      'current_category': None
    })
  
  '''
  Endpoint to DELETE question using a question ID. 
  '''
  @app.route("/questions/<int:question_id>",methods=['DELETE'])
  def remove_question(question_id):
    question = Question.query.filter(Question.id==question_id).one_or_none()
    if question is None:
      abort(404)
    question.delete()
    
    return jsonify({
      "success":True,
      "deleted":question_id
    })

  '''
  Endpoint to POST a new question and to get questions based on a search term
  '''
  @app.route("/questions",methods=['POST'])
  def create_question():
    body = request.get_json()
    new_question = body.get("question",None)
    new_answer = body.get("answer",None)
    new_category = body.get("category",None)
    new_difficulty = body.get("difficulty",None)
    searchTerm = body.get("searchTerm",None)
    try:
      if searchTerm:
        matched_questions =Question.query.order_by(Question.id).filter(
          Question.question.ilike("%{}%".format(searchTerm))
        )
        questions = paginate_questions(request,matched_questions)
        return jsonify({
          "success":True,
          "questions":questions,
          "total_questions": len(matched_questions.all()),
          'current_category': None
        })
      else:
        if (not new_question) or (not new_answer) or (not new_category) or (not new_difficulty):
          abort(422)
        question = Question(new_question,new_answer,new_category,new_difficulty)
        question.insert()
        
        return jsonify({
          "success":True,
        })
    except:
      abort(422)
  
  '''
  Endpoint to get questions based on category. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    allquestions = Question.query.filter(Question.category == category_id).all()
    questions = paginate_questions(request,allquestions)

    return jsonify({
      "success":True,
      "questions":questions,
      "total_questions":len(allquestions),
      "current_category":category_id
    })


  '''
  Endpoint to get questions to play the quiz.  
  '''
  @app.route("/quizzes",methods=['POST'])
  def play_quiz():
    try:
      body = request.get_json()
      previous_questions = body.get("previous_questions",None)
      quiz_category = body.get("quiz_category",None)

      
      if quiz_category['id'] == 0:
        available_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
      else:
        available_questions = Question.query.filter_by(
                    category=quiz_category['id']).filter(Question.id.notin_((previous_questions))).all()
      
      new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if len(available_questions) > 0 else None
      
      return jsonify({
        "success" :True,
        "question":new_question
      })
    except:
      abort(422)
  
  '''
  Error handlers for all expected errors 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "bad request"}), 400
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "resource not found"}),404,
    
  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({"success": False, "error": 405, "message": "Method Not allowed"}),405,

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}),422,
    
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({"success":False,"error":500,"message":"Internal server error"}),500
  
  
  return app

    