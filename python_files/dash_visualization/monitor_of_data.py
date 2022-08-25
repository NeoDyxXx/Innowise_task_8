from flask import Flask
from get_data_from_db import GetDataFromDB


app = Flask(__name__)
init_getter = GetDataFromDB()


@app.route('/')
def main():
    return 'API for get data in DynamoDB'


@app.route("/get_stage_data")
def get_stage_data():
    return {'status': 200, 'data': init_getter._get_stage_data()}


@app.route('/get_parse_data_type_one')
def get_parse_data_type_one():
    return {'status': 200, 'data': init_getter._get_parse_data_type_one()}

@app.route('/get_parse_data_type_two')
def get_parse_data_type_two():
    return {'status': 200, 'data': init_getter._get_parse_data_type_two()}
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)