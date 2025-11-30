const jokeDiv = document.getElementById('joke');
const explanationDiv = document.getElementById('explanation');
const nextJokeBtn = document.getElementById('nextJokeBtn');
const explainJokeBtn = document.getElementById('explainJokeBtn');
const scriptTag = document.currentScript;
const url = scriptTag.getAttribute('data-url');

async function generateJoke() {
    explanationDiv.innerHTML = "";
    explanationDiv.parentElement.classList.add('hidden');

    const config = {
        headers: {
            'Accept': 'application/json'
        }
    };

    const res = await fetch('https://icanhazdadjoke.com', config);
    const data = await res.json();
    jokeDiv.innerHTML = data.joke;
}

generateJoke();

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the name we want
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function explainJoke() {
    const currentJoke = jokeDiv.innerHTML;
    console.log("The joke: ", currentJoke);
    console.log("URL: ", url);

    try {
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ joke: currentJoke })
        });

        console.log("Response status: ", res.status);

        const reader = res.body.getReader();
        const decoder = new TextDecoder('utf-8');
        let result = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            result += decoder.decode(value);
            explanationDiv.innerHTML = result;
            explanationDiv.parentElement.classList.remove('hidden');
        }
        
    } catch (error) {
        console.error("Error in explainJoke function: ", error);
        alert('An error occurred while explaining the joke.');
    }
}

nextJokeBtn.addEventListener('click', generateJoke);
explainJokeBtn.addEventListener('click', explainJoke);