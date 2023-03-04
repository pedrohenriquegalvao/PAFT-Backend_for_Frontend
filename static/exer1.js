const form = document.getElementById('meals-form');
const selectCategories = document.getElementById('categories');
const localURL = 'http://127.0.0.1:5002';

window.onload = (() => {
    fetch(`${localURL}/categories`)
    .then(response => response.json())
    .then(data => {
        if(data){
            data.forEach(categoria => {
                opt = document.createElement('option');
                opt.setAttribute('value', categoria['nome_en']);
                opt.innerText = categoria['nome_pt'];
                selectCategories.appendChild(opt)  
            })
        }
    });
})

form.addEventListener("submit",((e) => {
    e.preventDefault();
    document.querySelector('.meals').innerHTML = '';
    for (option of selectCategories) {
        if (option.value !== 'default') {

            if(option.selected) {
                let category = option.innerText
                let parametros = {
                    category: option.value
                }
                let queryString = new URLSearchParams(parametros).toString()
                fetch(`${localURL}/meals?${queryString}`)
                .then(response => response.json())
                .then(data => {
                    let mealLink = ''
                    if (data) {
                        console.log(data)
                        data.forEach(meal => {
                            mealLink = fetchMealLink(meal['idMeal']);
                            document.querySelector('.meals').innerHTML += 
                            `<div class="meal">
                                <img src="${meal['foto']}" alt="">
                                <div class='card-right'>
                                    <div class='card-right-text'>
                                        <div class='card-right-text-title'>
                                            <h2>${meal['titulo']}</h2>
                                            <hr>
                                        </div>    
                                        <div class='card-right-text-content'>
                                            <p>Categoria: ${category}</p>
                                            <p>Dificuldade: Mediana</p>
                                        </div>
                                    </div>
                                    <button class='read-more' id='read-more' onclick='goToMeal(${mealLink})'>Saiba mais</button>
                                </div>
                            </div>`;
                        });
                        
                    }
                    
                });
            }

        }
    }

    


}))

function goToMeal(mealLink) { 
    if(mealLink !== undefined)
        window.open(mealLink, '_blank');
}

function fetchMealLink(idMeal) { // TODO: tornar essa func assincrona, ela esta sendo chamada porém retorna undefined
    let link = ''
    fetch(`${localURL}/meal/${idMeal}`)
    .then(response => response.json())
    .then(data => {
        if (data) 
            link = data['strSource']
        
    })
    return link
}