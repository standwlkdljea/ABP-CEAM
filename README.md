# ABP-CEAM

Clínica Veterinaria VetCuidado — sistema de gestión de citas, clientes y doctores.

## Requisitos

- Python 3.10+
- MySQL (base de datos `vetcuidado_db`, crear con `Script SQL ABP final.txt`)

## Instalación

```bash
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Iniciar el servidor

```bash
python run.py
```

El servidor arranca en `http://127.0.0.1:5000`.

## Modo debug

El modo debug está activado por defecto en `run.py`. Recarga automática y stack traces detallados en el navegador.

Para desactivarlo, editar `run.py`:

```python
app.run(host='0.0.0.0', port=5000, debug=False)
```
