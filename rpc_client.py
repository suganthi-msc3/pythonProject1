import xmlrpc.client
proxy=xmlrpc.client.ServerProxy('http://localhost:8002/')
hello=proxy.sayHello()
print("message from server  %s" %hello)