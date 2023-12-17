
function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(";");
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == " ") {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function setCookie(cname, cvalue) {
    document.cookie = cname + "=" + cvalue + ";path=/";
}

document.addEventListener('DOMContentLoaded', function () {
    const nextButton = document.getElementById('next-button');
    const questions = [
        {
            pregunta: 'Pregunta 1',
            textoH3: 'Sangra durant més de set dies al mes?'
        },
        {
            pregunta: 'Pregunta 2',
            textoH3: 'Té tres o més dies de sagnat més abundant durant la seva menstruació?'
        },
        {
            pregunta: 'Pregunta 3',
            textoH3: 'En general, la seva regla li resulta especialment molesta a causa de la seva abundància?'
        },
        {
            pregunta: 'Pregunta 4',
            textoH3: 'En algun dels dies de sagnat més abundant taca la roba a les nits; o la tacaria si no fes servir doble protecció o es canviés durant la nit?'
        },
        {
            pregunta: 'Pregunta 5',
            textoH3: 'Durant els dies de sagnat més abundant li preocupa tacar el seient de la seva cadira, sofà, etc...?'
        },
        {
            pregunta: 'Pregunta 6',
            textoH3: 'En general, en els dies de sagnat més abundant, evita (en la mesura del possible) algunes activitats, viatges o plaers d’oci perquè deu canviar-se sovint de tampó o la compresa?'
        }
    ];

    let currentQuestionIndex = 0;
    let score = 0;

    // Función para mostrar la pregunta actual
    function showCurrentQuestion() {
        const currentQuestion = questions[currentQuestionIndex];
        const h2Element = document.getElementsByTagName('h2')[0];
        const h3Element = document.getElementsByTagName('h3')[0];

        h2Element.textContent = currentQuestion.pregunta;
        h3Element.textContent = currentQuestion.textoH3;
    }

    // Función para manejar el clic en el botón "Siguiente"
    function handleNextButtonClick() {
        // Sumar puntos según la respuesta seleccionada
        if (document.getElementById('Si').checked == true) {
            if (currentQuestionIndex === 0 || currentQuestionIndex === 2) score += 3;
            else ++score;
        }

        // Si se ha alcanzado la última pregunta, mostrar el puntaje
        if (currentQuestionIndex === questions.length - 1) {
            //Implementar el querri cap a la BD
            if (score >= 3) alert(`Atencio! Puntuació de ${score} punts`);
            else alert(`Puntuació de ${score} punts`);

            // hacer la petición al back

            let usuari = getCookie("username")
            console.log(usuari);

            fetch("http://192.168.45.49:8000/api/upload_encuesta_qol/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    usuari: usuari,
                    punts: score
                }),
            })
                .then((response) => response.json())
                .catch((error) => {
                    // Handle any errors that occurred during the fetch
                    console.error("Error during fetch:", error);
                    alert("Error al comunicar-se amb el servidor");
                });
            // Puedes redirigir o realizar otras acciones según sea necesario
            // window.location.href = '/questionaris/';
            return; // Evitar ejecutar el resto del código si ya hemos redirigido
        }

        // Actualizar el índice de la pregunta actual
        currentQuestionIndex++;

        // Mostrar la pregunta actualizada
        showCurrentQuestion();
    }

    // Configurar el evento clic para el botón "Siguiente"
    nextButton.addEventListener('click', handleNextButtonClick);

    // Mostrar la primera pregunta al cargar la página
    showCurrentQuestion();
});
