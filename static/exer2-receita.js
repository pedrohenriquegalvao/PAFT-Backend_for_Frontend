const pathname = window.location.pathname.split('/');
const idMeal = pathname[pathname.length - 1];
const localURL = 'http://127.0.0.1:5002';

window.onload = () => {
    console.log('oi' + idMeal);
    console.log('\r\n\r\n')
    console.log('salve')
    fetch(`${localURL}/meal/${idMeal}`)
    .then(response => response.json())
    .then(data => {
        if (data) {
            countryData = data['countryData']
            mealData = data['mealData']
            console.log(`Country data: ${Object.keys(countryData)}`)
            console.log(`Meal data: ${Object.keys(mealData)}`)
            let ingredients = []
            let measures = []
            for(let key of Object.keys(mealData)) {
                if(key.toLowerCase().includes('ingredient'))
                    ingredients.push(mealData[key])
                if(key.toLowerCase().includes('measure'))
                    measures.push(mealData[key])
            }
            let mealName = mealData['strMeal']
            let mealImgURL = mealData['strMealThumb']
            let instructionsAux = JSON.stringify(mealData['strInstructions']).replace('"', '').split('\\r\\n')
            let instructions = instructionsAux.join('<br><br>').replace('"', '')
            let category = mealData['strCategory']
            let nomes = ""
            if (countryData['nomeComum'] == countryData['nomeOficial']) 
                nomes = `<li>Nome: ${countryData['nomeComum']}</li>`
            else
                nomes =  `<li>Nome comum: ${countryData['nomeComum']}</li>
                         <li>Nome oficial: ${countryData['nomeOficial']}</li>`
            document.querySelector('.header').innerHTML = `
                                <img src="${mealImgURL}" alt="">
                                <div class="info">
                                    <div class="meal-info">
                                        <h1>${mealName}</h1>
                                        <hr>
                                        <div class="meal-info-text">
                                            <p>Categoria: ${category}</p>
                                            <p>Dificuldade: Mediana</p>
                                        </div>
                                    </div>
                                    <div class="country-info">
                                        <h3>Informações sobre o país de origem</h3>
                                        <ul>
                                            ${nomes}
                                            <li>Região: ${countryData['regiao']}</li>
                                            <li>Capital: ${countryData['capital']}</li>
                                            <li>Moeda: ${countryData['moeda']['nome']} (${countryData['moeda']['simbolo']})</li>
                                        </ul>
                                        <img src="${countryData['bandeira']}" alt="">
                                    </div>
                                </div>
                                `
            let ingredientsAndMeasures = ""
            for (let c = 0; c < ingredients.length; c++) {
                ingredientsAndMeasures += `<li>${ingredients[c]} - ${measures[c]}</li>`
            }
            document.querySelector('.main').innerHTML = `
                                <div class="ingredients">
                                    <h2>Ingredientes e medidas</h2>
                                    <ul>
                                        ${ingredientsAndMeasures}
                                    </ul>
                                </div>
                                <div class="instructions">
                                    <h2>Modo de preparo</h2>
                                    <p>${instructions}</p>
                                </div>
            
                                `

        }
    })
}