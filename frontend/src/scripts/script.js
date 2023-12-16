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
      // Si se ha alcanzado la última pregunta, volver a la página de inicio
      if (currentQuestionIndex === questions.length - 1) {
        window.location.href = '/questionaris/';
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
  