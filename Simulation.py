#Andrea Lam 20102, Jorge Caballeros 20009
#Fecha de creaación: 08/03/21
#Modificación 1 :11/03/21
#Referencias: https://simpy.readthedocs.io/_/downloads/en/3.0.12/pdf/
import simpy
import random

def proc (env,nombre,ram,cpu,Cram,instrucciones,numi,tiempo,total):
    run =True
    tiempot=tiempo
    yield env.timeout(tiempo)
    print("Se esta iniciando el proceso, actualmente el proceso",(nombre,env.now),", se encuentra en ready")
    #El tiempo actual en el cual inicia la función
    pivotet=env.now
    
    while run == True:
        yield ram.get(Cram)
        #Tiempo en el que inicia el proceso
        tiempot=tiempot+env.now-pivotet+1
        
        while instrucciones>0:
            pivotet=env.now
            #Realiza el proceso
            with cpu.request() as req:
                yield req
                tiempot=tiempot+env.now-pivotet+1
                yield env.timeout(1)
                instrucciones=instrucciones-numi
                
                temp = random.randint(0,1)
                #Si es 1 se envia a pausa
                if(temp==1):
                    print("El proceso",nombre,", sera enviado a la cola de espera por ",tiempo," segundos. Ocupa:",Cram," de memoria")
                    yield env.timeout(3)
                    tiempot=tiempot+1
                #Si no es 1 se envia a procesar
                else:
                    print("El proceso ",nombre," se esta enviando a procesar ")
        
        #Sale del ciclo donde ya termino e imprime datos
        print("El proceso ",nombre," se a terminado exitosamente, con un tiempo de ",env.now)
        ram.put(Cram)
        run=False
        print("Tardo ",tiempot," en realizar el proceso ",nombre)
        total.put(tiempot)
        

#Variables y valores
env = simpy.Environment()
ram = simpy.Container(env, init=100,capacity=100)
total = simpy.Container(env,capacity=1000000000000000000000000)
cpu = simpy.Resource(env, capacity= 2)

#NUMERO DE PROCESOS --------------------------------------------------------------
procesos = 25

for i in range(procesos):
    t1=random.randint(1,10)
    t2=random.randint(1,10)
    t3=(random.expovariate(1/10) + 1)
    #Mando a llamar a la funcion con los datos equivalentes
    env.process(proc(env,i+1,ram,cpu,t1,t2,3,round(t3),total))

env.run()

print("Tiempo total para todos los procesos ")
print(total.level/procesos)
                    
                
                
                
            