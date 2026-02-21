from flask import Blueprint, request, jsonify
import os

api = Blueprint("api",__name__)

LOG="logs/seguranca.log"

API_KEY="rovie123"  # depois você muda


@api.route("/api/status")
def status():

    key=request.args.get("key")

    if key!=API_KEY:
        return jsonify({"error":"unauthorized"}),401

    total=alto=medio=baixo=0

    if os.path.exists(LOG):

        with open(LOG) as f:
            for l in f:

                total+=1

                if "ALTO" in l: alto+=1
                elif "MÉDIO" in l: medio+=1
                else: baixo+=1

    return jsonify({
        "total":total,
        "alto":alto,
        "medio":medio,
        "baixo":baixo
    })