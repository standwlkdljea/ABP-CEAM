document.addEventListener('DOMContentLoaded', () => {
    console.log("¡JavaScript de VetCuidado cargado correctamente!");

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
                    formCita.reset(); 
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

 
    document.addEventListener('click', async (event) => {
        const botonBorrar = event.target.closest('.btn-borrar');
        
        if (botonBorrar) {
            const clienteId = botonBorrar.getAttribute('data-id');
            // Localizamos la fila completa de la tabla para eliminarla después
            const filaTabla = botonBorrar.closest('tr');

            const seguro = confirm(`¿Estás seguro de que deseas eliminar al cliente #${clienteId}? Esta acción no se puede deshacer.`);
            
            if (!seguro) return; // Si cancela, no hacemos nada

            console.log(`Solicitando al backend la eliminación del cliente ID: ${clienteId}`);

            try {
                const response = await fetch(`/api/clientes/${clienteId}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    filaTabla.remove();
                    alert("Usuario eliminado correctamente del sistema y de la base de datos. 🗑️");
                } else {
                    alert(`Error ${response.status}: No se pudo eliminar al usuario.`);
                }
            } catch (error) {
                console.error("Error al intentar comunicar con la API de borrado:", error);
                alert("Hubo un error de conexión con el servidor backend.");
            }
        }
    });
});