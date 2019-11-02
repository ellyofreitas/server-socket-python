import socket
import sys
# Define as variáveis de endereço e porta
HOST, PORT = ('0.0.0.0', 5000)

# Instancia a variável sock com a conexão socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    try:
        # Define que o servidor vai reaproveitar a conexão antiga do socket que utiliza a mesmo HOST e PORT
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(60)
        # Liga o servidor
        sock.bind((HOST, PORT))

        # Habilita o servidor para aceitar conexões
        sock.listen(1)

        print('Server is ready for connections')

        while True and sock.gettimeout() > 0:
            # Recebe a conexão e endereço de cada conexão socket
            conn, addr = sock.accept()

            print('Connection received from', addr[0])

            with conn:
                # Decodifica a mensagem que veio do client
                data = conn.recv(1024).decode()

                if not data:
                    print('Not data connection')

                if len(data) > 0 and data.split()[1][1:]:
                    # Instancia o nome do arquivo a ser retornado
                    file = (data.split()[1])[1:]

                    # Instancia o nome do diretório a ser buscado o arquivo
                    dir_path = 'public/'

                    try:
                        # Ler o arquivo
                        bytes = open(dir_path + file).read()
                        # Instancia a resposta(arquivo) do client
                        response_body_raw = ''.join(bytes)
                        # Manda os cabeçalhos HTTP
                        conn.send('HTTP/1.1 200 OK\r\n'.encode())
                        conn.send(
                            "Content-Type: text/html\r\n".encode())
                        conn.send('\n'.encode())
                        # Envia a resposta(arquivo) para o client
                        conn.send(response_body_raw.encode())
                        print('Send file is success')
                    # Trata o erro, caso o arquivo não for encontrado
                    except IOError:
                        # Manda os cabeçalhos HTTP
                        conn.send(
                            'HTTP/1.1 404 Not Found\r\n'.encode())
                        conn.send(
                            "Content-Type: text/html\r\n".encode())
                        conn.send("\n".encode())
                        # Manda a mensagem que o arquivo não foi encontrado
                        conn.send("FILE_NOT_FOUND\n".encode())
                        print('Send file is failure')
                    conn.close()
                # Caso o servidor não receba nenhum nome de arquivo ou data
                else:
                    # Manda os cabeçalhos HTTP
                    conn.send('HTTP/1.1 400 Bad Request\r\n'.encode())
                    conn.send("Content-Type: text/html\r\n".encode())
                    conn.send("\n".encode())
                    # Manda a mensagem que a requisição foi feita sem nome do arquivo
                    conn.send("BAD_REQUEST, file is not specified\n".encode())
                    print('Bad request, file is not specified')

                print('Connection to', addr[0], 'closed\n')
                conn.close()

    except Exception as error:
        print('\nServer interrupted from error')
        print('Description error: ', error)
        # Fecha o servidor socket
        sock.close()
        # Desliga o servidor socket
        sock.shutdown(socket.SHUT_RDWR)
        print('Server is down')
        # Fecha o programa
        sys.exit()
    # Trata caso o servidor seja fechado pelo o usuário
    except KeyboardInterrupt as error:
        print('\nProgram interrupted from owner')
