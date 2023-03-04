'''
TheNewsAPI
Site: https://www.thenewsapi.com/documentation 
API Key: b7iyvQTBOaOJaAjPAW1L9aBjVo4l4Up6kQvgcwhE
Exemplo de request: “https://api.thenewsapi.com/v1/news/top?api_token=b7iyvQTBOaOJaAjPAW1L9aBjVo4l4Up6kQvgcwhE&locale=br&language=pt&limit=3”

RestCountries
Site: https://restcountries.com/
API Key: Não precisa
Exemplo de request: “https://restcountries.com/v3.1/name/peru”

'''

from flask import Flask, request, render_template
import requests
from googletrans import Translator

translator = Translator()

app = Flask(__name__)
# @app.route('/noticia')
# def noticia():
#     country = request.args.get('country')
#     respNews = requests.get('https://api.thenewsapi.com/v1/news/top?api_token=b7iyvQTBOaOJaAjPAW1L9aBjVo4l4Up6kQvgcwhE&limit=10')
#     jsonNews = respNews.json()
#     noticias = []
#     for noticia in jsonNews['data']:
#         noticiaData = {
#         'titulo': translator.translate(noticia['title'], dest='pt').text,
#         'descricao': translator.translate(noticia['description'], dest='pt').text,
#         'foto': noticia['image_url'],
#         'link': noticia['url'],
#         'data': noticia['published_at'],
#         'fonte': noticia['source'],
#         'pais': noticia['locale']
#         }
#         noticias.append(noticiaData)
#     return noticias 
    

@app.route('/receitas-exer1')
def receitas():
    return render_template('receitas-exer1.html')

@app.route('/receita/<int:idMeal>')
def receita(idMeal):
    return render_template('receita.html')

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
        if (value != None and value != ''): # Verifica e adiciona nos dados da receita apenas as chaves cujos valores não são vazios.
            # mealData.update({f'{key}':value})
            mealData.update({f'{key}':translator.translate(value, dest='pt').text}) # TODO: verificar 175g virando 175 EGP no meal id=52959
    return mealData

app.run(debug=True, port=5002)

