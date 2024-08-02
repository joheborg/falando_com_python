import PySimpleGUI as sg
import pyttsx3
from datetime import datetime
import os


def get_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    return voices


def text_to_speech(text, voice_id):
    engine = pyttsx3.init()
    engine.setProperty("voice", voice_id)

    rate = engine.getProperty("rate")
    engine.setProperty("rate", rate - 50)

    engine.setProperty("volume", 1.0)

    engine.say(text)
    engine.runAndWait()


def log_text(text):
    with open("historico.txt", "a", encoding="utf-8") as file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp} - {text}\n")


def load_log():
    if os.path.exists("historico.txt"):
        with open("historico.txt", "r", encoding="utf-8") as file:
            return file.read()
    return ""


def janela_principal(list_voice, historico):
    layout = [
        [sg.Text("Selecione a voz:")],
        [sg.Combo(list_voice, size=(50, 1), key="-VOZ-", default_value=list_voice[0])],
        [sg.Text("Cole ou digite o texto abaixo:")],
        [sg.Multiline(size=(50, 10), key="-TEXTO-", focus=True, enable_events=True)],
        [sg.Text("Histórico:")],
        [
            sg.Multiline(
                size=(50, 10), key="-HISTORICO-", disabled=True, default_text=historico
            )
        ],
        [sg.Button("Converter em Fala"), sg.Button("Sair")],
    ]

    return sg.Window(
        "Conversor de Texto para Fala", layout, return_keyboard_events=True
    )


voices = get_voices()
voice_names = [voice.name for voice in voices]
historico = load_log()

janela = janela_principal(voice_names, historico)

while True:
    event, values = janela.read()
    if event == sg.WINDOW_CLOSED or event == "Sair":
        break
    elif event == "Converter em Fala":
        text = values["-TEXTO-"].strip()
        selected_voice_name = values["-VOZ-"]
        selected_voice_id = None

        for voice in voices:
            if voice.name == selected_voice_name:
                selected_voice_id = voice.id
                break

        if text and selected_voice_id:
            text_to_speech(text, selected_voice_id)
            log_text(text)
            historico += f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - {text}\n'
            janela["-HISTORICO-"].update(historico)
            janela["-TEXTO-"].update("")

janela.close()
