'''

APIs utilizadas

TheMealDB
Site: https://www.themealdb.com/api.php
API Key: Não precisa

RestCountries
Site: https://restcountries.com/
API Key: N/A

'''

from flask import Flask, request, render_template
import requests
from googletrans import Translator

translator = Translator()

COUNTRIES = { 'American' : "us", 'Canadian' : "ca", 'British' : 'gb', 'Chinese' : 'cn', 'Croatian' : 'hr', 'Dutch' : 'nl', 'Egyptian' : 'eg', 'French' : 'fr',
'Greek' : 'gr', 'Indian' : 'in', 'Irish' : 'ie', 'Italian' : 'it',  'Jamaican' : 'jm', 'Japanese' : 'jp', 'Kenyan' : 'ke', 'Malaysian' : 'my', 'Mexican' : 'mx', 'Maroccan' : 'ma', 'Polish' : 'pl', 'Portuguese' : 'pt', 'Russian' : 'ru', 'Spanish' : 'es', 'Thai' : 'th', 'Tunisian' : 'tn', 'Turkish' : 'tr', 'Unknown' : '', 'Vietnamese' : 'vn' }

app = Flask(__name__)
    
@app.route('/receitas-exer1')
def receitas():
    return render_template('receitas-exer1.html')

@app.route('/receitas-exer2')
def receitasExer2():
    return render_template('receitas-exer2.html')

@app.route('/receita/<int:idMeal>')
def receita(idMeal):
    return render_template('receita-exer2.html')

@app.route('/categories')
def categories():
    respCategories = requests.get('https://www.themealdb.com/api/json/v1/1/list.php?c=list')
    jsonCategories = respCategories.json()['meals']
    categories = []
    for c in range(0,11):
        category = jsonCategories[c]
        translated = translator.translate(category['strCategory'], dest='pt').text
        categoryData = { # Adaptando o conteúdo da categoria
            'nome_en': category['strCategory'],
            'nome_pt': translated if translated != 'Lado' else 'Acompanhamento'
        }
        categories.append(categoryData)
    return categories


@app.route('/meals')
def meals():
    category = request.args.get('category')
    respMeals = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category}')
    jsonMeals = respMeals.json()['meals']
    limit = len(jsonMeals) if len(jsonMeals) <= 10 else 10 
# Se houver menos de 10 receitas, o limite é essa quantidade. Caso tenha mais de 10 receitas, o limite é cravado em 10.
    meals = []
    for c in range(0,limit):
        meal = jsonMeals[c]
        mealData = {
        'titulo': translator.translate(meal['strMeal'], dest='pt').text,
        'foto': meal['strMealThumb'],
        'idMeal': meal['idMeal']
        }
        meals.append(mealData)
    return meals 


@app.route('/meal/<int:idMeal>')
def meal(idMeal):
    respMeal = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={idMeal}")
    jsonMeal = respMeal.json()['meals'][0]
    mealData = {}
    for key, value in jsonMeal.items():
        # Verifica e adiciona nos dados da receita apenas as chaves cujos valores não são vazios.
        if (value != None and str(value).strip() != ''): 
            
            if 'strMeasure' in str(key) and ('ml' in str(value) or 'g' in str(value) ):
                mealData.update({f'{key}':value}) # Não traduz o valor
            else:
                mealData.update({f'{key}':str(translator.translate(value, dest='pt', src='en').text).capitalize()}) # Traduz o valor

    countryCode = COUNTRIES[jsonMeal['strArea']]
    respCountry = requests.get(f"https://restcountries.com/v3.1/alpha/{countryCode}")
    jsonCountry = respCountry.json()[0]
    moeda = {}
    for key,value in jsonCountry['currencies'].items():
        moeda.update( {'nome' : translator.translate(value['name'], dest='pt', src='en').text.capitalize()} )
        moeda.update( {'simbolo' : value['symbol']} )
    countryData = {
        'nomeComum' : jsonCountry['translations']['por']['common'],
        'nomeOficial' : jsonCountry['translations']['por']['official'],
        'regiao' : translator.translate(jsonCountry['region'], dest='pt', src='en').text.capitalize(),
        'capital' : jsonCountry['capital'][0],
        'moeda' : moeda,
        'bandeira' : jsonCountry['flags']['png']
    }
    data = {'mealData' : mealData, 'countryData' : countryData}
    return data

# Exercício 3
@app.route('/meals-template-engine')
def mealsTemplateEngine():
    category = {
        'realName' : 'Seafood',
        'translatedName': 'Frutos do mar'
    }
    respMeals = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?c={category["realName"]}')
    jsonMeals = respMeals.json()['meals']
    limit = len(jsonMeals) if len(jsonMeals) <= 10 else 10 
# Se houver menos de 10 receitas, o limite é essa quantidade. Caso tenha mais de 10 receitas, o limite é cravado em 10.
    meals = []
    for c in range(0,limit):
        meal = jsonMeals[c]
        mealData = {
            'titulo': translator.translate(meal['strMeal'], dest='pt').text,
            'categoria': category['translatedName'],
            'foto': meal['strMealThumb'],
            'idMeal': meal['idMeal']
        }
        meals.append(mealData)
    return render_template('meals-template-engine.html', meals=meals) 


app.run(debug=True, port=5002)

