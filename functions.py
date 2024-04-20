import pyautogui
from pynput import mouse, keyboard
import pyperclip
import time
import dotenv
import os
import sqlalchemy as sa
import urllib
import pandas as pd

dotenv.load_dotenv()

mouse_controller = mouse.Controller()
mouse_button = mouse.Button

keyboard_controller = keyboard.Controller()
keyboard_key = keyboard.Key

def openWppDektop():
    keyboard_controller.press(keyboard_key.cmd)
    keyboard_controller.press('1')
    keyboard_controller.release('1')
    keyboard_controller.release(keyboard_key.cmd)
    time.sleep(1)

class contatoWpp():
    def __init__(self, dadosContato):
        self.nome = dadosContato.NOME
        self.telefone = dadosContato.TELEFONE
        self.tipo_envio = dadosContato.ID_TIPO_ENVIO
        self.descricao_tipo_envio = dadosContato.DESCRICAO_TIPO_ENVIO
        self.caminho_arquivo = dadosContato.CAMINHO_ARQUIVO
        self.mensagem = dadosContato.DESCRICAO_MENSAGEM
        self.flag_img = True if dadosContato.ID_TIPO_ENVIO == 3 and dadosContato.CAMINHO_ARQUIVO else False

        self.eventClickSearch()

    def eventClickSearch(self):
        # botao_pesquisa_desktop = pyautogui.locateCenterOnScreen('botao_pesquisa_desktop.png')
        # pyautogui.click(botao_pesquisa_desktop[0], botao_pesquisa_desktop[1], interval=1)

        keyboard_controller.press(keyboard_key.ctrl)
        keyboard_controller.press('f')
        keyboard_controller.release('f')
        keyboard_controller.release(keyboard_key.ctrl)

        self.cleanSearh()

    def cleanSearh(self):
        keyboard_controller.press(keyboard_key.ctrl)
        keyboard_controller.press('a')
        keyboard_controller.release('a')
        keyboard_controller.release(keyboard_key.ctrl)

        keyboard_controller.press(keyboard_key.delete)
        keyboard_controller.release(keyboard_key.delete)

    def eventSelectUser(self):
        pyperclip.copy(self.telefone)

        keyboard_controller.press(keyboard_key.ctrl)
        keyboard_controller.press('v')
        keyboard_controller.release('v')
        keyboard_controller.release(keyboard_key.ctrl)

        time.sleep(2)

        keyboard_controller.press(keyboard_key.down)
        keyboard_controller.press(keyboard_key.enter)
        keyboard_controller.release(keyboard_key.down)
        keyboard_controller.release(keyboard_key.enter)

        time.sleep(2)

    def eventClickFile(self):
        botao_arquivo_desktop = pyautogui.locateCenterOnScreen('./img/botao_arquivo_desktop.png')
        pyautogui.click(botao_arquivo_desktop[0], botao_arquivo_desktop[1], interval=1)

        if self.flag_img:
            botao_imagem_desktop = pyautogui.locateCenterOnScreen('./img/botao_imagem_desktop.png')
            pyautogui.click(botao_imagem_desktop[0], botao_imagem_desktop[1], interval=1)
            mouse_controller.click(button=mouse_button.left)
            time.sleep(1)
        else:
            botao_imagem_desktop = pyautogui.locateCenterOnScreen('./img/botao_documento_desktop.png')
            pyautogui.click(botao_imagem_desktop[0], botao_imagem_desktop[1], interval=1)
            mouse_controller.click(button=mouse_button.left)
            time.sleep(1)

    def eventSendMsg(self):
        botao_mensagem_desktop = pyautogui.locateCenterOnScreen('./img/botao_arquivo_desktop.png')
        calc = (botao_mensagem_desktop[0]*20)/100
        pyautogui.click((botao_mensagem_desktop[0]+calc), botao_mensagem_desktop[1], interval=1)

        pyperclip.copy(self.mensagem)

        keyboard_controller.press(keyboard_key.ctrl)
        keyboard_controller.press('v')
        keyboard_controller.release('v')
        keyboard_controller.release(keyboard_key.ctrl)

        time.sleep(0.5)

        keyboard_controller.press(keyboard_key.enter)
        keyboard_controller.release(keyboard_key.enter)

        time.sleep(0.5)

    def eventSendFile(self):
        caminho_arquivo = self.caminho_arquivo
        pyperclip.copy(caminho_arquivo)

        keyboard_controller.press(keyboard_key.ctrl)
        keyboard_controller.press('v')
        keyboard_controller.release('v')
        keyboard_controller.release(keyboard_key.ctrl)

        time.sleep(0.5)

        keyboard_controller.press(keyboard_key.enter)
        keyboard_controller.release(keyboard_key.enter)

        time.sleep(0.5)

        pyperclip.copy(self.mensagem if self.mensagem is not None else '')
        
        time.sleep(0.5)

        keyboard_controller.press(keyboard_key.ctrl)
        keyboard_controller.press('v')
        keyboard_controller.release('v')
        keyboard_controller.release(keyboard_key.ctrl)

        time.sleep(0.5)

        keyboard_controller.press(keyboard_key.enter)
        keyboard_controller.release(keyboard_key.enter)

        time.sleep(1)

class dataBase():
    def __init__(self):
        self.serverName = os.getenv('serverName')
        self.dataBase = os.getenv('dataBase')
        self.userName = os.getenv('userName')
        self.password = os.getenv('password')
        self.drive = os.getenv('driveConnection')
    
    def connectDataBase(self):
        ps = urllib.parse.quote(self.password)

        connection_string = (
            f'Driver=' + self.drive + ';'
            f'Server=' + self.serverName + ';'
            f"Database=" + self.dataBase + ';'
            f'UID=' + self.userName + ';'
            f'PWD=' + ps + ';'
            f"Trusted_Connection=no;"
        )

        connection_url = sa.engine.URL.create(
            "mssql+pyodbc", 
            query={"odbc_connect": connection_string}
        )

        try:
            return sa.create_engine(connection_url,fast_executemany=True)
        except Exception as ex:
            return False, ex
        
    def select(self, query=str):
        return pd.DataFrame(pd.read_sql(sql= query, con= self.connectDataBase()))