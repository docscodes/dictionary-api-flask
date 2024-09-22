from flask import Flask, request, jsonify, render_template
from model.dbHandler import match_exact, match_like

app = Flask(__name__)


@app.get("/")
def index():
  response = {"usage": "/dict?=<word>"}
  return jsonify(response)


@app.get("/dict")
def dictionary():
  word = request.args.get("word")

  if not word:
    response = {"status": "error", "word": word, "data": "word not found"}
    return jsonify(response)

  definitions = match_exact(word)
  if definitions:
    response = {"status": "success", "word": word, "data": definitions}
    return jsonify(response)

  definitions = match_like(word)
  if definitions:
    response = {"status": "partial", "word": word, "data": definitions}
    return jsonify(response)
  else:
    response = {"status": "error", "word": word, "data": "word not found"}
    return jsonify(response)


@app.get("/dict_list")
def dictionary_list():
  words = request.args.getlist("word")

  if not words:
    response = {"status": "error", "word": words, "data": "word not found"}
    return jsonify(response)

  response = {"words": []}

  for word in words:
    definitions = match_exact(word)
    if definitions:
      response["words"].append(
          {"status": "success", "word": word, "data": definitions})
    else:
      definitions = match_like(word)
      if definitions:
        response["words"].append(
            {"status": "partial", "word": word, "data": definitions})
      else:
        response[words].append(
            {"status": "error", "word": word, "data": "word not found"})

  return jsonify(response)


if __name__ == "__main__":
  app.run()
