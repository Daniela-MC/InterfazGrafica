from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

def extraer_valor_tag(tags, clave):
    for tag in tags:
        if tag["key"] == clave:
            return tag["value"]
    return "-"

def obtener_snapshots(instance_id, nombre, contrasena):
    try:
        url = f"https://awstools.corp.latiniaservices.com/api/v1/instance/{instance_id}/snapshot"
        response = requests.get(url, auth=(nombre, contrasena))
        if response.status_code == 200:
            snapshots = response.json()
            if isinstance(snapshots, list):
                nombres = [s.get("name", "-") for s in snapshots]
                return ", ".join(nombres) if nombres else "-"
        return "-"
    except Exception as e:
        print(f"[ERROR] Snapshot error: {e}")
        return "-"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form.get("user", "").strip()
        contrasena = request.form.get("password", "").strip()

        if not nombre or not contrasena:
            return render_template_string(PAGINA_LOGIN, error=False)

        try:
            url = "https://awstools.corp.latiniaservices.com/api/v1/instance"
            response = requests.get(url, auth=(nombre, contrasena))
            if response.status_code == 200:
                data = response.json()
                tabla_html = generar_tabla(data, nombre, contrasena)
                return render_template_string(PAGINA_RESULTADO, nombre=nombre, tabla=tabla_html)
            elif response.status_code == 401:
                return render_template_string(PAGINA_LOGIN, error=True)
            else:
                return f"⚠️ Error al obtener datos. Código: {response.status_code}"
        except Exception as e:
            return f"🔌 Error de conexión: {e}"

    return render_template_string(PAGINA_LOGIN, error=False)

def badge(valor):
    try:
        return f'<span class="badge">{valor}</span>' if int(valor) > 0 else valor
    except:
        return valor

def generar_tabla(data, nombre, contrasena):
    filas = ""

    for instancia in data:
        instance_id = instancia.get("id", "-")
        snapshots = obtener_snapshots(instance_id, nombre, contrasena)
        estado_raw = instancia.get("status", {}).get("status", "-")
        estado = "ON" if estado_raw == "POWERED_ON" else "OFF" if estado_raw == "POWERED_OFF" else estado_raw
        valores = [
            instancia.get("name", "-"),
            estado,
            extraer_valor_tag(instancia.get("tags", []), "UsedBy"),
            extraer_valor_tag(instancia.get("tags", []), "PowerOnTime"),
            extraer_valor_tag(instancia.get("tags", []), "PowerOffTime"),
            extraer_valor_tag(instancia.get("tags", []), "OperGroup"),
            extraer_valor_tag(instancia.get("tags", []), "Notes"),
            snapshots
        ]
        estado_color = "green" if "ON" in valores[1].upper() else "red" if "OFF" in valores[1].upper() else "black"

        fila = "<tr>" + "".join(
            f'<td class="center" style="color:{estado_color}">{val}</td>' if i == 1 else
            f'<td class="center">{badge(val)}</td>' if i in [3, 4] else
            f'<td class="center">{val}</td>' if i in [2, 5] else
            f'<td>{val}</td>'
            for i, val in enumerate(valores)
        ) + "</tr>"
        filas += fila
    return filas

# ==========================
# Página de LOGIN
# ==========================
PAGINA_LOGIN = """
<!DOCTYPE html>
<html>
<head>
    <title>QA Systems Manager</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            height: 100vh;
            position: relative;
            overflow: hidden;
        }

        .background {
            background: url('https://i.ytimg.com/vi/m2AuliEdbQg/maxresdefault.jpg') no-repeat center center fixed;
            background-size: cover;
            filter: brightness(0.6);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }

        .container {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            z-index: 1;
        }

        h1 {
            font-size: 36px;
            color: white;
            text-shadow: 2px 2px 6px rgba(0,0,0,0.6);
            margin-bottom: 25px;
        }

        .login-box {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0,0,0,0.3);
            width: 320px;
        }

        .login-box h2 {
            text-align: center;
            margin-bottom: 20px;
        }

        .error-message {
            text-align: center;
            color: red;
            font-weight: bold;
            margin-bottom: 15px;
            font-size: 14px;
        }

        .error-image {
            display: block;
            margin: 0 auto 10px auto;
            width: 80px;
        }

        form {
            display: flex;
            flex-direction: column;
        }

        .input-group {
            position: relative;
            margin-bottom: 15px;
        }

        .input-group i.fa-user,
        .input-group i.fa-lock {
            position: absolute;
            top: 50%;
            left: 10px;
            transform: translateY(-50%);
            color: #999;
        }

        .toggle-password {
            position: absolute;
            top: 50%;
            right: 10px;
            transform: translateY(-50%);
            cursor: pointer;
            color: #999;
        }

        .input-group input {
            width: 100%;
            padding: 10px 35px 10px 35px;
            border: 1px solid #ccc;
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 14px;
        }

        input[type="submit"] {
            background: #2196f3;
            color: white;
            font-weight: bold;
            padding: 10px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
        }

        input[type="submit"]:hover {
            background: #1976d2;
        }
    </style>
</head>
<body>
    <div class="background"></div>

    <div class="container">
        <h1>QA Systems Manager</h1>

        <div class="login-box">
            <h2>Iniciar sesión</h2>

            {% if error is defined and error %}
                <img src="https://cdn3d.iconscout.com/3d/premium/thumb/acceso-de-hacker-14622078-11815532.png?f=webp" alt="intruder" class="error-image">
                <div class="error-message">Credenciales incorrectas... ¿Intruso?</div>
            {% endif %}

            <form method="post">
                <div class="input-group">
                    <i class="fas fa-user"></i>
                    <input type="text" name="user" placeholder="Usuario" required>
                </div>
                <div class="input-group">
                    <i class="fas fa-lock"></i>
                    <input type="password" id="password" name="password" placeholder="Contraseña" required>
                    <i class="fas fa-eye toggle-password" id="togglePassword"></i>
                </div>
                <input type="submit" value="Ingresar">
            </form>
        </div>
    </div>

    <script>
        const togglePassword = document.getElementById('togglePassword');
        const passwordField = document.getElementById('password');

        togglePassword.addEventListener('click', () => {
            const isPassword = passwordField.type === 'password';
            passwordField.type = isPassword ? 'text' : 'password';
            togglePassword.classList.toggle('fa-eye');
            togglePassword.classList.toggle('fa-eye-slash');
        });

        togglePassword.classList.add('fa-eye');
    </script>
</body>
</html>
"""

# ==========================
# Página de RESULTADOS
# ==========================

PAGINA_RESULTADO = """
<!DOCTYPE html>
<html>
<head>
    <title>QA Systems Manager</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #f8f9fa;
            padding: 30px;
        }
        
        .header {
            position: relative;
            width: 100%;
            margin-bottom: 20px;
        }

        .banner {
            width: 100%;
            height: auto;
            display: block;
        }
        
        
        .banner-text {
            position: absolute;
            top: 50%;
            left: 80%;
            transform: translate(-50%, -50%);
            color: white;
            font-size: 22px;
            font-weight: 500;
            font-family: 'Segoe UI', sans-serif;
            white-space: nowrap;
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
        }
    
        table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
        }
    
        thead th {
            background-color: #dbe4f0; /* gris azulado */
            color: #1a237e; /* azul fuerte */
            text-align: center;
            padding: 12px;
            font-weight: 600;
            border-bottom: 2px solid #ccc;
            position: sticky;
            top: 0;
            z-index: 1;
            transition: color 0.3s ease;
        }
    
        thead th:hover {
            color: #f57c00; /* naranja al pasar el mouse */
            cursor: default;
        }
    
        tbody tr:nth-child(even) {
            background-color: #f9f9f9;
        }
    
        tbody tr:nth-child(odd) {
            background-color: #ffffff;
        }
    
        td {
            padding: 12px;
            text-align: center;
            color: #333;
            border-bottom: 1px solid #eee;
            word-wrap: break-word;
        }
    
        td.center {
            text-align: center;
        }
    
        /* Ancho reducido para columnas específicas */
        thead th:nth-child(2),
        tbody td:nth-child(2) { width: 80px; }
        
        thead th:nth-child(3),
        tbody td:nth-child(3) { width: 100px; }
    
        thead th:nth-child(4),
        tbody td:nth-child(4) { width: 90px; }
    
        thead th:nth-child(5),
        tbody td:nth-child(5) { width: 90px; }
    
        /* Badge para valores destacados */
        .badge {
            background-color: orange;
            color: white;
            font-weight: bold;
            padding: 4px 8px;
            border-radius: 6px;
            display: inline-block;
            min-width: 28px;
        }
    </style>
</head>
<body>
    <div class="header">
        <img src="/static/headerLatinia.png" alt="LATINIA System Manager QA" class="banner">
        <div class="banner-text">Bienvenido {{ nombre }} 🎉</div>
    </div>
    <table>
        <thead>
            <tr>
                <th>Nombre</th>
                <th>Estado</th>
                <th>Usado por</th>
                <th>PowerON</th>
                <th>PowerOFF</th>
                <th>OperGroup</th>
                <th>Notas</th>
                <th>Snapshot</th>
            </tr>
        </thead>
        <tbody>
            {{ tabla|safe }}
        </tbody>
    </table>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
