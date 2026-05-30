document.addEventListener('DOMContentLoaded', () => {
    console.log('🐾 VetCuidado JS cargado correctamente.');

    const formCita = document.getElementById('formCita');
    const errorDiv = document.getElementById('error-msg');
    const fechaInput = document.getElementById('inicio');
    const horarioInfo = document.getElementById('horario-info');

    if (fechaInput && horarioInfo) {
        fechaInput.addEventListener('change', async () => {
            const val = fechaInput.value;
            if (!val) return;
            const fecha = val.split('T')[0];
            try {
                const resp = await fetch(`/citas/api/horario?fecha=${fecha}`);
                const data = await resp.json();
                horarioInfo.classList.remove('hidden');
                if (data.laboral) {
                    horarioInfo.textContent = `🕐 Horario: ${data.hora_apertura} – ${data.hora_cierre}`;
                    horarioInfo.className = 'text-xs text-emerald-600 mt-1';
                } else {
                    horarioInfo.textContent = '⚠️ ' + data.mensaje;
                    horarioInfo.className = 'text-xs text-red-500 mt-1';
                }
            } catch {
                horarioInfo.classList.add('hidden');
            }
        });
    }

    if (formCita && errorDiv) {
        formCita.addEventListener('submit', async (e) => {
            e.preventDefault();
            errorDiv.classList.add('hidden');

            const payload = {
                id_mascota: formCita.id_mascota.value,
                servicio_id: formCita.servicio_id.value,
                inicio: formCita.inicio.value,
                motivo: formCita.motivo.value
            };

            try {
                const resp = await fetch('/citas/api/agendar', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const data = await resp.json();
                if (data.status === 'success') {
                    window.location.href = '/citas';
                } else {
                    errorDiv.textContent = '⚠️ ' + data.mensaje;
                    errorDiv.classList.remove('hidden');
                }
            } catch {
                errorDiv.textContent = '⚠️ Error al conectar con el servidor.';
                errorDiv.classList.remove('hidden');
            }
        });
    }
});
