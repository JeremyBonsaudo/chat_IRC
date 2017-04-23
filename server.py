import select, socket, sys, signal

def handler(signal, none) :                    #Definition du signal.
	print("\nServer off\n")
	for server in inputs:
		if server != server:
			connsock.shutdown(socket.SHUT_RD-WR)
			connsock.close()
	sys.exit(0)

def username(client) :                  #Récupération de l'username.
    info = clientmap[client]
    name = info[1]
    return name[0]

def update_list(L, msg) :               #Update de la liste contenant les 5 derniers messages.
    if len(L) >= 5 :
	    L = L[1:]
	    L.append(msg)
    else :
	    L.append(msg)
    return L

def print_html(L) :                     #Contenue de la page html
    html = """<!DOCTYPE html>
    <head>
        <title>5 derniers messages :</title>
    </head>
    <body>
    <p>5 derniers messages :</p>
    <ol>
        <li>"""+L[4]+"""</li>
        <li>"""+L[3]+"""</li>
        <li>"""+L[2]+"""</li>
        <li>"""+L[1]+"""</li>
        <li>"""+L[0]+"""</li>
    </ol>
        
    </body>
    </html>
    """

    return html

def print_html_error() :                     #Contenue de la page html avec l'erreur 404
    html = """<!DOCTYPE html>
    <head>
        <title>error 404</title>
    </head>
    <body>
    <p>Error 404</p>
    </body>
    </html>
    """

    return html
    
		
		

signal.signal(signal.SIGINT, handler)


hote = sys.argv[1]
port = int(sys.argv[2])
port_web = int(sys.argv[3])

###################Serveur Chat########################
clients = 0
clientmap = {}
outputs = []
try :                   #Création du socket serveur.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except :
    print("Création du socket impossible !")

server.bind((hote,port))
server.listen(5)

print("Serveur connecter sur le port {}\n".format(port))


###################Serveur Web########################
global histo
histo = [""] * 5

try :                   #Création du socket Web.
    web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except :
    print("Création du socket impossible !")

web.bind((hote,port_web))
web.listen(5)


inputs = [server, web, sys.stdin]
outputs = []
    
run = 1

while run :
    try :
        inputready, outputready, exceptready = select.select(inputs, outputs, [])
    except select.error:
        break
    except socket.error:
        break

    for s in inputready:

        if s == server :                          #On accepte un client
            client, adress = server.accept()
            
            cname = client.recv(1024).decode()
            cname = cname.split('NAME: ')

            clients += 1
            a = 'CLIENT: ' + str(cname[0][:-1]) + '\n'
            client.send(a.encode())
            inputs.append(client)

            clientmap[client] = (adress, cname)

            msg = '\nNouveau client : {}'.format(username(client))      #On affiche ça connection 
            for o in outputs:                                           #et on l'envoie à tous les clients.
                o.send(msg.encode())

            outputs.append(client)
            print(msg)
            
        elif s == sys.stdin:
            junk = sys.stdin.readline()
            run = 0
            
        ##connexion au serveur web##
        elif (s == web):
            web_client, web_adress = web.accept()
            request = web_client.recv(1024)
            if request:
                try :
                        web_client.send(b'HTTP/1.0 200 OK\n')
                        web_client.send(b'Content-Type: text/html\n\n')
                        print_msg = ''
                        html = print_html(histo)
                        web_client.send(str(html).encode())
                        web_client.close()
                except :
                        web_client.send(b'HTTP/1.0 200 OK\n')
                        web_client.send(b'Content-Type: text/html\n\n')
                        print_msg = ''
                        html = print_html_error()
                        web_client.send(str(html).encode())
                        web_client.close()
            else :
                web_client.send(b'HTTP/1.0 200 OK\n')
                web_client.send(b'Content-Type: text/html\n\n')
                print_msg = ''
                html = print_html_error()
                web_client.send(str(html).encode())
                web_client.close()

    
        else:
            try:
                data = s.recv(1024)
                if data:
                    msg = '\n' + username(s) + ': ' + data.decode()      #Message sous la forme : "Jeremy: Bonjour!"
                    histo = update_list(histo, msg[1:]) #On enleve le \n du message sous string et on l'ajoute à la liste.
                    print(msg)
                    for o in outputs:           #Envoie du msg à tous les clients.
                        o.send(msg.encode())
                    
                else :
                    s.close()
                    inputs.remove(s)
                    outputs.remove(s)

                    msg = '\nDeconnection de {}'.format(username(s))     #Information que le client s'est déconnecté.
                    for o in outputs:
                        o.send(msg.encode())
            except socket.error:
                inputs.remove(s)
                outputs.remove(s)
                s.close()
server.close()
web.close()
    

            
