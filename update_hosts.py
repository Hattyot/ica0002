import re
import requests
import bs4

HOST_IP = "193.40.156.67"
SSH_KEY = "~/.ssh/id_rsa"
USERNAME = "Hattyot"


def get_hosts() -> list[dict]:
    """
    Gets host data on ica0002 vms
    :return: vm name, ssh port, ssh username
    """
    url = f'http://{HOST_IP}/students/{USERNAME}.html'
    data = requests.get(url)
    vms = bs4.BeautifulSoup(data.text, features="html5lib").find(name="table").find_all("tr")[1:]
    vm_data = []
    for vm in vms:
        try:
            data = [*vm.children]
            name = data[0].string
            ssh_port = data[2].string.split(" port ")[-1]
            ssh_username = data[2].string.split("@")[0]
            vm_data.append({"name": name, "port": ssh_port, "username": ssh_username})
        except:
            pass

    return vm_data


def update_hosts_file():
    hosts_file = './hosts'

    old_content = open(hosts_file, 'r').read()

    vm_data = get_hosts()
    lines = [f"vm{i + 1} ansible_port={vm['port']}" for i, vm in enumerate(vm_data)]
    section_pattern = r"(###\sBEGIN\sHOSTS\n?)((?:.|\n)*)(\n?###\sEND\sHOSTS)"
    new_content = re.sub(section_pattern, r"\1" + "\n".join(lines) + r"\n\3", old_content)

    open(hosts_file, 'w').write(new_content)


def update_ssh_config():
    ssh_config_file = "/home/ssaart/.ssh/config"

    old_content = open(ssh_config_file, 'r').read()

    vm_data = get_hosts()
    hosts = [f"""Host vm{i + 1}
    Hostname {HOST_IP}
    Port {vm['port']}
    User {vm['username']}
    ProxyCommand sh -c "python /home/ssaart/Documents/TTU/ica0002/update_hosts.py; /usr/bin/nc %h %p"
    IdentityFile {SSH_KEY}""" for i, vm in enumerate(vm_data)]

    if "### BEGIN ICA0002" not in old_content:
        old_content += "### BEGIN ICA0002\n### END ICA0002"

    section_pattern = r"(###\sBEGIN\sICA0002\n?)((?:.|\n)*)(\n?###\sEND\sICA0002)"
    new_content = re.sub(section_pattern, r"\1" + "\n".join(hosts) + r"\n\3", old_content)

    open(ssh_config_file, 'w').write(new_content)


if __name__ == '__main__':
    update_hosts_file()
    update_ssh_config()
