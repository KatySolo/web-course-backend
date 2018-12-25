import db_worker

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.run()

connection = None


def sortPayments(sort, field_option, filter_field):
    print(sort, field_option, filter_field)
    if field_option == 'no':
        return db_worker.selectAll(connection)
    elif filter_field != '':
        return db_worker.filter(connection, field_option, filter_field)
    else:
        return db_worker.orderby(connection, field_option, sort)


@app.route('/card-payment', methods=['POST', 'GET', 'PATCH'])
def login():
    if request.method == 'POST':
        jsonData = request.get_json()
        db_worker.insert(connection, jsonData)
        return jsonify(), 201
    elif request.method == 'GET':
        sort_option = request.args.get('sort', default='asc', type=str).upper()
        field_option = request.args.get('field', default='no', type=str)
        filter_option = request.args.get('filter', default='', type=str)
        return jsonify(sortPayments(sort_option, field_option, filter_option))
    elif request.method == 'PATCH':
        changes = request.get_json()
        db_worker.alterTrust(connection, changes['changes'])
        return jsonify(), 204

#
# @app.route('/require-payment', methods=['POST', 'GET'])
# def require():
#     if request.method == 'POST':
#         jsonData = request.get_json()
#         requirePayments.append(
#             {
#                 'name': jsonData['name'],
#                 'bik': jsonData['bik'],
#                 'account_num': jsonData['account_num'],
#                 'nds': jsonData['nds'],
#                 'amount': jsonData['amount'],
#                 'tel_number': jsonData['tel_number'],
#                 'email':jsonData['email']
#             }
#         )
#         print (requirePayments)
#         return jsonify(), 201
#     elif request.method == 'GET':
#         return jsonify(requirePayments), 200
#

if __name__ == '__main__':
    try:
        connection = db_worker.connectDB()
        app.run()
    finally:
        db_worker.disconnectDB(connection)
