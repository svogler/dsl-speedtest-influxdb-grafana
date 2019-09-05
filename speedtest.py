import subprocess
import datetime
from influxdb import InfluxDBClient

cmd = '/usr/local/bin/speedtest --simple'
host = '192.168.178.38'
port = '8086'
user = 'admin'
password = 'influx'
dbname = 'DSL'

time = datetime.datetime.utcnow()

# run command, capture stdout & stderr, decode tuple byte list to tuple string list, split string by space
p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate()
stdout_string = stdout.decode("utf8")
bandwidth = stdout_string.split()
# bandwidth should now have ping result in index 1, download in index 4, upload in index 7

print(bandwidth)

# create connection to InfluxDB with pre-defined parameters. Do inserts for each value, tagging each one.
# use current time for value. inserting 3 tags at once goes against InfluxDB data structure
dbclient = InfluxDBClient(host, port, user, password, dbname)

json_body = [
{
    "measurement": "dslmeasure",
    "tags": {
        "type": "Home"
    },
    "time": time,
    "fields": {
        "latency": float(bandwidth[1]),
        "download": float(bandwidth[4]),
        "upload": float(bandwidth[7])

    }
}
]

