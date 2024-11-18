from opcua import Server
from datetime import datetime
import time
from opcua import ua

# Creazione del server OPC UA
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

# Imposta un namespace URI per evitare conflitti di nomi
uri = "http://example.org/industria_chimica"
idx = server.register_namespace(uri)

# Aggiungi un oggetto che simula il contesto industriale
industrial_context = server.nodes.objects.add_object(idx, "ContestoIndustriale")

# Creazione dell'oggetto "Server Unico"
server_unico = industrial_context.add_object(idx, "ServerUnico")

# Creazione dei "Reattori di Sintesi"
reattoreA = server_unico.add_object(idx, "ReattoreA")
reattoreB = server_unico.add_object(idx, "ReattoreB")
reattoreC = server_unico.add_object(idx, "ReattoreC")
reattoreD = server_unico.add_object(idx, "ReattoreD")

# Funzione per creare e aggiungere variabili ai reattori, con nome basato sul parent
def aggiungi_variabili_reattore(parent_name, reattore, temperatura, pressione, livello):
    temperatura_var = reattore.add_variable(idx, f"{parent_name}_Temperatura", round(temperatura, 1), datatype=ua.NodeId(ua.ObjectIds.Double))
    temperatura_var.set_writable()
    print(f"Creato nodo: {parent_name}_Temperatura -> {temperatura_var.nodeid}")

    pressione_var = reattore.add_variable(idx, f"{parent_name}_Pressione", round(pressione, 1), datatype=ua.NodeId(ua.ObjectIds.Double))
    pressione_var.set_writable()
    print(f"Creato nodo: {parent_name}_Pressione -> {pressione_var.nodeid}")

    livello_var = reattore.add_variable(idx, f"{parent_name}_Livello", round(livello, 1), datatype=ua.NodeId(ua.ObjectIds.Double))
    livello_var.set_writable()
    print(f"Creato nodo: {parent_name}_Livello -> {livello_var.nodeid}")

    valvola_mandata_var = reattore.add_variable(idx, f"{parent_name}_ValvolaMandata", 0, datatype=ua.NodeId(ua.ObjectIds.Int32))
    valvola_mandata_var.set_writable()
    print(f"Creato nodo: {parent_name}_ValvolaMandata -> {valvola_mandata_var.nodeid}")

    valvola_scarico_var = reattore.add_variable(idx, f"{parent_name}_ValvolaScarico", 0, datatype=ua.NodeId(ua.ObjectIds.Int32))
    valvola_scarico_var.set_writable()
    print(f"Creato nodo: {parent_name}_ValvolaScarico -> {valvola_scarico_var.nodeid}")

    camicia_riscaldamento_var = reattore.add_variable(idx, f"{parent_name}_CamiciaRiscaldamento", 0, datatype=ua.NodeId(ua.ObjectIds.Int32))
    camicia_riscaldamento_var.set_writable()
    print(f"Creato nodo: {parent_name}_CamiciaRiscaldamento -> {camicia_riscaldamento_var.nodeid}")

    agitatore_status_var = reattore.add_variable(idx, f"{parent_name}_AgitatorStatus", False, datatype=ua.NodeId(ua.ObjectIds.Boolean))
    agitatore_status_var.set_writable()
    print(f"Creato nodo: {parent_name}_AgitatorStatus -> {agitatore_status_var.nodeid}")

    agitatore_speed_var = reattore.add_variable(idx, f"{parent_name}_AgitatorSpeed", 0, datatype=ua.NodeId(ua.ObjectIds.Int32))
    agitatore_speed_var.set_writable()
    print(f"Creato nodo: {parent_name}_AgitatorSpeed -> {agitatore_speed_var.nodeid}")

    modalita_operativa_var = reattore.add_variable(idx, f"{parent_name}_ModalitaOperativa", True, datatype=ua.NodeId(ua.ObjectIds.Boolean))
    modalita_operativa_var.set_writable()
    print(f"Creato nodo: {parent_name}_ModalitaOperativa -> {modalita_operativa_var.nodeid}")

    return temperatura_var, pressione_var, livello_var, valvola_mandata_var, valvola_scarico_var, camicia_riscaldamento_var, agitatore_status_var, agitatore_speed_var, modalita_operativa_var

# Aggiungi variabili ai Reattori
variabili_reattoreA = aggiungi_variabili_reattore("ReattoreA", reattoreA, 25.0, 2.0, 8.0)
variabili_reattoreB = aggiungi_variabili_reattore("ReattoreB", reattoreB, 22.0, 2.5, 9.0)
variabili_reattoreC = aggiungi_variabili_reattore("ReattoreC", reattoreC, 23.0, 1.8, 6.0)
variabili_reattoreD = aggiungi_variabili_reattore("ReattoreD", reattoreD, 27.0, 2.8, 7.0)

# Limiti delle variabili
TEMPERATURA_MIN, TEMPERATURA_MAX = 10.0, 50.0
PRESSIONE_MIN, PRESSIONE_MAX = 0.0, 4.0
LIVELLO_MIN, LIVELLO_MAX = 0.0, 100.0

# Funzione per aggiornare le variabili del reattore
def aggiorna_variabili(reattore_vars):
    temperatura, pressione, livello, valvola_mandata, valvola_scarico, camicia_riscaldamento, agitatore_status, agitatore_speed, modalita_operativa = reattore_vars

    # Aggiorna Temperatura
    camicia_on = camicia_riscaldamento.get_value() == 1
    agitatore_on = agitatore_status.get_value()
    if camicia_on:
        incremento = 1.0 * (1.2 if agitatore_on else 1.0)
        nuova_temperatura = temperatura.get_value() + incremento
    else:
        decremento = 1.0 * (0.8 if not agitatore_on else 1.0)
        nuova_temperatura = temperatura.get_value() - decremento
    nuova_temperatura = round(min(max(nuova_temperatura, TEMPERATURA_MIN), TEMPERATURA_MAX), 1)
    temperatura.set_value(nuova_temperatura)

    # Aggiorna Pressione proporzionalmente alla temperatura
    nuova_pressione = PRESSIONE_MIN + (nuova_temperatura - TEMPERATURA_MIN) / (TEMPERATURA_MAX - TEMPERATURA_MIN) * (PRESSIONE_MAX - PRESSIONE_MIN)
    nuova_pressione = round(nuova_pressione, 1)
    pressione.set_value(nuova_pressione)

    # Aggiorna Livello
    if valvola_scarico.get_value() == 1:
        nuovo_livello = livello.get_value() - (livello.get_value() * 0.05)
    elif valvola_mandata.get_value() == 1:
        nuovo_livello = livello.get_value() + (livello.get_value() * 0.05)
    else:
        nuovo_livello = livello.get_value()
    nuovo_livello = round(min(max(nuovo_livello, LIVELLO_MIN), LIVELLO_MAX), 1)
    livello.set_value(nuovo_livello)

# Definizione della classe per il logging
class LogHandler:
    def datachange_notification(self, node, val, data):
        print(f"[{datetime.now()}] Data Change Notification: Node: {node}, Value: {val}")

# Avvio del server
server.start()

try:
    print(f"Server OPC UA avviato su {server.endpoint}")
    print("Namespace registrati:", server.get_namespace_array())
    
    # Creiamo una sottoscrizione per monitorare i cambiamenti
    handler = LogHandler()
    subscription = server.create_subscription(500, handler)

    # Sottoscriviamo tutte le variabili dei reattori per monitorare cambiamenti di valore
    for variabili in [variabili_reattoreA, variabili_reattoreB, variabili_reattoreC, variabili_reattoreD]:
        for var in variabili:
            subscription.subscribe_data_change(var)

    # Loop principale per aggiornare i valori ogni 5 secondi
    while True:
        for i, reattore_vars in enumerate([variabili_reattoreA, variabili_reattoreB, variabili_reattoreC, variabili_reattoreD]):
            print(f"Aggiornamento variabili Reattore {chr(65+i)}...")
            aggiorna_variabili(reattore_vars)
        time.sleep(5)
except KeyboardInterrupt:
    print("Chiusura del server OPC UA...")
finally:
    server.stop()
    print("Server fermato.")
