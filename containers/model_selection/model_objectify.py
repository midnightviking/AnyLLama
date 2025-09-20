import os
import yaml
import requests

class LLMAvailability:
    model_list = []
    
    def __init__(self, name, prefix, port=None):
        self.status = 0
        self.size   = 0
        self.valid  = 0
        self.name   = name if name else ""
        self.prefix = prefix if prefix else ""
        self.port   = port if port else 4200
        self.isRunning = False
        self.nicename = self.set_nicename(name)
        if name not in LLMAvailability.model_list:
            LLMAvailability.model_list.append(name)

    def __str__(self):
        return f"{self.name} - {self.status} - {self.size} - {self.valid}"
    
    def set_size(self, size):
        k_size = 0
        if size >= 1024**3:
            k_size = f"{size / 1024**3:.2f} GB"
        elif size >= 1024**2:
            k_size = f"{size / 1024**2:.2f} MB"
        elif size >= 1024:
            k_size =  f"{size / 1024:.2f} KB"
        else:
            k_size = f"{size} B"
        self.size = k_size

    def set_status(self, status):
        self.status = status
    def set_valid(self, valid):
        self.valid = valid
    def set_port(self, port):
        self.port = port
    def set_running(self, running):
        self.isRunning = running

    def set_nicename(self, name):
        self.nicename = name.split(":")[0] if not None else ""
        return self.nicename
    
    def get_name(self):
        return self.name
    def get_nicename(self):
        if self.nicename == "":
            nn = self.nicename
        return self.nicename if not None else self.name
    def get_status(self):
        return self.status
    def get_size(self):
        return self.size
    def get_port(self):
        return self.port
    def get_valid(self): 
        return self.valid
    def get_running(self):
        return self.isRunning

    def get_retrevable_name(self):
        return self.prefix + "/" + self.name

    def get_model(model):
        if model in LLMAvailability.model_list:
            return model
        else:
            return None


available_models = []

def load_available_models():
    try:
        req = requests.get("http://ollama:11434/api/tags")
        if req.status_code == 200:
            LLMAvailability.model_list.clear()
            available_models.clear()
            result = req.json()
            local_models = result.get("models")
            for m in local_models:
                available_models.append(LLMAvailability(name=m.get("name"), prefix="ollama_chat"))
    except requests.exceptions.ConnectionError as e:
        print(f"Warning: Could not connect to Ollama service at http://ollama:11434: {e}")
        print("Ollama service may not be running or may not be accessible.")
    except Exception as e:
        print(f"Error loading available models: {e}")
    
    return LLMAvailability.model_list

def get_available_models():
    if(len(available_models) == 0):
        load_available_models()
        get_download_status() # also get the size and status of the models, only Ollama for the moment
    return available_models

def get_model(model_name, refresh=False):
    if(len(available_models) == 0 or refresh):
        load_available_models()
    for model in available_models:
        if model.get_nicename() == model_name or model.get_name() == model_name:
            model.set_valid(1)
            return model
    return None

def get_download_status():
    if(len(available_models) == 0):
        load_available_models()

    try:
        req = requests.get("http://ollama:11434/api/tags")
        if(req.status_code == 200):
            ollamaModelsInstalled = req.json()
        else:
            return available_models
    except requests.exceptions.ConnectionError as e:
        print(f"Warning: Could not connect to Ollama service at http://ollama:11434: {e}")
        return available_models
    except Exception as e:
        print(f"Error getting download status: {e}")
        return available_models
        
    if not ollamaModelsInstalled:
        return available_models

    for model in available_models:
        for installed_model in ollamaModelsInstalled["models"]:
            nicename = installed_model["name"].split(":")[0]
            if model.get_nicename() == nicename:
                model.set_status(1)
                model.set_size(installed_model["size"])
                
    return available_models

def get_models_json():
    models = []
    try:
        # update current status of the models
        get_available_models()
        get_download_status()
        for model in available_models:
            models.append({"name": model.get_name(),"nicename": model.get_nicename(), "status": model.get_status(),"size": model.get_size(), "port": model.get_port(), "running": model.get_running()})
    except Exception as e:
        print(f"Error getting models JSON: {e}")
    return models

def set_model_running(model_name, running):
    for a in available_models:
        if a.get_nicename() == model_name or a.get_name() == model_name:
            a.set_running(running)
        else:
            a.set_running(False)
    