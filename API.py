from flask import Flask, request, Response
import requests

app = Flask(__name__)

PRODUCT_SERVICE_URL = 'http://localhost:5000'
ORDER_SERVICE_URL = 'http://localhost:5001'
INVENTORY_SERVICE_URL = 'http://localhost:5002'
LOGIN_SERVICE_URL = 'http://localhost:5003'

@app.route('/products', methods=['POST'])
def proxy_to_add():
    response = requests.request(
        method=request.method,
        url=f"{PRODUCT_SERVICE_URL}/products",
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items()
               if name.lower() not in excluded_headers]

    return Response(response.content, response.status_code, headers)



@app.route('/products', defaults={'path': ''}, methods=['GET','PUT', 'DELETE'])
@app.route('/products/<path:path>', methods=['GET', 'PUT',  'DELETE'])

def proxy_to_product(path):

    response = requests.request(
        method=request.method,
        url = f"{PRODUCT_SERVICE_URL}/products/{path}",
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = {name: value for (name, value) in response.raw.headers.items()
               if name.lower() not in excluded_headers}

    return Response(response.content, response.status_code, headers)


@app.route('/orders', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/orders/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_to_order(path):
    # Construct the full URL to the order service
    url = f"{ORDER_SERVICE_URL}/orders/{path}"

    # Forward the request to the order service
    response = requests.request(
        method=request.method,
        url=url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    # Exclude headers that could interfere with Flask's handling
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = {name: value for (name, value) in response.raw.headers.items()
               if name.lower() not in excluded_headers}

    # Return the response from the order service
    return Response(response.content, response.status_code, headers)

@app.route('/inventory/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_to_inventory(path):
    response = requests.request(
        method=request.method,
        url=f"{INVENTORY_SERVICE_URL}/inventory/{path}",
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    # Fixed how headers are fetched using the.items() call
    headers = [(name, value) for name, value in response.headers.items()
               if name.lower() not in excluded_headers]

    return Response(response.content, response.status_code, headers=headers)

@app.route('/login', methods=['POST'])
def proxy_to_login_service():
    data = request.json
    response = requests.post(f"{LOGIN_SERVICE_URL}/login", json=data)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items()
               if name.lower() not in excluded_headers]

    return Response(response.content, response.status_code, headers)

if __name__ == '__main__':
    app.run(port=12345, debug=True, threaded=True)

