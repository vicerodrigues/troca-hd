from tkinter import *
from tkinter import ttk
import logging

class FrameLog(ttk.Frame, logging.Handler):
    """Esta classe cria o frame onde é mostrado o TextBox de log do programa.
        O loglevel está setado para info inicialmente.
    """

    def __init__(self, parent):

        ttk.Frame.__init__(self, parent)

        # Cria o frame desta parte do programa
        self.iniciaLog = ttk.Frame(self, padding=(5, 5, 5, 5), relief=RIDGE, borderwidth=2)
        self.iniciaLog.grid(row=0, column=0, sticky=(N, S, E, W), padx=2, pady=2)

        # Cria a label e o tkinter.Text
        self.lbl = ttk.Label(self.iniciaLog, text='LOG:', font='TkCaptionFont')
        self.lbl.grid(row=0, column=0, sticky=W, pady=(5, 2))
        self.logText = Text(self.iniciaLog, width=45, height=15, wrap='word')
        self.logText.grid(row=1, column=0, pady=4)
        self.logText.configure(state='disabled')

        # Criando a ScrollBar e associando a TextBox
        self.logScroll = ttk.Scrollbar(self.iniciaLog, orient=VERTICAL, command=self.logText.yview)
        self.logScroll.grid(row=1, column=1, sticky=(N, S))
        self.logText['yscrollcommand'] = self.logScroll.set

        # Create textLogger
        self.text_handler = FrameLog.TextHandler(self.logText)

        # Add the handler to logger
        self.logger = logging.getLogger()
        self.logger.addHandler(self.text_handler)
        self.logger.setLevel('INFO')

        # Inicializando o LOG com formato diferente:
        self.text_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.info('=' * 10 + 'Inicializando o programa' + '=' * 11 + '\n' * 2)
        self.logger.info(' ' * 12 + 'Inicializando o LOG:' + ' ' * 13 + '\n'*2)

        # Formatação do log:
        self.format_ = ' (%(asctime)s) [%(levelname)s]:\n     %(message)s\n\n'
        self.text_handler.setFormatter(logging.Formatter(self.format_))

        self.logger.info('Iniciando Frame de log.')

        # INFO: Exemplos de mensagens de log
        # self.logger.debug('debug message')
        # self.logger.info('info message')
        # self.logger.warn('warn message')
        # self.logger.error('error message')
        # self.logger.critical('critical message')

    def WriteLog(self, level, text):
        """Esta função pode ser chamada externamente pelas outras classes para
            escrever no log global do programa, devendo somente ser passada a instância.
        """
        if level == 'debug':
            self.logger.debug(text)
        elif level == 'info':
            self.logger.info(text)
        elif level == 'warn':
            self.logger.warn(text)
        elif level == 'error':
            self.logger.error(text)
        elif level == 'critical':
            self.logger.critical(text)
        else:
            self.logger.critical('NÍVEL DE LOG ERRADO!')

    class TextHandler(logging.Handler):
        """Esta classe permite o log do sistema ser escrito em um widget Text do tkinter
            ou num ScrolledText.
        """

        def __init__(self, text):
            # corre o Handler __init__
            logging.Handler.__init__(self)

            # guarda a referência ao tkinter.Text onde será feito o log.
            self.text = text

        def emit(self, record):
            msg = self.format(record)

            def append():
                self.text.configure(state='normal')
                self.text.insert(END, msg)
                self.text.configure(state='disabled')
                # Autoscroll após cada entrada.
                self.text.yview(END)

            # Comentário original: "This is necessary because we can't modify the Text from other threads"
            self.text.after(0, append)
