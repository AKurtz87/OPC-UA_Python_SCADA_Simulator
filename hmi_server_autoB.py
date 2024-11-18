from flask import Flask, render_template, request, redirect, url_for, jsonify
from opcua import Client
import logging
import time
import threading
from threading import Event, Lock

# Configurazione del logging per facilitare il debug
logging.basicConfig(level=logging.WARNING)

app = Flask(__name__, static_folder='static')

# Connessione al server OPC UA
client = Client("opc.tcp://localhost:4840/freeopcua/server/")
client.connect()


# Identificatori dei nodi OPC UA (mappati manualmente dai dati del server)
node_ids = {
    "ReattoreA": {
        "Temperatura": "ns=2;i=7",
        "Pressione": "ns=2;i=8",
        "Livello": "ns=2;i=9",
        "ValvolaMandata": "ns=2;i=10",
        "ValvolaScarico": "ns=2;i=11",
        "CamiciaRiscaldamento": "ns=2;i=12",
        "AgitatorStatus": "ns=2;i=13",
        "AgitatorSpeed": "ns=2;i=14",
        "ModalitaOperativa": "ns=2;i=15",
    },
    "ReattoreB": {
        "Temperatura": "ns=2;i=16",
        "Pressione": "ns=2;i=17",
        "Livello": "ns=2;i=18",
        "ValvolaMandata": "ns=2;i=19",
        "ValvolaScarico": "ns=2;i=20",
        "CamiciaRiscaldamento": "ns=2;i=21",
        "AgitatorStatus": "ns=2;i=22",
        "AgitatorSpeed": "ns=2;i=23",
        "ModalitaOperativa": "ns=2;i=24",
    },
    "ReattoreC": {
        "Temperatura": "ns=2;i=25",
        "Pressione": "ns=2;i=26",
        "Livello": "ns=2;i=27",
        "ValvolaMandata": "ns=2;i=28",
        "ValvolaScarico": "ns=2;i=29",
        "CamiciaRiscaldamento": "ns=2;i=30",
        "AgitatorStatus": "ns=2;i=31",
        "AgitatorSpeed": "ns=2;i=32",
        "ModalitaOperativa": "ns=2;i=33",
    },
    "ReattoreD": {
        "Temperatura": "ns=2;i=34",
        "Pressione": "ns=2;i=35",
        "Livello": "ns=2;i=36",
        "ValvolaMandata": "ns=2;i=37",
        "ValvolaScarico": "ns=2;i=38",
        "CamiciaRiscaldamento": "ns=2;i=39",
        "AgitatorStatus": "ns=2;i=40",
        "AgitatorSpeed": "ns=2;i=41",
        "ModalitaOperativa": "ns=2;i=42",
    },
}

# Stato operativo per ogni reattore (True = Automatico, False = Manuale)
stati_reattori = {
    "ReattoreA": True,
    "ReattoreB": True,
    "ReattoreC": True,
    "ReattoreD": True,
}

# Flag di terminazione per i thread
stop_flags = {
    "ReattoreA": Event(),
    "ReattoreB": Event(),
    "ReattoreC": Event(),
    "ReattoreD": Event(),
}

# Lock per sincronizzare automazione e operazioni manuali
locks = {
    "ReattoreA": Lock(),
    "ReattoreB": Lock(),
    "ReattoreC": Lock(),
    "ReattoreD": Lock(),
}

# E' sufficiente fare solo il rendering dell'html in quanto in contenuti si aggiornano manualmente
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
        print(variabili_reattori)
        return render_template('dashboard.html', variabili_reattori=variabili_reattori)

    except Exception as e:
        logging.error(f"Errore durante l'accesso al server OPC UA: {e}")
        return "Si è verificato un errore durante la connessione al server OPC UA.", 500


@app.route('/api/reattori', methods=['GET'])
def api_reattori():
    try:
        variabili_reattori = {}
        for reattore, variabili in node_ids.items():
            variabili_reattori[reattore] = {
                nome: client.get_node(nodo).get_value()
                for nome, nodo in variabili.items()
            }
            # Aggiungi lo stato operativo (automatico/manuale)
            variabili_reattori[reattore]['ModalitaOperativa'] = stati_reattori[reattore]
        return jsonify(variabili_reattori)
    except Exception as e:
        logging.error(f"Errore durante il recupero dei dati dei reattori: {e}")
        return jsonify({"error": "Errore nel recupero dei dati"}), 500


@app.route('/<azione>_<reattore>', methods=['POST'])
def gestisci_variabile(azione, reattore):
    print(azione)
    print(reattore)
    try:
        with locks[reattore]:  # Blocca l'accesso durante l'operazione manuale
            nodo_id = node_ids[reattore][azione]
            nodo = client.get_node(nodo_id)
            nuovo_valore = request.form['valore']  # Riceve il valore dal form

            # Conversione del valore in base all'azione
            if azione in ['ValvolaMandata', 'ValvolaScarico', 'CamiciaRiscaldamento']:
                nuovo_valore = int(nuovo_valore)
            elif azione == 'AgitatorStatus':
                nuovo_valore = nuovo_valore.lower() == 'true'
            elif azione == 'AgitatorSpeed':
                nuovo_valore = int(nuovo_valore)
            else:
                raise ValueError(f"Azione '{azione}' non valida.")

            # Imposta il valore nel nodo OPC UA
            nodo.set_value(nuovo_valore)
            logging.info(f"Variabile {azione} del {reattore} impostata a {nuovo_valore}.")

        # Dopo l'operazione, rimanda alla dashboard
        return redirect(url_for('index'))
        

    except Exception as e:
        logging.error(f"Errore durante l'aggiornamento della variabile {azione} per {reattore}: {e}")
        return "Si è verificato un errore durante l'aggiornamento dei valori", 500



@app.route('/CambiaModalita/<reattore>', methods=['POST'])
def cambia_modalita(reattore):
    try:
        modalita = request.form['modalita']  # 'automatico' o 'manuale'
        if reattore not in stati_reattori:
            return jsonify({"error": "Reattore non valido"}), 400

        if modalita.lower() == 'automatico':
            stati_reattori[reattore] = True
            stop_flags[reattore].clear()  # Riabilita il ciclo automatico
            threading.Thread(target=ciclo_reattore, args=(reattore,), daemon=True).start()
            nodo_id = node_ids[reattore]["ModalitaOperativa"]
            nodo = client.get_node(nodo_id)
            nodo.set_value(True)
            logging.info(f"Modalità del {reattore} impostata a automatico.")
        elif modalita.lower() == 'manuale':
            stati_reattori[reattore] = False
            stop_flags[reattore].set()  # Termina il thread automatico
            nodo_id = node_ids[reattore]["ModalitaOperativa"]
            nodo = client.get_node(nodo_id)
            nodo.set_value(False)
            logging.info(f"Modalità del {reattore} impostata a manuale.")
        else:
            return redirect(url_for('index'))

        # Restituisci una risposta JSON per aggiornare il frontend
        return redirect(url_for('index'))

    except Exception as e:
        logging.error(f"Errore durante il cambio di modalità per {reattore}: {e}")
        return jsonify({"error": "Errore nel cambio di modalità"}), 500



def ciclo_reattore(reattore):
    """
    Simula il ciclo di operazioni per un singolo reattore.
    """
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


# Avvia automazione indipendente
threading.Thread(target=lambda: [threading.Thread(target=ciclo_reattore, args=(r,), daemon=True).start() for r in node_ids.keys()], daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True)

