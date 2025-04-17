from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from collections import Counter
from urllib.request import urlopen
import sqlite3
import requests

                                                                                                                                       
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


# Route pour afficher le graphique des commits
@app.route('/commits/')
def commits():
    # Récupérer les commits depuis l'API GitHub
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()

    # Extraire les minutes des commits
    minutes = []
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        commit_datetime = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        minute = commit_datetime.strftime('%Y-%m-%d %H:%M')  # Extrait l'année, mois, jour, heure et minute
        minutes.append(minute)

    # Compter les commits par minute
    commit_counts = Counter(minutes)

    # Organiser les données pour le graphique
    data = []
    for minute, count in commit_counts.items():
        data.append([minute, count])

    return render_template('commits.html', data=data)

# Route pour extraire les minutes (optionnel, utilisé pour tester la date)
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

if __name__ == '__main__':
    app.run(debug=True)



                                                                                                                                


