from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-engine', methods=['GET'])
def run_engine():
    try:
        # Uruchom main.py
        result = subprocess.run(['python', 'main.py'], capture_output=True, text=True, check=True)
        output = result.stdout
        return jsonify({'message': 'Silnik uruchomiony', 'output': output})
    except subprocess.CalledProcessError as e:
        return jsonify({'error': str(e), 'output': e.stderr}), 500
    except FileNotFoundError:
        return jsonify({'error': 'main.py nie znaleziono'}), 404

if __name__ == '__main__':
    app.run(host="localhost", port=5001)
