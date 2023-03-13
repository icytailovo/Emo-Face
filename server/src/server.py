from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import base64

import pipeline


hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse(self.path).query
        query_components = dict(qc.split("=") for qc in query.split("&"))
        
        print(query_components["path"], query_components["prompt"])
        image_path = query_components["path"].replace("%20", " ")
        prompt = query_components["prompt"].replace("%20", " ")
        output_paths = pipeline.run_pipline(image_path, prompt)
        
        # format json output
        images = []
        for path in output_paths:
            image = open(path, "rb")
            byte_array = image.read()
            int_array = [x for x in byte_array]
            images.append({"image": int_array})
        json_output = json.dumps(images).encode(encoding='utf_8')
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json_output)

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    webServer.timeout = 300
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")