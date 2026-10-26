import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO
    input_tipo = ft.TextField(label="Tipo")
    input_marca = ft.TextField(label="Marca")
    input_anno = ft.TextField(label="Anno")
    input_valore = ft.TextField(
    label="Valore (€)",
    value="0",
    width=130,
    text_align=ft.TextAlign.CENTER,
    read_only=True
)


    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO
    def aumenta_valore(e):
        try:
            valore_corrente = int(input_valore.value)
            input_valore.value = str(valore_corrente + 1)
            page.update()
        except ValueError:
            alert.show_alert("❌ Il valore deve essere un numero intero.")
    def diminuisci_valore(e):
        try:
            valore_corrente = int(input_valore.value)
            if valore_corrente > 0:
                input_valore.value = str(valore_corrente - 1)
                page.update()
        except ValueError:
            alert.show_alert("❌ Il valore deve essere un numero intero.")
    def aggiungi_strumento(e):
        tipo = input_tipo.value.strip()
        marca = input_marca.value.strip()
        anno = input_anno.value.strip()

        if not tipo or not marca or not anno:
            alert.show_alert("❌ Tutti i campi devono essere compilati.")
            return

        try:
            anno_int = int(anno)
        except ValueError:
            alert.show_alert("❌ L'anno deve essere un numero intero.")
            return

        try:
            valore = int(input_valore.value)
        except ValueError:
            alert.show_alert("❌ Il valore deve essere un numero intero.")
            return

        deposito.aggiungi_strumento(tipo, marca, anno_int, valore)
        aggiorna_lista_strumenti()

        # Reset dei campi di input
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        input_valore.value = "0"
        page.update()
    

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO
    pulsante_aumenta_valore = ft.Button("➕", on_click=aumenta_valore)
    pulsante_diminuisci_valore = ft.Button("➖", on_click=diminuisci_valore)
    pulsante_aggiungi_strumento = ft.Button("Aggiungi Strumento", on_click=aggiungi_strumento)

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
        # TODO
        ft.Divider(),
        ft.Text("Aggiungi Nuovo Strumento", size=20),
        ft.Row(spacing=20,
               controls=[input_tipo, input_marca, input_anno, ft.Column(controls=[pulsante_aumenta_valore, input_valore, pulsante_diminuisci_valore],alignment=ft.MainAxisAlignment.CENTER)],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(spacing=20,
               controls=[pulsante_aggiungi_strumento],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
