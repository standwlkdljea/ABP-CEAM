document.addEventListener('DOMContentLoaded', () => {
  // ==============  PET MANAGEMENT (mascotas.html) ==============
  const petsContainer = document.getElementById('petsContainer');
  if (petsContainer) {
    if (typeof petsData === 'undefined') {
      console.warn('No pets data provided');
      return;
    }
    renderPets(petsData);

    const modal = document.getElementById('modalAddPet');
    document.getElementById('btnAddPet')?.addEventListener('click', () => modal.classList.remove('hidden'));
    document.getElementById('btnCloseModal')?.addEventListener('click', () => modal.classList.add('hidden'));

    document.getElementById('formAddPet')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = {
        nombre_mascota: document.getElementById('petName').value,
        tipo_mascota: document.getElementById('petType').value,
        edad: document.getElementById('petAge').value,
        descripcion: document.getElementById('petDesc').value
      };
      try {
        const res = await fetch('/api/pets', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (res.ok) {
          const updated = await fetch('/api/pets');
          const pets = await updated.json();
          renderPets(pets);
          modal.classList.add('hidden');
          e.target.reset();
        } else {
          alert('Error al agregar mascota');
        }
      } catch (err) {
        console.error(err);
        alert('Error de conexión');
      }
    });

    window.deletePet = async (petId) => {
      if (!confirm('¿Eliminar esta mascota?')) return;
      const res = await fetch(`/api/pets/${petId}`, { method: 'DELETE' });
      if (res.ok) {
        const updated = await fetch('/api/pets');
        const pets = await updated.json();
        renderPets(pets);
      } else {
        alert('No se pudo eliminar');
      }
    };
  }

  function renderPets(pets) {
    if (!petsContainer) return;
    let html = '';
    if (pets.length === 0) {
      html = `<div class="col-span-full text-center py-16 text-gray-500">Aún no has registrado mascotas.</div>`;
    } else {
      pets.forEach(pet => {
        html += `
          <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-col justify-between">
            <div>
              <h3 class="text-xl font-bold text-gray-900">${pet.nombre_mascota}</h3>
              <p class="text-gray-500 text-sm mt-1">${pet.tipo_mascota}, ${pet.edad} años</p>
              <p class="text-gray-600 text-sm mt-2">${pet.descripcion || 'Sin descripción'}</p>
            </div>
            <div class="mt-4 flex justify-end gap-2">
              <button onclick="deletePet(${pet.id})" class="text-red-600 hover:text-red-800 text-sm font-medium">🗑️ Eliminar</button>
            </div>
          </div>`;
      });
    }
    petsContainer.innerHTML = html;
  }

  // ==============  BOOKING FORM (citas.html) ==============
  const formCita = document.getElementById('formCita');
  if (formCita) {
    formCita.addEventListener('submit', async (event) => {
      event.preventDefault();
      const pet_id = document.getElementById('pet_id').value;
      const service_id = document.getElementById('service_id').value;
      const start_time = document.getElementById('start_time').value;
      const motivo = document.getElementById('motivo').value.trim();

      if (!pet_id || !service_id || !start_time || !motivo) {
        alert('Todos los campos son obligatorios');
        return;
      }

      const payload = {
        pet_id: parseInt(pet_id),
        service_id: parseInt(service_id),
        start_time: start_time,
        motivo: motivo
      };

      try {
        const response = await fetch('/api/citas', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (response.status === 201) {
          alert('¡Cita agendada correctamente! 🐾');
          formCita.reset();
        } else if (response.status === 400) {
          const err = await response.json();
          alert('Error: ' + (err.message || 'Datos incorrectos'));
        } else if (response.status === 401) {
          alert('Debes iniciar sesión como cliente.');
        } else {
          alert('Error inesperado');
        }
      } catch (error) {
        console.error(error);
        alert('Error de conexión con el servidor');
      }
    });
  }
});
