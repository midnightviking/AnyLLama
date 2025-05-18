import json
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

import requests as req
import model_objectify
from flask_socketio import SocketIO
from model_objectify import LLMAvailability

app = Flask(__name__)
socketio = SocketIO(app)


# get the models setup
model_objectify.get_available_models()
availableModels = model_objectify.get_models_json()
mport = 5100 # just port for models that are missing a port in the config file
data = {
    "models": availableModels,
    "model_list": model_objectify.get_available_models(),
    "selectedModel"  : None,
    "ollamaStatus"   : None,
    "ollamaAvailableModels": [{}] ,
}

async def getOllamaStatus():
    res = req.get("http://localhost:11434/")
    status = 0
    if res.status_code == 200:
        status = 1
    data["ollamaStatus"] = status
    # grab the status of the models too
    model_objectify.get_download_status()
    return status


#interface
# Index
@app.route("/")
def index():
    return render_template('index.html', data=data)

# This route will be used to get the models
@app.route("/models", methods=['GET'])
def models():
    data["models"] = model_objectify.get_models_json()    
    return  {"models": data["models"], "selectedModel": data["selectedModel"]}

# This route will be used to select the model
@app.route("/model", methods=['GET', 'POST'])
def model():

    model_name = request.args.get("model_name")
    if model_name is None:
        return {"name": "None", "valid": False}
    
    model = None
    valid = False
    addToList = False

    model = model_objectify.get_model(model_name)

    if model is None: # download it if its not already installed    
        data["selectedModel"] = model_name
        completed = "0%"
        _data = {
            "model": model_name
        }
        datam = json.dumps(_data)        
        res = req.post("http://0.0.0.0:11434/api/pull",data=datam, stream=True)
        
        #stream to socketio
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                j = json.loads(chunk.decode('utf-8'))
                if(j["status"] == "success"):
                    valid = True
                if("completed" in j and "total" in j ):
                    completed = str(round((j["completed"] / j["total"])*100)) + "%"
                socketio.emit('model-download', {'data': j, "progress": completed, "model": model_name})
        model = model_objectify.get_model(model_name=model_name, refresh=True )
        addToList = True
        valid = True 
    else:
        valid = True
    
    if(valid):
        # check if the model has a port
        if(model.get_port() == None):
            global mport
            model.set_port(str(mport))
            mport += 1
        # start the model proxy
        model_objectify.set_model_running(model_name=model_name, running=True)
        # anythingllm to be the provider    
        return {"name": model.get_name(), "valid": valid, "size": model.get_size(),
                "port": model.get_port(), "running": model.get_running(), "addToList": addToList} 
        
    return {"name": model_name, "valid": False, "addToList":addToList}


@app.route("/service-request", methods=['GET'])
async def status():
    ollama = await getOllamaStatus()
    return {
        "ollama"  : ollama,
        "model"   : data["selectedModel"],
    }

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('connect')
def test_connect():
    print('Client connected')

if __name__ == '__main__':
    load_dotenv()
    port = int(os.getenv("APP_PORT", 5100))
    app.run(host='0.0.0.0', port=port, debug=True)
    socketio.run(app)