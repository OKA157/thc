import flask
import os
import tempfile
import json
from flask import Flask, request,jsonify,make_response, send_file

from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/submitVote', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def submitVote():

    import json
    import voteFunctions.setVoting as voting

    try:
        # Process the form data here
        param1 = request.data
        json_bytes = param1
        json_bytes.decode('utf-8')
        receivedData = json.loads(json_bytes)

        key=receivedData["key"]
        title=receivedData["title"]
        expiring=receivedData["expiring"]
        closing=receivedData["closing"]
        props=receivedData["props"]

        # SET VOTE
        voting.makeVote(key, title, closing, expiring, props)
        
        response_data = {'message': 'Form submitted successfully!'}
        response = make_response(jsonify(response_data), 200)
    
    except Exception as e:
        # If there's an error during processing
        error_message = str(e)
        response_data = {'error': error_message}
        response = make_response(jsonify(response_data), 500)
    
    return response


@app.route('/confirmOption', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def confirmOption():

    import json
    import voteFunctions.setSingleVote as voting
    import voteFunctions.TimeRecorder as recTime

    try:
        # Process the form data here
        param1 = request.data
        json_bytes = param1
        json_bytes.decode('utf-8')
        receivedData = json.loads(json_bytes)

        key=receivedData["key"]
        option=receivedData["option"]

        paillierTimer = recTime.read_execution_times('paillier_vote.txt')
        thcTimer = recTime.read_execution_times('thc_vote.txt')
        result = voting.setVote(key, option)
        print("RESULT: ",result)

        # Prepare and send the response
        response_data = {
            'message': result,
            'paillierTimer': paillierTimer[-1] if paillierTimer else "No timing data",
            'thcTimer': thcTimer[-1] if thcTimer else "No timing data"
        }
        response = make_response(jsonify(response_data), 200)
    except Exception as e:
        response_data = {
            'message': 'error',
        }
        response = make_response(jsonify(response_data), 500)
    return response

@app.route('/listActiveVotes', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def listActiveVotes():

    import voteFunctions.setVoting as voting
    try:
        activeVotes = voting.getActiveVotingList()
        print(activeVotes[0])
        response = make_response(jsonify(activeVotes), 200)
    
    except Exception as e:
        error_message = str(e)
        response_data = {'error': error_message}
        response = make_response(jsonify(response_data), 500)
    return response

@app.route('/listClosedVotes', methods=['GET'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def listClosedVotes():

    import voteFunctions.setVoting as voting
    try:
        activeVotes = voting.getClosedVotingList()
        print(activeVotes[0])
        response = make_response(jsonify(activeVotes), 200)
    except Exception as e:
        error_message = str(e)
        response_data = {'error': error_message}
        response = make_response(jsonify(response_data), 500)
    return response


@app.route('/resultsVote', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def resultsVote():

    import voteFunctions.getResults as resultsVoting
    
    try:
        param1 = request.data
        json_bytes = param1
        json_bytes.decode('utf-8')
        receivedData = json.loads(json_bytes)

        vote_key=receivedData["key"]
        option=receivedData["option"]
        print("PARAM 1: ",vote_key)
        print("PARAM 2: ",option)
        try:
            result_count = resultsVoting.get_specific_result(vote_key, option)
            return jsonify({'result': result_count})
        except Exception as e:
            return jsonify({'result': 0})
        

    except Exception as e:
        error_message = str(e)
        response_data = {'error': error_message}
        response = make_response(jsonify(response_data), 500)

    return response
    


if __name__ == '__main__':
    app.run(debug=True, port=8001, host="0.0.0.0")
