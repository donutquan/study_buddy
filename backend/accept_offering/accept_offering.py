from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)


user_URL = environ.get('user_URL') or "http://localhost:5000/user"
homework_URL = environ.get('homework_URL') or "http://localhost:5100/homework"
liaise_URL = environ.get('liaise_URL') or "http://localhost:5200/liaise"



@app.route("/accept_offering", methods=['POST'])
def accept_offering():
    # Check for input format and data of the reques tare JSON

    if request.is_json:
        try:
            offering = request.get_json()
            print("\nReceived a request to accept offering in JSON:", offering)

            # Activate function to update relevant microservices

            result = processAcceptance(offering)
            print('\n-------------------------')
            print('\nresult: ', result)
            return jsonify(result), result['code']
        
        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "accept_offering.py internal error: " + ex_str
            }), 500
    

    # Not a JSON request
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " +str(request.get_data())
    })


def processAcceptance(offering):

    #Invoke homework microservice to update status
    print('\n-----Invoking homework microservice-----')
    homework_id = offering.homework_id
    homework_URL = homework_URL + '/' + homework_id
    homework_result = invoke_http(homework_URL, method='PUT', json=offering)
    print('homework_result:', order_result)

    
    homework_code = homework_result["code"]
    if code not in range(200,300):
        print("Error in updating homework")
        return {
            "code": 400,
            "data": {
                "homework_result": homework_result
            },
            "message": "There has been an error in updating the homework. Error has been sent for error handling."
        }

    # Implementation of error handling --> AMQP


    #Invoke user liaise microservice to update status
    print('\n-----Invoking liaise microservice-----')
    liaise_id = offering.liaise_id
    liaise_URL = liaise_URL + '/' + liaise_id
    liaise_result = invoke_http(liaise_URL, method='PUT', json=offering)
    print('liaise_result:', liaise_result)

    
    
    liaise_code = liaise_result["code"]
    if code not in range(200,300):
        print("Error in updating homework")
        return {
            "code": 400,
            "data": {
                "liaise_result": liaise_result
            },
            "message": "There has been an error in updating the liaison. Error has been sent for error handling."
        }

    # Implementation of error handling --> AMQP




if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5300, debug=True)


    # For our understanding
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network