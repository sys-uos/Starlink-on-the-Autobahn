import datetime
import subprocess
import pandas as pd
import time
import os

lt_trace = pd.read_csv('Data/Emulation/loss_time_trace.csv')
lt_trace['relative_time'] = lt_trace['relative_time'].astype(float)
lt_trace['lost'] = lt_trace['lost'].astype(bool)


def del_qdisc():
    command = ['ip', 'netns', 'exec', 'ns2', 'tc', 'qdisc',
               'delete', 'dev', 'veth2', 'root']
    process = subprocess.Popen(command)
    stdout, stderr = process.communicate()
    exit_code = process.returncode
    print('Cond removded (' + str(exit_code) + ')')
    

def init_default_state():
    del_qdisc()
    command = ['ip', 'netns', 'exec', 'ns2', 'tc', 'qdisc',
               'add', 'dev', 'veth2', 'root',
               'netem', 'rate', '300mbit', 'loss', '0%', 'delay', '36ms', '33ms', 'distribution', 'pareto', 'seed', '42', 'limit', '100000']
    process = subprocess.Popen(command)
    stdout, stderr = process.communicate()
    exit_code = process.returncode
    print('Loss set to 0% (' + str(exit_code) + ')')

def set_default_state():
    command = ['ip', 'netns', 'exec', 'ns2', 'tc', 'qdisc',
               'replace', 'dev', 'veth2', 'root',
               'netem', 'rate', '300mbit', 'loss', '0%', 'delay', '36ms', '33ms', 'distribution', 'pareto', 'seed', '42', 'limit', '100000']
    process = subprocess.Popen(command)
    stdout, stderr = process.communicate()
    exit_code = process.returncode
    print('Loss set to 0% (' + str(exit_code) + ')')

def set_bridge_state():
    command = ['ip', 'netns', 'exec', 'ns2', 'tc', 'qdisc',
               'replace', 'dev', 'veth2', 'root',
               'netem', 'rate', '300mbit', 'loss', '100%', 'delay', '36ms', '33ms', 'distribution', 'pareto', 'seed', '42', 'limit', '100000']
    process = subprocess.Popen(command)
    stdout, stderr = process.communicate()
    exit_code = process.returncode
    print('Loss set to 100% (' + str(exit_code) + ')')
    
def start_tshark_in_namespace(namespace, output_file, iface):
    try:
        # Construct the tshark command
        command = [
            'ip', 'netns', 'exec', namespace, 
            'tshark', 
            '-w', output_file,  # Write output to the specified file
            '-i', iface  # Capture from any interface; you may specify a specific interface
        ]

        # Start the subprocess
        print(f"Starting tshark in namespace '{namespace}' and writing to '{output_file}'")
        tshark_process = subprocess.Popen(command)
        return tshark_process

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def start_webserver_in_namespace(namespace, port):

    # Construct the command to run the Python HTTP server
    command = [
        'ip', 'netns', 'exec', namespace,
        'python3', '-m', 'http.server', str(port)
    ]

    # Start the subprocess to run the web server
    print(f"Starting Python web server in namespace '{namespace}' on port {port}...")
    webserver_process = subprocess.Popen(command)

    return webserver_process

def download_file_in_background(namespace, url):
    # Use wget to download the file
    command = [
        'ip', 'netns', 'exec', namespace, 'wget', url,  # The URL to download from
        '-O', 'down/random_47GB_file.bin',  # Specify the output file name
        '--quiet',  # Suppress output
    ]

    # Start the subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("Download started in the background...")

    return process

def busy_wait(ttw):
    start_time = datetime.datetime.now()
    target_time = start_time + datetime.timedelta(seconds=ttw)
    print('Waiting for ' + str(ttw) + 's')
    while datetime.datetime.now() < target_time:
        pass 
    


# initialize random loss with seed
init_default_state()

# run tshark in both namespaces
ts1 = start_tshark_in_namespace('ns1', '47G_ns1_measurement_01.pcap', 'veth1')
ts2 = start_tshark_in_namespace('ns2', '47G_ns2_measurement_01.pcap', 'veth2')
time.sleep(2)
# start webserver
webserv = start_webserver_in_namespace('ns2', 8000)
time.sleep(2)
# start file transfer
dlproc = download_file_in_background('ns1', 'http://10.0.0.2:8000/serv/random_47GB_file.bin')

# start timer to next brigde
while True:
    if dlproc.poll() is not None:
            # Download has finished
            break  # Exit the loop
    # Iterate through the rows of the DataFrame
    for index, row in lt_trace.iterrows():
        if dlproc.poll() is not None:
            # Download has finished
            break  # Exit the loop
        if row['lost']:
            print('change to loss')
            set_bridge_state()
        elif not row['lost']:
            print('change to normal')            
            set_default_state()
        ttw = lt_trace.iloc[index + 1]['relative_time'] - row['relative_time']
        busy_wait(ttw)
    
print('Exiting...')
# kill all subprocesses
ts1.terminate()
ts1.wait()
ts2.terminate()
ts2.wait()
del_qdisc()
webserv.terminate()
webserv.wait()
