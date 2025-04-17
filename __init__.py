from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime,timedelta  
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

# Définir le décalage horaire pour Paris (UTC+2 pendant l'heure d'été)
# Vous pouvez ajuster le décalage si nécessaire, par exemple en UTC+1 en hiver
UTC_OFFSET = timedelta(hours=2)  # Décalage pour l'heure d'été (Paris)

@app.route('/commits/')
def commits():
    # Récupérer les commits depuis l'API GitHub avec urllib
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = urlopen(url)  # Utilisation de urllib pour ouvrir l'URL
    commits_data = json.loads(response.read())  # Lire et décoder la réponse JSON
    
    # Créer un dictionnaire pour compter les commits par minute
    commits_per_minute = {}

    # Analyser chaque commit et convertir son timestamp
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']  # La date du commit
        commit_time_utc = datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ")  # Date en UTC
        
        # Convertir UTC en temps local en ajoutant le décalage horaire
        commit_time_local = commit_time_utc + UTC_OFFSET  # Appliquer le décalage horaire
        
        # Extraire la minute du commit
        commit_minute = commit_time_local.strftime('%Y-%m-%d %H:%M')  # Format "2025-04-17 14:35"
        
        # Comptabiliser le commit par minute
        if commit_minute not in commits_per_minute:
            commits_per_minute[commit_minute] = 1
        else:
            commits_per_minute[commit_minute] += 1

    # Créer les données à passer au graphique
    data = []
    for minute, count in commits_per_minute.items():
        data.append([minute, count])
    
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)



                                                                                                                                


