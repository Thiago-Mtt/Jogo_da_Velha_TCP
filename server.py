import socket,  threading, time

host = '127.0.0.1'
port = 5000

class Jogador:
    
    vitoria = ('147', '258', '369', '789', '456',
     '123', '357', '159')

    def __init__(self, con=None, cliente=None, mov=''):
        # estoque = nome do estoque;
        self.con = con
        self.cliente = cliente
        self.mov = mov

    def rodada(self):
        while True:
            msg = self.con.recv(1024)
            if msg: break
        msg = msg.decode(encoding='UTF-8',errors='ignore')
        return (msg)

    def vencedor(self):
        lis_mov = list(self.mov)
        lis_mov.sort()
        contador = 0
        for v in Jogador.vitoria:
            for nro in range(len(lis_mov)):
                if lis_mov[nro] in v:
                    contador = contador + 1
                if contador == 3:
                    return True
            contador = 0
        return False


def jogo(jogadores):
    j1 = Jogador(jogadores[0], jogadores[1])
    j2 = Jogador(jogadores[2], jogadores[3])
    j1.con.send(b'partida comeca')
    j2.con.send(b'partida comeca')
    mov_disp = '987654321'
    partida = True
    j1.con.send(b'start')
    while partida == True:
        msg = j1.rodada()
        if msg in mov_disp:
            j1.mov = j1.mov+msg
            mov_disp = mov_disp.replace(msg, '')
        venceu = j1.vencedor()
        if venceu == True:
            j1.con.send(b'voce venceu')
            j2.con.send(b'voce perdeu')
            j1.con.close()
            j2.con.close()
            break
        if len(mov_disp) == 0:
            j1.con.send(b'velha')
            j2.con.send(b'velha')
            j1.con.close()
            j2.con.close()
            break
        j2.con.send(j1.mov.encode())
        msg = j2.rodada()
        if msg in mov_disp:
            j2.mov= j2.mov+msg
            mov_disp = mov_disp.replace(msg, '')
        venceu = j2.vencedor()
        if venceu == True:
            j2.con.send(b'voce venceu')
            j1.con.send(b'voce perdeu')
            j2.con.close()
            j1.con.close()
            break
        if len(mov_disp) == 0:
            j1.con.send(b'velha')
            j2.con.send(b'velha')
            j1.con.close()
            j2.con.close()
            break
        j1.con.send(j2.mov.encode())


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (host, port)

tcp.bind(orig)
tcp.listen(1)

fila = []

while True:
    j = Jogador()
    j.con, j.cliente = tcp.accept()
    print('conexao aceita')
    if fila == []:
        fila.append(j.con)
        fila.append(j.cliente)
        j.con.send(b'aguarde um oponente')
    else :
        fila.append(j.con)
        fila.append(j.cliente)
        j.con.send(b'oponente disponivel')
        t = threading.Thread(target=jogo, args=(fila,))
        t.start()
        fila = []

