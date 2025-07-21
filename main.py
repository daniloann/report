from actions import (getbyidcountry,addcountry, allcountry, regionsofcountry,
                     cityesofregion, searchperson, searchinfo,getbyId,password, get_family_tree)

from http.server import SimpleHTTPRequestHandler, HTTPServer

import urllib.parse
import json
import requests
import logging

logging.basicConfig(level=logging.INFO)


class MyHandler(SimpleHTTPRequestHandler):
    def send_json_response(self, result):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(result.encode('utf-8'))

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)  # Извлечение параметров
        try:
            if (parsed_path.path == "/country/getByIdcountry"):
                country_id = query_params.get('id', [None])[0]
                if country_id is None:
                    self.send_error(400, "ID parameter is required")
                    return
                result = getbyidcountry(country_id)
                logging.info(f"Request path: {parsed_path.path}, ID: {country_id}")
                self.send_json_response(result)

            elif (parsed_path.path == "/country/getallcountry"):
                result = allcountry()
                logging.info(f"Request path: {parsed_path.path}")
                self.send_json_response(result)

            elif (parsed_path.path == "/country/regionsofcountry"):
                country_id = query_params.get('id', [None])[0]
                if country_id is None:
                    self.send_error(400, "ID parameter is required")
                    return
                result = regionsofcountry(country_id)
                logging.info(f"Request path: {parsed_path.path}, ID: {country_id}")
                self.send_json_response(result)

            elif (parsed_path.path == "/country/cityesofregion"):
                region_id = query_params.get('id', [None])[0]
                if region_id is None:
                    self.send_error(400, "ID parameter is required")
                    return
                result = cityesofregion(region_id)
                logging.info(f"Request path: {parsed_path.path}, ID: {region_id}")
                self.send_json_response(result)

            elif (parsed_path.path == "/country/searchperson"):
                name = query_params.get('name', [None])[0]
                if name is None:
                    self.send_error(400, "name parameter is required")
                    return
                result = searchperson(name)
                logging.info(f"Request path: {parsed_path.path}, NAME: {name}")
                self.send_json_response(result)
        except Exception as e:
            logging.error(e)
            self.send_error(500, str(e))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_path = urllib.parse.urlparse(self.path)
        try:
            if (parsed_path.path == "/country/postaddcountry"):
                json_data = json.loads(post_data.decode('utf-8'))
                name = json_data.get('name')
                if not name:
                    self.send_error(400, "Country name is required")
                    return
                result = addcountry(name)
                logging.info(f"Request path: {parsed_path.path}, NAME: {name}")
                self.send_json_response(result)

            elif (parsed_path.path == "/country/searchinfo"):
                json_data = json.loads(post_data.decode('utf-8'))
                result = searchinfo(json_data)
                self.send_json_response(result)
                logging.info(f"Request path: {parsed_path.path}, INFO: {json_data}")

            elif (parsed_path.path == "/family/getbyId"):
                json_data = json.loads(post_data.decode('utf-8'))
                result = getbyId(json_data)
                self.send_json_response(result)
                logging.info(f"Request path: {parsed_path.path}, INFO: {json_data}")

            elif (parsed_path.path == "/person/password"):
                json_data = json.loads(post_data.decode('utf-8'))
                result = password(json_data)
                self.send_json_response(result)
                logging.info(f"Request path: {parsed_path.path}, INFO: {json_data}")

            elif (parsed_path.path == "/family/get_family_tree"):
                json_data = json.loads(post_data.decode('utf-8'))
                result = get_family_tree(json_data)
                self.send_json_response(result)
                logging.info(f"Request path: {parsed_path.path}, INFO: {json_data}")

        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            logging.error(e)
            self.send_error(500, str(e))

server_address = ('localhost', 8000)
httpd = HTTPServer(server_address, MyHandler)

print("Starting server on port 8000...")
httpd.serve_forever()
