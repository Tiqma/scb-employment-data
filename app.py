from flask import Flask, redirect, render_template, request, send_file
from analys import graf, get_options
from compare import compare
import base64
from io import BytesIO
import matplotlib.pyplot as plt
app = Flask(__name__)

@app.route("/")
def index():
    innehall = get_options()
    sektor = innehall["sektor"]
    kon = innehall["kön"]
    ar = innehall["år"]

    return render_template("index.html", sektor=sektor, kon=kon, ar=ar)

@app.route("/graf", methods=["GET"])
def grafroute():
    innehall = get_options()
    sektor_i = innehall["sektor"]
    kon_i = innehall["kön"]
    ar_i = innehall["år"]

    data  = request.args
    sektor = data.get("sektor")
    kon    = data.get("kon")
    år     = data.get("år")

    fig = graf(sektor, kon, år)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return render_template("index.html", plot=img_base64, sektor=sektor_i, kon=kon_i, ar=ar_i)

@app.route('/compare')
def jamfor():
    innehall = get_options()
    sektor_i = innehall["sektor"]
    kon_i = innehall["kön"]
    ar_i = innehall["år"]

    return render_template("compare.html", sektor=sektor_i, kon=kon_i, ar=ar_i)

@app.route('/bild')
def get_image():
    data  = request.args
    sektor = data.get("sektor")
    kon    = data.get("kon")
    år     = data.getlist("år")
    img_buf = compare(sektor, kon, år)

    img_buf.seek(0)

    return send_file(img_buf, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)