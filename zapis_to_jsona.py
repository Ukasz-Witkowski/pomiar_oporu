import json

jsonFile = open("data.json", "r") 
data = json.load(jsonFile) 
jsonFile.close() 

data["default_path"] = "ratatata"

jsonFile = open("data.json", "w+")
jsonFile.write(json.dumps(data))
jsonFile.close()
