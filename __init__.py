from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)

@app.route("/contact/") #Formulaire de contact
def MaPremiereAPI():
    return render_template("contact.html")


@app.route('/tawarano/') #DonnéeMeteo
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  

@app.route("/rapport/")#Rapport
def mongraphique():
    return render_template("graphique.html")



@app.route("/histogramme/")#histogramme
def monhisto():
  return render_template("histogramme.html")


                                                                                                                                       
@app.route('/')#helloPage
def hello_world():
    return render_template('hello.html') #Commit


  
if __name__ == "__main__":
  app.run(debug=True)



