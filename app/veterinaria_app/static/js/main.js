document.addEventListener('DOMContentLoaded', () => {
  console.log("¡JavaScript enlazado con éxito a citas.html!");

  const formCita = document.getElementById('formCita');

  if (formCita) {
    formCita.addEventListener('submit', async (event) => {
      event.preventDefault();
      const dueno = document.getElementById('nombre_dueno').value;
      const mascota = document.getElementById('nombre_mascota').value;
      const especie = document.getElementById('tipo_mascota').value;
      const fecha = document.getElementById('fecha_cita').value;
      const motivoConsulta = document.getElementById('motivo').value;


      const datosCita = {
        nombre_dueno: dueno,
        dni_dueno: document.getElementById('dni_dueno').value,
        email_dueno: document.getElementById('email_dueno').value,
        nombre_mascota: mascota,
        tipo_mascota: especie,
        fecha_cita: fecha,
        motivo: motivoConsulta
      };

      console.log("Enviando datos de la cita al backend:", datosCita);

      try {
        const response = await fetch('/api/citas', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(datosCita)
        });

        if (response.status === 201) {
          alert("¡Cita agendada de forma rápida y segura! Nos vemos pronto. 🐾");
          formCita.reset(); // Limpia el formulario
        } else if (response.status === 400) {
          alert("Error 400: Los datos enviados son incorrectos.");
        } else {
          alert("Error " + response.status + ": No se pudo guardar la cita.");
        }
      } catch (error) {
        console.error("Error crítico de comunicación con la API:", error);
        alert("No se pudo conectar con el servidor backend.");
      }
    });
  }
});
