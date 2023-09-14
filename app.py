# Import necessary libraries
from flask import Flask, Response, abort, request
from flask_httpauth import HTTPBasicAuth
from vcf_functions import translate_vcf
import os

app = Flask(__name__)
auth = HTTPBasicAuth()
users = {
    "admin": "123456"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    
@app.route('/ls/health', methods=['GET'])
def health_check():
    return Response("Healthy", 200)


@app.route('/ls/getPgtAData', methods=['GET'])
@auth.login_required
def get_data():
    base_vcf_file_path = os.path.normpath(request.json.get('outputsDir'))
    vcf_file_path = os.path.join(base_vcf_file_path,"CnvActor-00","mosaic","CN_Segments.vcf")
    current_directory = os.path.dirname(os.path.abspath(__file__))
    cytoband_file_path = os.path.join(current_directory, 'cytoBand.txt')
    vcf_file_path = os.path.join(current_directory, vcf_file_path)

    try:
        df = translate_vcf(cytoband_file_path,vcf_file_path)
        return Response(df.to_csv(index=False, sep='\t'), mimetype="text/tab-separated-values")
    except FileNotFoundError:
        return Response("Resource not found",404)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)