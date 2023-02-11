import socket

from workerthread import WorkerThread

class WebServer:
  def serve(self):
    print("=== Server: サーバーを起動します ===")

    try:
      server_socket = self.create_server_socket()

      while True:

        print("=== Server: クライアントからの接続を待ちます ===")
        (client_socket, address) = server_socket.accept()
        print(f"=== Server: クライアントとの接続が完了しました remote_address: {address} ===")

        thread = WorkerThread(client_socket, address)

        thread.start()
    finally:
      print("=== Server: サーバーを停止します。 ===")

  def create_server_socket(self) -> socket:
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(("localhost", 8080))
    server_socket.listen(10)

    return server_socket