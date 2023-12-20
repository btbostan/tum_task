from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-network-data')
def get_network_data():
    with open('E:\\tum_task\\data\Germany_Nobel.json', 'r') as file:
        data = json.load(file)
    return jsonify(data['networkStructure']['nodes']['node'])








if __name__ == '__main__':
    app.run(debug=True)