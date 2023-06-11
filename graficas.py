import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import matplotlib.animation as animation

#Primero se importan los datos que salen rápido: posición y velocidad del cm y densidades locales

cm=np.genfromtxt("cm.txt",delimiter=" ")
densidades=np.genfromtxt("densidades.txt",delimiter=" ")
fig,ax=plt.subplots()
denslabels=["[-60,-40)","[-40,-20)","[-20,0)","[0,20)","[20,40)","[40,60]"]
for i in range(0,6):
    ax.plot(densidades[:,0],densidades[:,i+1],label=denslabels[i])
plt.xlabel("t")
plt.ylabel("Número de partículas")
ax.legend()
plt.savefig("Densidades.pdf")


fig,ax=plt.subplots()
ax.plot(cm[:,0],cm[:,1],label="Región 1")
ax.plot(cm[:,0],cm[:,3],label="Región 2")
plt.xlabel("t")
plt.ylabel("X")
ax.legend()
plt.savefig("Posiciones.pdf")

fig,ax=plt.subplots()
ax.plot(cm[:,0],cm[:,2],label="Región 1")
ax.plot(cm[:,0],cm[:,4],label="Región 2")
plt.xlabel("t")
plt.ylabel("V")
ax.legend()
plt.savefig("Velocidad.pdf")

os.chdir("./PythonData")
fulldata=[]
print("Leyendo archivos...")
frames=1000

for i in range(0,frames):
    #Esta parte del código funciona. Modificar el index  a 2000 para ejecución completa
    index=int((i)*200000/frames)
    prov=np.genfromtxt("dump.{0}.txt".format(index),delimiter=" ",skip_header=9)
    fulldata.append(prov)
    fulldata[i].sort(axis=0)
    if i%(frames/10)==0:
          print(str(100*i/frames)+"% completado")
print ("Todos los archivos leídos correctamente")
os.chdir("..")

fig=plt.figure()
labels=["id","type","x","Distancia al punto inicial","z","vx","vy","v²"]


def update_hist(num,col):
    if col==-1:
        rang=[0,50]
    else:
        rang=None
    plt.cla()
    plt.hist(fulldata[num][:,col],bins=200,range=rang)
    plt.title("t = " + str(np.round(200000*0.0005*(num+1)/frames,1)))
    plt.xlabel(labels[col])
    plt.ylabel("Número de partículas")
        
for i in fulldata:
    i[:,-1]= (i[:,-1]**2 + i[:,-2]**2 + i[:,-3]**2)
for i in range(0,len(fulldata)):
    fulldata[i][:,3]=((fulldata[i][:,2]-fulldata[0][:,2])**2 + (fulldata[i][:,3]-fulldata[0][:,3])**2 + (fulldata[i][:,4]-fulldata[0][:,4])**2)**(1/2)

writervideo= animation.PillowWriter(fps=60)
Vid=animation.FuncAnimation(fig,update_hist,frames,fargs=(2,),interval=40)
Vid.save("x.gif",writer=writervideo,dpi=100)
print("Video de x guardado")
Vid=animation.FuncAnimation(fig,update_hist,frames,fargs=(-1,),interval=40)
Vid.save("V2.gif",writer=writervideo,dpi=100)
print("Video de v² guardado")
Vid=animation.FuncAnimation(fig,update_hist,frames,fargs=(3,),interval=200)
Vid.save("dist.gif",writer=writervideo,dpi=100)
print("Video de distancia guardado")
