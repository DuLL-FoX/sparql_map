import requests

from flask import Flask, request, jsonify, render_template
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)


def run_sparql_query(country_name):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>

    SELECT ?country ?abstract ?capital ?populationTotal
    WHERE {{
      BIND(dbr:{} AS ?country)
      ?country dbo:abstract ?abstract .
      ?country dbo:capital ?capital .
      ?country dbo:populationTotal ?populationTotal .
      FILTER (lang(?abstract) = 'en')
    }}
    """.format(country_name.replace(" ", "_"))

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def get_country_from_coords(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&accept-language=en"
    response = requests.get(url)
    data = response.json()
    return data.get('address', {}).get('country', '')


@app.route('/get_country_by_coords', methods=['POST'])
def get_country_by_coords():
    data = request.json
    lat, lon = data['lat'], data['lon']
    country_name = get_country_from_coords(lat, lon)
    result = run_sparql_query(country_name)
    return jsonify(result)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
