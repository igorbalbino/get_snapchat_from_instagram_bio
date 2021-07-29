'''
Titulo: Criar BOT Inscritos Instagram
Autor: Igor do Espírito Santo
Linguagem: Python
'''

#IMPORTA DEPENDENCIAS NECESSARIAS

import os
import time
import random
import PySimpleGUI as sg
import logging
import instaloader
import shutil
import threading

class Util:
    #pega o log do argumento passado
    def getLog(self, e):
        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)
        #temos também:
        #logging.INFO
        handler = logging.FileHandler('getSnapchat.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info(e)
    #getLog

    def delay(self):
        time.sleep(random.randint(2, 5))
    
    def deleteDir(self, path):
        sg.Print('Conteudo de', path, f'deletado!{os.linesep}')
        try:
            shutil.rmtree(path)
        except Exception as e:
            sg.popup_ok(f'DELETE DIR ERROR!   ', e)
    #deleteDir

    def createDir(self, path, permission):
        sg.popup_ok('Diretorio ', path, f' criado!{os.linesep}')
        try:
            os.mkdir(path, mode=permission)
        except Exception as e:
            sg.popup_error(f'CREATE DIR ERROR!   ', e)
    #createDir

#CRIA CLASSE QUE CONTEM A LOGICA DO SISTEMA.
class InstagramBot:
    #CRIA FUNCAO CONSTRUTOR
    def __init__(self, username, password, target_user):
        self.util = Util()

        self.username           = username
        self.password           = password
        self.target_user        = target_user

    #FECHA __init__
    
    def initGetSnapchat(self):
        try:
            if ',' in self.target_user:
                aux_target_user = self.target_user.split(',')
                for target in aux_target_user:
                    followers_arr = self.getFollowers(target)
                    for follower in followers_arr:
                        self.util.delay()
                        #Created the Threads
                        t1 = threading.Thread(target=self.getFollowers, args=(follower,))
                        #Started the threads
                        t1.start()
                        #Joined the threads
                        t1.join()
                        #self.getFollowers(follower)
            else:
                self.util.delay()
                #Created the Threads
                t1 = threading.Thread(target=self.getFollowers, args=(self.target_user,))
                #Started the threads
                t1.start()
                #Joined the threads
                t1.join()
                #self.getFollowers(self.target_user)
            print('Finished!')
        except  Exception as e:
                self.util.getLog(e)
    #initGetSnapchat
                
            
    
    def getFollowers(self, target):
        try:
            L = instaloader.Instaloader()
            
            L.login(self.username, self.password)
            self.util.delay()
            
            profile = instaloader.Profile.from_username(L.context, target)
            
            fall                = []
            selected_followers  = []
            followers_bio_arr   = []
            
            fall = profile.get_followers()
            
            for f in fall:
                if 'SC' or 'Snapchat' or 'snapchat' or 'Snap Chat' or 'snap chat' or 'sc' in f.biography:
                    selected_followers.append(f)
                    followers_bio_arr.append(f.biography)
            
            self.saveSnapchat(followers_bio_arr)
        except  Exception as e:
                self.util.getLog(e)
    #getFollowers
    
    def saveSnapchat(self, arr):
        try:
            self.util.delay()
            
            toSaveInfoDir = '.\snapchats.txt'
            for item in arr:
                f = open(toSaveInfoDir, "w")
                f.writelines(item)
                f.close()
        except  Exception as e:
                self.util.getLog(e)
    #getSnapchat
    
class TelaPython:
    #CRIA FUNCAO CONSTRUTOR
    def __init__(self):
        #LAYOUT
        layout = [
            #CRIA ELEMENTO NA TELA COM UM INPUT PARA RECEBER DADOS
            [sg.Text('')],
            [sg.Text('Username', size=(10, 0)), sg.Input(size=(30, 0), key='username', default_text='igor927482')],
            [sg.Text('Password', size=(10, 0)), sg.Input(size=(30, 0), key='password', password_char='*', default_text='#12131212aA!@')],
            [sg.Text('')],
            [sg.Text('Target User', size=(25, 0)), sg.Input(size=(30, 0), key='target_user', default_text='godsledpotato')],
            [sg.Text('')],
            [sg.Button('Submit',size=(30, 0))]
        ]
        #JANELA
        #CRIA A TELA E COLOCA OS ELEMENTOS DE LAYOUT NELA
        self.janela = sg.Window('Get Snapchat from bio - Instagram').layout(layout)
    #FECHA __init__

    def Iniciar(self):
        while True:
            # EXTRAIR DADOS DA TELA
            self.button, self.values = self.janela.Read()
            username = self.values['username']
            password = self.values['password']
            target_user = self.values['target_user']

            logBot = InstagramBot(username, password, target_user)
            logBot.initGetSnapchat()
        #FECHA while
    # FECHA Iniciar
#TelaPython

#INSTANCIA CLASSE TelaPython EM tela
tela = TelaPython()
tela.Iniciar()