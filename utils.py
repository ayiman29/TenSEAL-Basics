import base64

def write_data(file_name, data):
    data = base64.b64encode(data)

    with open(file_name, 'wb') as f:
        f.write(data)


def read_data(file_name):
    with open(file_name, 'rb') as f:
        data = f.read()

    return base64.b64decode(data)