import subprocess
import paramiko
import requests

def ping(host):
    # Define the ping command, number of pings as 'count' and the target host
    command = ['ping', '-c', '4', host]

    # Run the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the standard output and errors
    stdout, stderr = process.communicate()

    # Decode bytes to string
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    if process.returncode == 0:
        print(f"Success:\n{stdout}")
    else:
        print(f"Error:\n{stderr}")


def nslookup(domain):
    # Define the nslookup command and the target domain
    command = ['nslookup', domain]

    # Run the command
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Get the standard output and errors
    stdout, stderr = process.communicate()

    # Decode bytes to string
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    if process.returncode == 0:
        print(f"NSLookup successful:\n{stdout}")
    else:
        print(f"NSLookup error:\n{stderr}")


def send_ssh_command():
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #아이디 비밀번호 입력
        ssh_client.connect("computer.tukorea.ac.kr", 22, "아이디", "비밀번호")
        
        #stdin, stdout, stderr = ssh_client.exec_command("ls -l")
       # print(f"SSH command output:\n{stdout.read().decode('utf-8')}")
       # print(f"SSH command error:\n{stderr.read().decode('utf-8')}")
        
        ssh_client.close()
    except paramiko.AuthenticationException:
        print("Authentication failed")
    except paramiko.SSHException as sshException:
        print(f"Unable to establish SSH connection: {sshException}")
    except paramiko.BadHostKeyException as badHostKeyException:
        print(f"Unable to verify server's host key: {badHostKeyException}")
    except Exception as e:
        print(f"Error: {e}")


def send_http_get(url):
    urlFormat = f"http://{url}"
    try:
        response = requests.get(urlFormat)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        print(f"Success:")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error: {err}")