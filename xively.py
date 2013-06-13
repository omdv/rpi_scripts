# cosm.py Copyrigth 2012 Itxaka Serrano Garcia <itxakaserrano@gmail.com>
# licensed under the GPL2
# see the full license at http://www.gnu.org/licenses/gpl-2.0.txt
#
# You only need to add 2 things, YOUR_API KEY HERE and YOUR_FEED_NUMBER_HERE
# also, you can change your stream ids, in that case change the id names in the "data = json.dumps..." line

import json, subprocess, os

hdd = subprocess.check_output(["df | grep rootfs | awk '{print $2,$3,$4,$5}'"], shell=True)
hdd = hdd.split()
hdd_avail = int(hdd[2]) / 1024
hdd_used = int(hdd[1]) / 1024

cpu = subprocess.check_output(["vmstat | awk '{print $13}'"], shell=True)
cpu = cpu.split()[1]

mem = subprocess.check_output(["cat /proc/meminfo | grep Mem | awk '{print $2}'"], shell=True)
mem = mem.split()
mem_total = int(mem[0]) / 1024
mem_free = int(mem[1]) / 1024
mem_used = mem_total - mem_free

cpu_temp = subprocess.check_output(["sudo /opt/vc/bin/vcgencmd measure_temp | cut -c6-9"], shell=True)

with open('/proc/uptime', 'r') as f:
	uptime = round(float(f.readline().split()[0])/60/60,2)

data = json.dumps({"version":"1.0.0", "datastreams":[{"id":"uptime","current_value":uptime },{"id":"hdd_used","current_value":hdd_used },{"id":"hdd_free","current_value":hdd_avail },{"id":"mem_free","current_value":mem_free},{"id":"mem_used","current_value":mem_used},{"id":"cpu_temp","current_value":cpu_temp}]})
with open("temp.tmp", "w") as f:
	f.write(data)

subprocess.call(['curl --request PUT --data-binary @temp.tmp --header "X-ApiKey: j8wMYwFf19v0TsH0d4uwsMn373TlDdhTyHMjx364jKrrO0HS" http://api.cosm.com/v2/feeds/785647941'], shell=True)

os.remove("temp.tmp")
