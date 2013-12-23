# monitoring sensor temperatures and adding these to the database
# the database is shown on the web

import subprocess, os, re, sqlite3

def get_data():

    try:
        result=[]
        hdd = subprocess.check_output(["sudo df | grep rootfs | awk '{print $2,$3,$4,$5}'"], shell=True)
        hdd = hdd.split()
        hdd_free = int(hdd[2]) / 1024
        hdd_used = int(hdd[1]) / 1024

        result.append(hdd_free)
        result.append(hdd_used)

#        cpu = subprocess.check_output(["vmstat | awk '{print $13}'"], shell=True)
#        cpu = cpu.split()[1]
#        result.append(cpu)

        mem = subprocess.check_output(["sudo cat /proc/meminfo | grep Mem | awk '{print $2}'"], shell=True)
        mem = mem.split()
        mem_total = int(mem[0]) / 1024
        mem_free = int(mem[1]) / 1024
        mem_used = mem_total - mem_free
        result.append(mem_used)
        result.append(mem_free)

        cpu_temp = subprocess.check_output(["sudo /opt/vc/bin/vcgencmd measure_temp"], shell=True)
        m=re.findall('^.*\=(.{4}).*$',cpu_temp)
        result.append(float(m[0]))

        with open('/proc/uptime', 'r') as f:
            uptime = round(float(f.readline().split()[0])/60/60,2)
        result.append(uptime)

        return result

    except:
        print "Error"
        return None

def log_data(valstr):

    dbname='/var/www/monitor.db'

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    curs.execute("insert into RT_data values(datetime('now'), (?),(?),(?),(?),(?),(?))", (valstr[0],valstr[1],valstr[2],valstr[3],valstr[4],valstr[5],))

    conn.commit()
    conn.close()

#print get_data()
log_data(get_data())
