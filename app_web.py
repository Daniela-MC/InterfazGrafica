from flask import Flask, request, render_template_string, jsonify, session
import requests
import json

app = Flask(__name__)
app.secret_key = "una-clave-secreta-y-larga"

def extraer_valor_tag(tags, clave):
    for tag in tags:
        if tag["key"] == clave:
            return tag["value"]
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
                tabla_html = generar_tabla(data)

                session["nombre"] = nombre
                session["contrasena"] = contrasena

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

def generar_tabla(data):
    filas = ""

    for instancia in data:
        instance_id = instancia.get("id", "-")
        estado_raw = instancia.get("status", {}).get("status", "-")
        estado = "ON" if estado_raw == "POWERED_ON" else "OFF" if estado_raw == "POWERED_OFF" else estado_raw

        safe_id = instance_id.replace("-", "")
        lupa_html = f'<i class="fas fa-search lupa" data-id="{safe_id}" data-instance="{instance_id}"></i>'

        valores = [
            instancia.get("name", "-"),
            estado,
            extraer_valor_tag(instancia.get("tags", []), "UsedBy"),
            extraer_valor_tag(instancia.get("tags", []), "PowerOnTime"),
            extraer_valor_tag(instancia.get("tags", []), "PowerOffTime"),
            extraer_valor_tag(instancia.get("tags", []), "OperGroup"),
            extraer_valor_tag(instancia.get("tags", []), "Notes"),
            lupa_html
        ]

        fila = "<tr>" + "".join(
            f'<td class="center"><span class="status-on">ON</span></td>' if i == 1 and val == "ON" else
            f'<td class="center"><span class="status-off">OFF</span></td>' if i == 1 and val == "OFF" else
            f'<td class="center">{badge(val)}</td>' if i in [3, 4] else
            f'<td class="center">{val}</td>' if i in [2, 5] else
            f'<td>{val}</td>'
            for i, val in enumerate(valores)
        ) + "</tr>"
        filas += fila

    return filas

@app.route("/snapshots/<instance_id>")
def obtener_snapshots(instance_id):
    try:
        nombre = session.get("nombre")
        contrasena = session.get("contrasena")

        if not nombre or not contrasena:
            return jsonify({"error": "No autorizado"}), 401

        url = f"https://awstools.corp.latiniaservices.com/api/v1/instance/{instance_id}/snapshot"
        response = requests.get(url, auth=(nombre, contrasena))
        if response.status_code == 200:
            snapshots = response.json()
            return jsonify(snapshots)
        else:
            return jsonify({"error": "No se pudieron obtener snapshots"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/logout")
def logout():
    session.clear()
    return render_template_string(PAGINA_LOGIN, error=False)


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
                    <input type="text" name="user" placeholder="User" required>
                </div>
                <div class="input-group">
                    <i class="fas fa-lock"></i>
                    <input type="password" id="password" name="password" placeholder="Password" required>
                    <i class="fas fa-eye toggle-password" id="togglePassword"></i>
                </div>
                <input type="submit" value="Login">
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
# Página de RESULTADO
# ==========================

PAGINA_RESULTADO = """
<!DOCTYPE html>
<html>
<head>
    <title>QA Systems Manager</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
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
            right: 30px;
            transform: translateY(-50%);
            color: white;
            font-size: 22px;
            font-weight: 500;
            font-family: 'Segoe UI', sans-serif;
            white-space: nowrap;
            display: flex;
            align-items: center;
            gap: 14px;
            z-index: 1;
        }

        .avatar-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid white;
            cursor: pointer;
        }

        .avatar-menu-container {
            position: relative;
            display: inline-block;
        }

        .dropdown-content {
            display: none;
            position: absolute;
            right: 0;
            background: white;
            border: 1px solid #ccc;
            border-radius: 6px;
            min-width: 100px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.15);
            z-index: 10;
        }

        .dropdown-content a {
            display: block;
            padding: 8px;
            color: black;
            text-decoration: none;
            font-size: 14px;
        }

        .dropdown-content a:hover {
            background-color: #f0f0f0;
        }

        .status-on {
            background-color: #4caf50;
            color: white;
            font-weight: bold;
            padding: 4px 10px;
            border-radius: 6px;
            display: inline-block;
            min-width: 40px;
        }

        .status-off {
            background-color: #f44336;
            color: white;
            font-weight: bold;
            padding: 4px 10px;
            border-radius: 6px;
            display: inline-block;
            min-width: 40px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
        }

        thead th {
            background-color: #dbe4f0;
            color: #1a237e;
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
            color: #f57c00;
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

        .badge {
            background-color: orange;
            color: white;
            font-weight: bold;
            padding: 4px 8px;
            border-radius: 6px;
            display: inline-block;
            min-width: 28px;
        }

        .lupa {
            font-size: 22px;
            color: #1a237e;
            cursor: pointer;
            transition: color 0.3s ease;
        }

        .lupa:hover {
            color: #f57c00;
        }

        .refresh-btn {
            font-size: 20px;
            color: white;
            cursor: pointer;
            background-color: #1a237e;
            border: none;
            border-radius: 6px;
            padding: 6px 10px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }

        .refresh-btn:hover {
            background-color: #1976d2;
        }
    </style>
</head>
<body>
    <div class="header">
        <img src="/static/headerLatinia.png" alt="LATINIA System Manager QA" class="banner">
        <div class="banner-text">
            Welcome {{ nombre }}
            <button class="refresh-btn" onclick="location.reload()">🔄</button>
            <div class="avatar-menu-container">
                <img src="https://preview.redd.it/msn-avatars-of-all-colors-v0-h70w8hxd5uha1.png?width=640&crop=smart&auto=webp&s=746b504acc441e9828a6fca05bcd9ad59ac7d210"
                     alt="avatar" class="avatar-icon" id="avatarBtn">
                <div id="avatarDropdown" class="dropdown-content">
                    <a href="#" id="logoutBtn">LogOut</a>
                </div>
            </div>
        </div>
    </div>

    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Status</th>
                <th>Used by</th>
                <th>PowerON</th>
                <th>PowerOFF</th>
                <th>OperGroup</th>
                <th>Notes</th>
                <th>Snapshot</th>
            </tr>
        </thead>
        <tbody>
            {{ tabla|safe }}
        </tbody>
    </table>

    <script>
    document.addEventListener("DOMContentLoaded", () => {
        const lupas = document.querySelectorAll(".lupa");
        console.log("🔍 Se encontraron", lupas.length, "iconos lupa");

        lupas.forEach(el => {
            el.addEventListener("click", async function () {
                const instanceId = this.getAttribute("data-instance");
                console.log("📦 Instance ID:", instanceId);

                if (!instanceId) {
                    alert("⚠️ ID de instancia no disponible.");
                    return;
                }

                Swal.fire({
                    title: 'Loading Snapshots...',
                    text: 'Please wait while we fetch the snapshot data.',
                    allowOutsideClick: false,
                    didOpen: () => {
                        Swal.showLoading();
                    }
                });

                try {
                    const res = await fetch(`/snapshots/${instanceId}`);
                    const data = await res.json();
                    console.log("📥 Snapshots recibidos:", data);

                    Swal.close();

                    let mensaje = "";
                    if (Array.isArray(data) && data.length === 0) {
                        mensaje = "No snapshots available.";
                    } else if (Array.isArray(data)) {
                        data.forEach((snap, i) => {
                            mensaje += `<strong>#${i + 1}: ${snap.name || "Unnamed"}</strong><br>${snap.description || "No description"}<br><br>`;
                        });
                    } else {
                        mensaje = `<em>Error:</em> ${data.error || "Unexpected response."}`;
                    }

                    Swal.fire({
                        title: '📸 Snapshots',
                        html: mensaje,
                        icon: 'info',
                        confirmButtonText: 'Close',
                        customClass: {
                            popup: 'swal2-custom-popup'
                        }
                    });
                } catch (err) {
                    console.error("❌ Error al obtener snapshots:", err);
                    Swal.close();
                    Swal.fire("Error", "Failed to retrieve snapshot data.", "error");
                }
            });
        });

        const avatarBtn = document.getElementById("avatarBtn");
        const dropdown = document.getElementById("avatarDropdown");
        const logoutBtn = document.getElementById("logoutBtn");

        avatarBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
        });

        document.addEventListener("click", () => {
            dropdown.style.display = "none";
        });

        logoutBtn.addEventListener("click", (e) => {
            e.preventDefault();
            window.location.href = "/logout";
        });
    });
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
