from .views import emit, request, randint
def handleconnect(games) :
	emit("message",{"data":"test"})
	games[request.sid] = randint(1,1000)#set une clé dans le dico avec la valeur personnel clé = session id
	emit('message',{"data":request.sid})