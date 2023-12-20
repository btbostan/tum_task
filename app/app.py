from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

json_file_path = 'E:\\tum_task\\data\\custom_network.json'  # Your custom data network

def get_json_data():
    if not os.path.exists(json_file_path):
        # Create a new JSON structure if the file doesn't exist
        return {"networkStructure": {"nodes": {"node": []}, "links": {"link": []}}}
    with open(json_file_path, 'r+') as file:
        return json.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-network-data')
def get_network_data():
    with open('E:\\tum_task\\data\Germany_Nobel.json', 'r') as file:
        data = json.load(file)
    return jsonify(data['networkStructure']['nodes']['node'])


@app.route('/get-link-data')
def get_link_data():
    with open('E:\\tum_task\\data\\Germany_Nobel.json', 'r') as file:
        data = json.load(file)
    return jsonify(data['networkStructure']['links']['link'])




@app.route('/add-node', methods=['POST'])
def add_node():
    data = request.json
    node_name = data['name']
    latitude = str(data['latitude'])
    longitude = str(data['longitude'])

    file_data = get_json_data()

    # Check if the node already exists
    for node in file_data['networkStructure']['nodes']['node']:
        if (str(node['coordinates']['x']) == longitude and 
            str(node['coordinates']['y']) == latitude):
            return jsonify({"success": False, "message": "Node already exists"})

    # Add new node
    new_node = {
        "id": node_name,
        "coordinates": {"x": longitude, "y": latitude}
    }
    file_data['networkStructure']['nodes']['node'].append(new_node)

    # Write the updated data back to the file
    with open(json_file_path, 'w') as file:
        json.dump(file_data, file, indent=4)

    return jsonify({"success": True, "message": "Node added"})



@app.route('/delete-node', methods=['POST'])
def delete_node():
    data = request.json
    latitude = str(data['latitude'])
    longitude = str(data['longitude'])

    # Check if file exists
    if not os.path.exists(json_file_path):
        return jsonify({"success": False, "message": "JSON file not found"})

    with open(json_file_path, 'r+') as file:
        file_data = json.load(file)

        # Find and remove the node
        nodes = file_data['networkStructure']['nodes']['node']
        node_count_before = len(nodes)
        nodes[:] = [node for node in nodes if not (str(node['coordinates']['x']) == longitude and 
                                                    str(node['coordinates']['y']) == latitude)]
        node_count_after = len(nodes)

        if node_count_before == node_count_after:
            return jsonify({"success": False, "message": "Node not found"})

        # Write the updated data back to the file
        file.seek(0)
        file.truncate()
        json.dump(file_data, file, indent=4)

    return jsonify({"success": True, "message": "Node deleted"})


if __name__ == '__main__':
    app.run(debug=True)