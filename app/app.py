from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime
import logging

app = Flask(__name__)

network_json_path='E:\\tum_task\\data\Germany_Nobel.json'
log_path="E:\\tum_task\\log.txt"

class SimpleLogger:
    def __init__(self, log_file=log_path):
        self.log_file = log_file

    def log(self, message, ip_address=''):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp} - {ip_address}] {message}\n"
        
        with open(self.log_file, 'a') as file:
            file.write(log_message)


logger = SimpleLogger()

def get_json_data():
 
    with open(network_json_path, 'r+') as file:
        return json.load(file)


@app.route('/')
def index():
    logger.log("Server started.")
    return render_template('index.html')

@app.route('/get-network-data')
def get_network_data():

    with open(network_json_path, 'r') as file:
        data = json.load(file)



    node_data = data['networkStructure']['nodes']['node']
    logger.log("Nodes imported to the map.")
    return jsonify(node_data)


@app.route('/get-link-data')
def get_link_data():

    with open(network_json_path, 'r') as file:
        data = json.load(file)

    link_data = data['networkStructure']['links']['link']
    logger.log("Links imported to the map.")
    return jsonify(link_data)




@app.route('/add-node', methods=['POST'])
def add_node():
    data = request.json
    node_name = data['name']
    latitude = str(data['latitude'])
    longitude = str(data['longitude'])
    client_ip = request.remote_addr
    file_data = get_json_data()
    print(client_ip)

    # Check if the node already exists
    for node in file_data['networkStructure']['nodes']['node']:
        if (str(node['coordinates']['x']) == longitude and 
            str(node['coordinates']['y']) == latitude):

            logmsg = str(node_name) + " aldready exist. Could not add."
            logger.log(logmsg, client_ip)

            return jsonify({"success": False, "message": "Node already exists"})

    # Add new node
    new_node = {
        "id": node_name,
        "coordinates": {"x": longitude, "y": latitude}
    }
    file_data['networkStructure']['nodes']['node'].append(new_node)

    # Write the updated data back to the file
    with open(network_json_path, 'w') as file:
        json.dump(file_data, file, indent=4)

    logmsg = str(node_name)+ "lat: " + str(latitude)+ "long: "+ str(longitude) + " added"
    logger.log(logmsg, client_ip)

    return jsonify({"success": True, "message": "Node added"})



@app.route('/delete-node', methods=['POST'])
def delete_node():
    data = request.json
    node_name = data['name']
    latitude = str(data['latitude'])
    longitude = str(data['longitude'])
    client_ip = request.remote_addr


    with open(network_json_path, 'r+') as file:
        file_data = json.load(file)

        # Find and remove the node
        nodes = file_data['networkStructure']['nodes']['node']
        node_count_before = len(nodes)
        nodes[:] = [node for node in nodes if not (str(node['coordinates']['x']) == longitude and 
                                                    str(node['coordinates']['y']) == latitude)]
        node_count_after = len(nodes)

        if node_count_before == node_count_after:

            logmsg = str(node_name) + "lat: " + str(latitude)+ "long: "+ str(longitude)+ " Could not delete. Not found."
            logger.log(logmsg, client_ip)

            return jsonify({"success": False, "message": "Node not found"})

        # Write the updated data back to the file
        file.seek(0)
        file.truncate()
        json.dump(file_data, file, indent=4)

    logmsg = str(node_name)+ "lat: " + str(latitude)+ "long: "+ str(longitude) + " deleted."
    logger.log(logmsg, client_ip)

    return jsonify({"success": True, "message": "Node deleted"})

@app.route('/get-link-coordinates', methods=['POST'])
def get_link_coordinates():
    data = request.json
    source_node = data['source']
    target_node = data['target']
    client_ip = request.remote_addr
    # This section is to write data to JSON file


    with open(network_json_path, 'r+') as file:
        file_data = json.load(file)
        nodes = file_data['networkStructure']['nodes']['node']
    
        # Check if both source and target nodes exist
        source_exists = any(node['id'] == source_node for node in nodes)
        target_exists = any(node['id'] == target_node for node in nodes)

        if not source_exists or not target_exists:

            logmsg = "Source or target node not found. Link is not added."
            logger.log(logmsg, client_ip)

            return jsonify({"success": False, "message": "Source or target node not found"})

        # Add the link
        new_link = {"source": source_node, "target": target_node}
        file_data['networkStructure']['links']['link'].append(new_link)
        # Write the updated data back to the file
        file.seek(0)
        file.truncate()
        json.dump(file_data, file, indent=4)
    logmsg = "source: "+ source_node +"target: " + target_node + " Link is added."
    logger.log(logmsg, client_ip)
            
    # This section is to send coordinates to front end
    with open(network_json_path, 'r') as file:
        file_data = json.load(file)
        nodes = file_data['networkStructure']['nodes']['node']

        source_coords = next(({'latitude': node['coordinates']['y'], 'longitude': node['coordinates']['x']} 
                                for node in nodes if node['id'] == source_node), None)
        target_coords = next(({'latitude': node['coordinates']['y'], 'longitude': node['coordinates']['x']} 
                                for node in nodes if node['id'] == target_node), None)

        if not source_coords or not target_coords:
            return jsonify({"success": False, "message": "Source or target node not found"})

    return jsonify({"success": True, "source": source_coords, "target": target_coords, "message": "Link added"})



@app.route('/delete-link', methods=['POST'])
def delete_link():
    data = request.json
    source_node = data['source']
    target_node = data['target']
    client_ip = request.remote_addr

    with open(network_json_path, 'r+') as file:
        file_data = json.load(file)

        # Find and remove the link
        links = file_data['networkStructure']['links']['link']
        link_count_before = len(links)
        links[:] = [link for link in links if not (link['source'] == source_node and link['target'] == target_node)]

        link_count_after = len(links)

        if link_count_before == link_count_after:
            logmsg = "source: "+ source_node +"target: " + target_node + " Link not found. Could not delete."
            logger.log(logmsg, client_ip)

            return jsonify({"success": False, "message": "Link not found"})

        # Write the updated data back to the file
        file.seek(0)
        file.truncate()
        json.dump(file_data, file, indent=4)

    logmsg = "source: "+ source_node +"target: " + target_node + " Link is added."
    logger.log(logmsg, client_ip)
    
    return jsonify({"success": True, "message": "Link deleted"})



if __name__ == '__main__':
    app.run(debug=True)