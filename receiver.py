from flask import Flask, request, jsonify
import json, os
app = Flask(__name__)
@app.post('/report')
def report():
    token = os.environ.get('REPORT_TOKEN', 'lab-local-token')
    if request.headers.get('X-Report-Token') != token:
        return jsonify(error='Unauthorized'), 401
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or 'tests' not in data:
        return jsonify(error='Invalid report'), 400
    with open('test-report.json','w',encoding='utf-8') as f:
        json.dump(data,f,indent=2)
    print('Saved test-report.json:', data.get('overall_status'), flush=True)
    return jsonify(saved=True)
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5001)
