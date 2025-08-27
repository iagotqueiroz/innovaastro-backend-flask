from flask import Flask,jsonify,Response,request
from flask_cors import CORS
from astro import buscar_astro
from camera import start_cam_view


app = Flask(__name__)
cors = CORS(app)

@app.route("/version")
def version():
    return jsonify({"version": "1.0.0"})

@app.route('/stream',methods=["GET"])
def stream():
    return Response(start_cam_view(), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/buscar",methods=["POST"])
def buscar():
    nome_astro = request.get_json()['name']
    latitude = request.get_json()['latitude']
    longitude = request.get_json()['longitude']
    try:
        return buscar_astro(latitude,longitude,nome_astro)
    except:
        return jsonify({'erro': f'Astro \"{nome_astro}\" não encontrado.'}), 404
   
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)