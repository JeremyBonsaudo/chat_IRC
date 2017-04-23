import socket, sys, select, signal

def handler(sig, frame) :                           #Definition du signal
	stri = username + " s'est déconnecté !"
	sock.send(stri.encode())
	print("\nA Bientôt !")
	sock.close()
	sys.exit()

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGHUP, handler)
signal.signal(signal.SIGPIPE, handler)

hote = sys.argv[1]
port = int(sys.argv[2])
username = str(sys.argv[3])


run = True

try:         #On essaye de créer un socket et de se connecter au serveur
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hote, port))
    print('Connecté sur le port {}.'.format(port))
    # Envoie mon username
    a = username
    sock.send(a.encode())
    data = sock.recv(1024)

    prompt = ''
    
except socket.error:
     print('Connection impossible sur le port {}'.format(port))
     sys.exit(1)

while run :
    try:
        sys.stdout.write(prompt)            #On initialise le prompt
        sys.stdout.flush()

        inputs, outputs,excepts = select.select([0, sock], [],[])

        for i in inputs:
            if i == 0 :
                data = sys.stdin.readline().strip()
                if data :
                    sock.send(data.encode())
                else :
                    print("Deconnection")
                    run = False
                    sock.close()
                    break
            elif i == sock :
                data = sock.recv(1024)
                if not data :
                    print("Deconnection")
                    run = False
                    break
                else :
                    sys.stdout.write(data.decode() + '\n')
                    sys.stdout.flush()
    except KeyboardInterrupt:
        print("Interruption")
        sock.close()
        break

        
