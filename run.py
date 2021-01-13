import os
from api import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORTA', 20019)), debug=True)
