# Import necessary libraries
from flask import Flask, Response, request
from flask_httpauth import HTTPBasicAuth
from vcf_functions import translate_vcf
import os

app = Flask(__name__)
auth = HTTPBasicAuth()
# Access credentials from environment variables
USERNAME = os.environ.get('FLASK_APP_USERNAME', 'admin') # default to 'admin' if not set
PASSWORD = os.environ.get('FLASK_APP_PASSWORD', '123456') # default to '123456' if not set

users = {
    USERNAME:PASSWORD
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    
@app.route('/ls/health/', methods=['GET'])
@app.route('/ls/health', methods=['GET'])
def health_check():
    return Response("Healthy", 200)

@app.route('/ls/getPgtAData/', methods=['GET'])
@app.route('/ls/getPgtAData', methods=['GET'])
@auth.login_required
def get_data():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    base_vcf_file_path = os.path.normpath(request.json.get('outputsDir'))

    if base_vcf_file_path is not None and base_vcf_file_path != '':
        vcf_file_path = os.path.join("data/",base_vcf_file_path,"CnvActor-00/","mosaic/","CN_Segments.vcf")
    else:
        vcf_file_path = os.path.join("data/","CnvActor-00/","mosaic/","CN_Segments.vcf")

    cytoband_file_path = os.path.join(current_directory, 'cytoBand.txt')
    # FYI, if the passed value in the JSON starts with a '/' then it will ignore all of this and just use the provided value
    vcf_file_path = os.path.normpath(os.path.join(current_directory, vcf_file_path))

    try:
        df = translate_vcf(cytoband_file_path,vcf_file_path)
        return Response(df.to_csv(index=False, sep='\t'), mimetype="text/tab-separated-values")
    except FileNotFoundError:
        return Response("VCF not found at " + vcf_file_path,404)

if __name__ == '__main__':
    app.run(port=5000,ssl_context='adhoc')