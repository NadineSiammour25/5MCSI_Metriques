from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from collections import Counter
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)

@app.route('/')#helloPage
def hello_world():
    return render_template('hello.html') #Commit1
  

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

@app.route("/commits/")
def commits_chart():
    return render_template("commits.html")

@app.route("/api/commits/")
def get_commits_data():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    
    # Vérification de la réponse de l'API
    if response.status_code == 200:
        print("API Call Success")
    else:
        print("API Call Failed, Status Code:", response.status_code)
    
    data = response.json()

    if not data:
        print("Aucun commit trouvé dans la réponse.")
    else:
        print(f"Nombre de commits récupérés : {len(data)}")

    minutes_list = []
    for commit in data:
        try:
            # Extraction de la date de commit
            date_str = commit["commit"]["author"]["date"]
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            minutes_list.append(dt.minute)
        except KeyError as e:
            print("Clé manquante dans un commit", e)

    count_by_minute = dict(Counter(minutes_list))
    formatted_data = [{"minute": m, "count": count_by_minute[m]} for m in sorted(count_by_minute)]

    print(f"Data formatée pour le graphique: {formatted_data}")

    return jsonify(formatted_data)


                                                                                                                                  

if __name__ == "__main__":
  app.run(debug=True)



