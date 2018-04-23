from flask import Flask
from flask import request
import json

app = Flask(__name__)



@app.route("/searchDrug")
def get_ingredient():
    name = request.args.get('active_ingredient')
    ingrediente = """ "substance_name": [
          "SILICON DIOXIDE"
        ]"""
    return ingrediente + name

@app.route("/searchCompany")
def get_company():
    name = request.args.get('company')
    empresa = """ "manufacturer_name": [
          "Rxhomeo Private Limited d.b.a. Rxhomeo, Inc"
        ]"""
    return empresa + name

@app.route("/listDrugs")
def get_drugs():
    #name = request.args.get('drug')
    medicamentos = """ "substance_name": [
          "SILICON DIOXIDE"
        ]"""
    return medicamentos

@app.route("/listCompanies")
def get_listcomp():
    #name = request.args.get('drug')
    empresas = "Rxhomeo Private Limited d.b.a. Rxhomeo, Inc"
    return empresas


if __name__ == "__main__":
    app.run()