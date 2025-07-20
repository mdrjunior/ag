# /home/SEU_USUARIO/aguas_rio/consulta.py
from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

HEADERS = {
    "ocp-apim-subscription-key": "4b70bdf7ac3548a7afefb73bf7ce4aa5",
    "origin": "https://servicosonline.aguasdorio.com.br",
    "referer": "https://servicosonline.aguasdorio.com.br/"
}

# Página + resultado na mesma URL
@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    erro = None

    if request.method == "POST":
        doc = request.form.get("doc", "").strip()
        mat = request.form.get("mat", "").strip()

        if doc and mat:
            url = (
                "https://api.aegea.com.br/external/agencia-virtual/app/v1/publico/"
                f"debito-deslogado/debito-totais-deslogado?matricula={mat}&documento={doc}"
            )
            try:
                r = requests.get(url, headers=HEADERS, timeout=10)
                r.raise_for_status()
                resultado = r.json()
            except Exception as e:
                erro = str(e)
        else:
            erro = "Preencha CPF/CNPJ e matrícula."

    return render_template_string("""
    <!doctype html>
    <html lang="pt-BR">
    <head>
      <meta charset="utf-8">
      <title>Águas do Rio – Consulta</title>
      <style>
        body{font-family:Arial;margin:40px auto;max-width:500px}
        input{display:block;width:100%;margin:8px 0;padding:8px}
        button{background:#17e3cb;color:#fff;border:none;padding:10px 20px}
        pre{background:#f5f5f5;padding:10px;overflow:auto}
        .erro{color:red}
      </style>
    </head>
    <body>
      <h2>Consulta de Débitos – Águas do Rio</h2>
      <form method="post">
        <input name="doc" type="text" placeholder="CPF ou CNPJ (somente números)" required>
        <input name="mat" type="text" placeholder="Matrícula" required>
        <button type="submit">Consultar</button>
      </form>

      {% if erro %}
        <p class="erro">{{ erro }}</p>
      {% endif %}

      {% if resultado %}
        <h3>Resultado</h3>
        <pre>{{ resultado | tojson(indent=2) }}</pre>
      {% endif %}
    </body>
    </html>
    """, resultado=resultado, erro=erro)

if __name__ == "__main__":
    app.run()
