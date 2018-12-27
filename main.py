import db_worker
import pdf_worker

from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.run()

connection = None


def sortPayments(sort, field_option, filter_field, db):
    # print(sort, field_option, filter_field)
    if field_option == 'no':
        return db_worker.selectAll(connection, db)
    elif filter_field != '':
        return db_worker.filter(connection, field_option, filter_field, db)
    else:
        return db_worker.orderby(connection, field_option, sort, db)


@app.route('/card-payment', methods=['POST', 'GET', 'PATCH'])
def login():
    if request.method == 'POST':
        jsonData = request.get_json()
        db_worker.insert(connection, jsonData, 'CardPayments')
        return jsonify(), 201
    elif request.method == 'GET':
        sort_option = request.args.get('sort', default='asc', type=str).upper()
        field_option = request.args.get('field', default='no', type=str)
        filter_option = request.args.get('filter', default='', type=str)
        return jsonify(sortPayments(sort_option, field_option, filter_option, 'CardPayments'))
    elif request.method == 'PATCH':
        changes = request.get_json()
        db_worker.alterTrust(connection, changes['changes'])
        return jsonify(), 204


@app.route('/require-payment', methods=['POST', 'GET'])
def require():
    if request.method == 'POST':
        jsonData = request.get_json()
        db_worker.insert(connection, jsonData, 'RequirePayments')
        return jsonify(), 201
    elif request.method == 'GET':
        sort_option = request.args.get('sort', default='asc', type=str).upper()
        field_option = request.args.get('field', default='no', type=str)
        filter_option = request.args.get('filter', default='', type=str)
        return jsonify(sortPayments(sort_option, field_option, filter_option, 'RequirePayments'))

@app.route('/create-payment', methods=['POST','GET'])
def document():
    if request.method == 'POST':
        jsonData = request.get_json()
        # print (jsonData)
        name = pdf_worker.create_payment_document(jsonData)
        return jsonify(name), 201
    elif request.method == 'GET':
        name = request.args.get('name', default='', type=str)
        response = send_file(name, 'application/pdf')
        response.headers['Content-Disposition'] = "attachment; filename='payment.pdf'"
        return response

#
if __name__ == '__main__':
    try:
        connection = db_worker.connectDB()
        app.run()
    finally:
        db_worker.disconnectDB(connection)
