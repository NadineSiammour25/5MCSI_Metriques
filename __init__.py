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


@app.route('/commits/')
def commits():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    
    try:
        # Effectuer la requête à l'API GitHub
        response = urlopen(url)
        commits_data = json.loads(response.read().decode('utf-8'))

        # Extraire les minutes des commits
        minutes = []
        for commit in commits_data:
            try:
                commit_date = commit['commit']['author']['date']
                commit_datetime = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
                minute = commit_datetime.strftime('%Y-%m-%d %H:%M')  # Extrait l'année, mois, jour, heure et minute
                minutes.append(minute)
            except KeyError as e:
                print(f"Clé manquante dans le commit: {e}")
                continue  # Ignorer les commits problématiques

        # Compter les commits par minute
        commit_counts = Counter(minutes)

        # Organiser les données pour le graphique
        data = [[minute, count] for minute, count in commit_counts.items()]

        return render_template('commits.html', data=data)
    
    except Exception as e:
        # En cas d'erreur réseau ou autre exceptions
        return jsonify({'error': f'Erreur lors de la récupération des données de l\'API GitHub : {str(e)}'}), 502


if __name__ == '__main__':
    app.run(debug=True)



                                                                                                                                


