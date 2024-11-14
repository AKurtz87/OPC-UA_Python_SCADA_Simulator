from flask import Flask, render_template, request, redirect, url_for
from opcua import Client
import logging
import time
import threading

# Configurazione del logging per facilitare il debug
logging.basicConfig(level=logging.INFO)

app = Flask(__name__, static_folder='static')

# Connessione al server OPC UA
client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.connect()

# Identificatori dei nodi OPC UA (mappati manualmente dai dati del server)
node_ids = {
    "ReattoreA": {
        "Temperatura": "ns=2;i=7",
        "Livello": "ns=2;i=9",
        "ValvolaMandata": "ns=2;i=10",
        "ValvolaScarico": "ns=2;i=11",
        "CamiciaRiscaldamento": "ns=2;i=12",
        "AgitatorStatus": "ns=2;i=13",
        "AgitatorSpeed": "ns=2;i=14",
    },
    "ReattoreB": {
        "Temperatura": "ns=2;i=15",
        "Livello": "ns=2;i=17",
        "ValvolaMandata": "ns=2;i=18",
        "ValvolaScarico": "ns=2;i=19",
        "CamiciaRiscaldamento": "ns=2;i=20",
        "AgitatorStatus": "ns=2;i=21",
        "AgitatorSpeed": "ns=2;i=22",
    },
    "ReattoreC": {
        "Temperatura": "ns=2;i=23",
        "Livello": "ns=2;i=25",
        "ValvolaMandata": "ns=2;i=26",
        "ValvolaScarico": "ns=2;i=27",
        "CamiciaRiscaldamento": "ns=2;i=28",
        "AgitatorStatus": "ns=2;i=29",
        "AgitatorSpeed": "ns=2;i=30",
    },
    "ReattoreD": {
        "Temperatura": "ns=2;i=31",
        "Livello": "ns=2;i=33",
        "ValvolaMandata": "ns=2;i=34",
        "ValvolaScarico": "ns=2;i=35",
        "CamiciaRiscaldamento": "ns=2;i=36",
        "AgitatorStatus": "ns=2;i=37",
        "AgitatorSpeed": "ns=2;i=38",
    },
}

@app.route('/')
def index():
    try:
        # Recupera i valori di ciascun reattore
        variabili_reattori = {}
        for reattore, variabili in node_ids.items():
            variabili_reattori[reattore] = {
                nome: client.get_node(nodo).get_value()
                for nome, nodo in variabili.items()
            }

        # Passa i dati al template HTML
        return render_template('dashboard.html', variabili_reattori=variabili_reattori)

    except Exception as e:
        logging.error(f"Errore durante l'accesso al server OPC UA: {e}")
        return "Si è verificato un errore durante la connessione al server OPC UA.", 500

@app.route('/<azione>_<reattore>', methods=['POST'])
def gestisci_variabile(azione, reattore):
    try:
        nodo_id = node_ids[reattore][azione]
        nodo = client.get_node(nodo_id)
        nuovo_valore = request.form['valore']

        if azione in ['ValvolaMandata', 'ValvolaScarico', 'CamiciaRiscaldamento']:
            nuovo_valore = int(nuovo_valore)
        elif azione == 'AgitatorStatus':
            nuovo_valore = nuovo_valore.lower() == 'true'
        elif azione == 'AgitatorSpeed':
            nuovo_valore = int(nuovo_valore)
        else:
            raise ValueError(f"Azione '{azione}' non valida.")

        nodo.set_value(nuovo_valore)
        logging.info(f"Variabile {azione} del {reattore} impostata a {nuovo_valore}.")

        return redirect(url_for('index'))

    except Exception as e:
        logging.error(f"Errore durante l'aggiornamento della variabile {azione} per {reattore}: {e}")
        return "Si è verificato un errore durante l'aggiornamento dei valori", 500

def automazione_indipendente():
    try:
        for reattore in node_ids.keys():
            threading.Thread(target=ciclo_reattore, args=(reattore,), daemon=True).start()
            logging.info(f"Thread avviato per il reattore {reattore}.")
    except Exception as e:
        logging.error(f"Errore nell'avvio dell'automazione: {e}")

def ciclo_reattore(reattore):
    try:
        logging.info(f"Avvio del ciclo per il reattore {reattore}.")
        while True:
            # Nodi OPC UA
            valvola_mandata = client.get_node(node_ids[reattore]["ValvolaMandata"])
            valvola_scarico = client.get_node(node_ids[reattore]["ValvolaScarico"])
            camicia_riscaldamento = client.get_node(node_ids[reattore]["CamiciaRiscaldamento"])
            agitatore_status = client.get_node(node_ids[reattore]["AgitatorStatus"])
            agitatore_speed = client.get_node(node_ids[reattore]["AgitatorSpeed"])
            livello = client.get_node(node_ids[reattore]["Livello"])
            temperatura = client.get_node(node_ids[reattore]["Temperatura"])

            # Step 1: Resetta
            valvola_mandata.set_value(0)
            valvola_scarico.set_value(0)
            camicia_riscaldamento.set_value(0)
            agitatore_speed.set_value(0)
            agitatore_status.set_value(False)

            # Step 2: Inizia il riempimento
            agitatore_speed.set_value(60)
            agitatore_status.set_value(True)
            valvola_mandata.set_value(1)
            while livello.get_value() < 90.0:
                time.sleep(1)
            valvola_mandata.set_value(0)

            # Step 3: Riscalda
            camicia_riscaldamento.set_value(1)
            while temperatura.get_value() < 40.0:
                time.sleep(1)
            camicia_riscaldamento.set_value(0)
            

            # Step 4: Scarico
            while temperatura.get_value() > 20.0:
                time.sleep(1)
            agitatore_speed.set_value(30)
            valvola_scarico.set_value(1)
            while livello.get_value() > 5.0:
                time.sleep(1)
            valvola_scarico.set_value(0)
            agitatore_status.set_value(False)
            agitatore_speed.set_value(0)
            time.sleep(10)

    except Exception as e:
        logging.error(f"Errore nel ciclo del reattore {reattore}: {e}")

threading.Thread(target=automazione_indipendente, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)
