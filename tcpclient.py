import socket

class TCPClient:

  def request(self):

    print("=== クライアントを起動します ===")

    try:
      client_socket = socket.socket()
      client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

      print("=== サーバーと接続します ===")
      client_socket.connect(("127.0.0.1", 80))
      print("=== サーバーとの接続が完了しました ===")

      with open("client_send.txt", "rb") as f:
        request = f.read()

      client_socket.send(request)

      response = client_socket.recv(4096)

      with open("client_recv.txt", "wb") as f:
        f.write(response)

      client_socket.close()

    finally:
      print("=== クライアントを停止します。 ===")

if __name__ == '__main__':
  client = TCPClient()
  client.request()