import socket,  threading, time

host = '127.0.0.1'
port = 5000

class Jogador_local():

    tabuleiro = '''
      |     |     
   7  |  8  |  9  
 _____|_____|_____
      |     |     
   4  |  5  |  6  
 _____|_____|_____
      |     |     
   1  |  2  |  3  
      |     |     
'''

    comandos = ['1','2','3','4','5','6','7','8','9']
    dmsgs = ('velha', 'voce perdeu','voce venceu')

    def __init__(self, tcp, mov = []):
        # estoque = nome do estoque;
        self.tcp = tcp
        self.mov = mov

    def msg_server(self,dmsg):
        if dmsg in self.dmsgs:
            print (dmsg)
            self.tcp.close()
            time.sleep(2)
            return False
        return True

    def montar_tabuleiro(self,dmsg):
        if dmsg != 'start':
            tab = self.tabuleiro
            for x in dmsg:
                tab = tab.replace(x, 'O')
            for y in self.mov:
                tab = tab.replace(y, 'X')
            print(tab)
        else: print(self.tabuleiro)

    def com_ok(self, dmsg):
        mov_disp = self.comandos
        for nro in dmsg:
            if nro in mov_disp:
                mov_disp.remove(nro)
        for nro in self.mov:
            if nro in mov_disp:
                mov_disp.remove(nro)
        while True:
            comando = input('faça sua jogada:')
            if comando in mov_disp:
                break
            else : print('jogada inválida')
        return comando






tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (host, port)
tcp.connect(dest)
jogador = Jogador_local(tcp)

while True:
    msg = tcp.recv(1024)
    dmsg = msg.decode(encoding='UTF-8',errors='ignore')
    print(dmsg)
    if dmsg == 'partida comeca' : 
        break

partida = True

while True:
    msg = tcp.recv(1024)
    dmsg = msg.decode(encoding='UTF-8',errors='ignore')
    continuar = jogador.msg_server(dmsg)
    if not continuar: 
        break
    jogador.montar_tabuleiro(dmsg)
    comando = jogador.com_ok(dmsg)
    jogador.mov.append(comando)
    tcp.send(comando.encode())
    print('aguarde')
