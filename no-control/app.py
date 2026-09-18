from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, emit
import qrcode
import io
import socket

app = Flask(__name__)

app.config["SECRET_KEY"] = "science-arcade"

socketio = SocketIO(
    app,
    cors_allowed_origins="*"
)


def get_local_ip():
    """
    Descobre o IP do computador na rede local.
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]

    except OSError:
        ip = "127.0.0.1"

    finally:
        s.close()

    return ip


# =========================
# PÁGINAS
# =========================

@app.route("/")
def index():

    ip = get_local_ip()

    return render_template(
        "index.html",
        local_ip=ip
    )


@app.route("/login")
def login():

    return render_template("login.html")


@app.route("/controller")
def controller():

    return render_template("controller.html")


# =========================
# QR CODE
# =========================

@app.route("/qr")
def qr():

    ip = get_local_ip()

    # Página que o celular vai abrir
    url = f"http://{ip}:5000/login"

    img = qrcode.make(url)

    buffer = io.BytesIO()

    img.save(buffer, format="PNG")

    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/png"
    )


# =========================
# SOCKET.IO
# =========================

@socketio.on("connect")
def handle_connect():

    print("📱 Dispositivo conectado!")


@socketio.on("disconnect")
def handle_disconnect():

    print("📱 Dispositivo desconectado!")


@socketio.on("player_login")
def handle_player_login(data):

    print()
    print("👤 NOVO JOGADOR")
    print("----------------")
    print("Nome:", data.get("name"))
    print("ID:", data.get("id"))
    print()

    emit(
        "login_success",
        data
    )


@socketio.on("controller_input")
def handle_controller_input(data):

    print()
    print("🎮 COMANDO RECEBIDO")
    print("-------------------")
    print("Jogador:", data.get("playerName"))
    print("Comando:", data.get("command"))
    print()


# =========================
# INICIAR SERVIDOR
# =========================

if __name__ == "__main__":

    ip = get_local_ip()

    print()
    print("=" * 40)
    print("        SCIENCE ARCADE")
    print("=" * 40)

    print()
    print("🖥️ Computador:")
    print("http://127.0.0.1:5000")

    print()
    print("📱 Celular:")
    print(f"http://{ip}:5000/login")

    print()
    print("📷 QR Code disponível na página inicial")

    print("=" * 40)
    print()

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )