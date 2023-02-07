import socket
from datetime import datetime


class TCPServer:

  def serve(self):
    print("=== サーバーを起動します ===")

    try:
      server_socket = socket.socket()
      server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

      server_socket.bind(("localhost", 8080))
      server_socket.listen(10)

      print("=== クライアントからの接続を待ちます ===")
      (client_socket, address) = server_socket.accept()
      print(f"=== クライアントとの接続が完了しました remote_address: {address} ===")

      request = client_socket.recv(4096)

      with open("server_recv.txt", "wb") as f:
        f.write(request)

      response_body = "<html><body><h1>It works!</h1></body></html>"

      response_line = "HTTP/1.1 200 OK\r\n"

      response_header = ""
      response_header += f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
      response_header += "Host: HenaServer/0.1\r\n"
      response_header += f"Content-Length: {len(response_body.encode())}\r\n"
      response_header += "Connection: Close\r\n"
      response_header += "Content-Type: text/html\r\n"

      response = (response_line + response_header + "\r\n" + response_body).encode()

      client_socket.send(response)

      client_socket.close()

    finally:
      print("=== サーバーを停止します。 ===")

if __name__ == '__main__':
  server = TCPServer()
  server.serve()