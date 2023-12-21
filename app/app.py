from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

network_json_path='E:\\tum_task\\data\Germany_Nobel.json'
custom_json_path = 'E:\\tum_task\\data\\custom_network.json'  # Your custom data network

def get_json_data():
    if not os.path.exists(custom_json_path):
        # Create a new JSON structure if the file doesn't exist
        return {"networkStructure": {"nodes": {"node": []}, "links": {"link": []}}}
    with open(custom_json_path, 'r+') as file:
        return json.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-network-data')
def get_network_data():

    with open(network_json_path, 'r') as file:
        data = json.load(file)

    with open(custom_json_path, 'r') as file:
        data_1 = json.load(file)

    node_data = data['networkStructure']['nodes']['node']
    node_data = node_data+data_1['networkStructure']['nodes']['node']

    return jsonify(node_data)


@app.route('/get-link-data')
def get_link_data():

    with open(network_json_path, 'r') as file:
        data = json.load(file)
    with open(custom_json_path, 'r') as file:
        data_1 = json.load(file)

    link_data = data['networkStructure']['links']['link']
    link_data = link_data + data_1['networkStructure']['links']['link']

    return jsonify(link_data)




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
    with open(custom_json_path, 'w') as file:
        json.dump(file_data, file, indent=4)

    return jsonify({"success": True, "message": "Node added"})



@app.route('/delete-node', methods=['POST'])
def delete_node():
    data = request.json
    latitude = str(data['latitude'])
    longitude = str(data['longitude'])

    # Check if file exists
    if not os.path.exists(custom_json_path):
        return jsonify({"success": False, "message": "JSON file not found"})

    with open(custom_json_path, 'r+') as file:
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

@app.route('/get-link-coordinates', methods=['POST'])
def get_link_coordinates():
    data = request.json
    source_node = data['source']
    target_node = data['target']
    # This section is to write data to JSON file
    with open(custom_json_path, 'r+') as file:
        file_data = json.load(file)
        nodes = file_data['networkStructure']['nodes']['node']
        with open(network_json_path,'r') as file_2:
            file_data_2 = json.load(file_2)
            nodes_2 = file_data_2['networkStructure']['nodes']['node']
            nodes_total = nodes + nodes_2
            # Check if both source and target nodes exist
            source_exists = any(node['id'] == source_node for node in nodes_total)
            target_exists = any(node['id'] == target_node for node in nodes_total)

            if not source_exists or not target_exists:
                return jsonify({"success": False, "message": "Source or target node not found"})

            # Add the link
            new_link = {"source": source_node, "target": target_node}
            file_data['networkStructure']['links']['link'].append(new_link)
            nodes_total.append(new_link)
            # Write the updated data back to the file
            file.seek(0)
            file.truncate()
            json.dump(file_data, file, indent=4)

            
    # This section is to send coordinates to front end
    with open(custom_json_path, 'r') as file:
        file_data = json.load(file)
        nodes = file_data['networkStructure']['nodes']['node']
        with open(network_json_path,'r') as file_2:
            file_data_2 = json.load(file_2)
            nodes_2 = file_data_2['networkStructure']['nodes']['node']
            nodes_total = nodes + nodes_2

            source_coords = next(({'latitude': node['coordinates']['y'], 'longitude': node['coordinates']['x']} 
                                    for node in nodes_total if node['id'] == source_node), None)
            target_coords = next(({'latitude': node['coordinates']['y'], 'longitude': node['coordinates']['x']} 
                                    for node in nodes_total if node['id'] == target_node), None)

            if not source_coords or not target_coords:
                return jsonify({"success": False, "message": "Source or target node not found"})

    return jsonify({"success": True, "source": source_coords, "target": target_coords, "message": "Link added"})



@app.route('/delete-link', methods=['POST'])
def delete_link():
    data = request.json
    source_node = data['source']
    target_node = data['target']

    with open(custom_json_path, 'r+') as file:
        file_data = json.load(file)

        # Find and remove the link
        links = file_data['networkStructure']['links']['link']
        link_count_before = len(links)
        links[:] = [link for link in links if not (link['source'] == source_node and link['target'] == target_node)]

        link_count_after = len(links)

        if link_count_before == link_count_after:
            return jsonify({"success": False, "message": "Link not found"})

        # Write the updated data back to the file
        file.seek(0)
        file.truncate()
        json.dump(file_data, file, indent=4)

    return jsonify({"success": True, "message": "Link deleted"})



if __name__ == '__main__':
    app.run(debug=True)