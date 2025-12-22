from flask import Flask, render_template, request
from analys import graf, get_options
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
    data  = request.args
    sektor = data.get("sektor")
    kon    = data.get("kon")
    år     = data.get("år")

    # Skapa grafen
    fig = graf(sektor, kon, år)

    # Konvertera figuren till PNG i minnet
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)  # stäng figuren för att frigöra minnet
    buf.seek(0)

    # Konvertera till Base64 så vi kan bädda in i HTML
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    # Skicka Base64-strängen till templaten
    return render_template("index.html", plot=img_base64)

if __name__ == "__main__":
    app.run(debug=True)