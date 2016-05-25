import os
import app.module.mod_database as database



def createFloppy(pod,nod,pub):


    os.popen("rm -rf app/temp")


    os.popen("mkdir app/temp")


    os.popen("mkdir app/temp/"+pod)

    os.popen("wget http://localhost:5000/"+pod+"/platformConfig.xml")

    os.popen("mv platformConfig.xml app/temp/"+pod+"/")


    if pub == True:
        os.popen("touch app/temp/"+pod+"/clusterConfig.xml")


    os.popen("dd if=/dev/zero of=app/temp/"+pod+"/"+nod+".img count=1440 bs=1k")

    os.popen("/sbin/mkfs.msdos app/temp/"+pod+"/"+nod+".img")

    os.popen("mcopy -i app/temp/"+pod+"/"+nod+".img app/temp/"+pod+"/platformConfig.xml ::/")

    if pub == True:
        os.popen("mcopy -i app/temp/"+pod+"/"+nod+".img app/temp/"+pod+"/clusterConfig.xml ::/")



createFloppy("07","cucm01",False)
