import socket
import urllib.parse



def parse_url(url):
	parseResult = urllib.parse.urlparse(url)

	if parseResult.hostname:
		print(parseResult.hostname)
		print(parseResult.port)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("www.example.com", 80))

request = f'GET / HTTP/1.1\r\nHost:www.example.com\r\n\r\n'

print(request)

sock.sendall(request.encode('utf-8'))

response = sock.recv(4096)

print(response.decode())    # UTF-8-encoded string
sock.close()

url = 'https://www.example.com/'
parse_url(url)
