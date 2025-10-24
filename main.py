import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    def handleAdd(e):
        #questa funzione per il tasto + ed incrementare i valori
        currentVal = int(numero_passeggeri.value)
        numero_passeggeri.value = currentVal + 1
        numero_passeggeri.update()

    def handleRemove(e):
        #questa funzione per il tasto meno e diminuire il valore del numero di posti
        currentVal = int(numero_passeggeri.value)
        #metto un controllo sul valore del numero di passeggeri che non può essere un un numero negativo
        if currentVal > 0:
            numero_passeggeri.value = currentVal - 1
            numero_passeggeri.update()

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    auto_marca = ft.TextField(value= "Marca")
    auto_modello = ft.TextField(value= "Modello")
    autoAnno = ft.TextField(value= "Anno")
    btnMinus = ft.IconButton (icon = ft.Icons.REMOVE,
                              icon_color="red",
                              icon_size= 16, on_click=handleRemove)
    btnAdd = ft.IconButton (icon = ft.Icons.ADD,
                            icon_color="green",
                            icon_size= 16, on_click=handleAdd)
    numero_passeggeri = ft.TextField(width=100, disabled=True, value = "0", border_color= "green", text_align = ft.TextAlign.CENTER)


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    def aggiungi_automobile(e):
        #qua gestisci le eccezioni
        try:
            """uso una variabile locale "anno" invece di "autoAnno" perché autoAnno è il TextField:
                se lo sovrascrivessi con un numero (int), al prossimo click il programma andrebbe in errore
                dato che non sarebbe più un campo di testo ma un intero. 
                In laboratorio non capivamo perchè scrivendo autoAnno = int(autoAnno.value) non funzionasse"""
            anno = int(autoAnno.value)
            numero_posti = int(numero_passeggeri.value)
            #auto_marca e modello sono due elementi flet quindi di questi devo passare solo il value alla funzione autonoleggio
            autonoleggio.aggiungi_automobile(auto_marca.value, auto_modello.value, anno, numero_posti)
            aggiorna_lista_auto()
            auto_marca.value=""
            auto_modello.value=""
            autoAnno.value=""
            numero_passeggeri.value = "0"


            #aggiorno la pagina (potrei aggiornare anche i singoli elementi presi uno per volta, per visualizzarli "vuoti"
            page.update()

        except Exception:
            alert.show_alert("ERRORE:inserisci valori numeri per anno e posti")



    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    bottone_aggiungi_automobile = ft.ElevatedButton("Aggiungi Automobile", on_click=aggiungi_automobile)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Text("Aggiungi nuova automobile", size = 20),
        ft.Row(spacing=20,
               controls=[auto_marca, auto_modello, autoAnno, btnMinus, numero_passeggeri, btnAdd],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(spacing=20,
               controls=[bottone_aggiungi_automobile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
