import os
from pathlib import Path
from CONFIG import FIRST_CONFIG,SSH_CONFIG
import subprocess

domain_type=int(input('Input the domain type 1-poddomain 2-main domain:'))
print(domain_type)
domain_name=input('write the domain name:')
folder_name=domain_name 
file_name=domain_name 

if domain_type==2:
    domain_name=f'{domain_name} www.{domain_name} include acme'
try:
    os.makedirs(f'/var/www/html/{folder_name}')
except FileExistsError:
    pass
try: 
    os.makedirs(f'/etc/nginx/sites-enabled')
except FileExistsError:
    pass 

file_dir=os.path.join('/etc/nginx/sites-enabled/', file_name)
print(file_dir)
with open(file_dir, 'w+') as f:
    config=FIRST_CONFIG.replace('$FOLDER$',folder_name).replace('$DOMAIN$',domain_name)
    
    f.write(config)

print('deleting default nginx...')
bashCommand = "rm /etc/nginx/sites-enabled/default"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
print('nginx default deleted.\n')

print('restarting nginx without certificate...')
bashCommand = "systemctl restart nginx"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
print('nginx without certificate restarted.\n')

print('getting certificate...')
if domain_type==2:
    bashCommand = f"certbot certonly -a standalone -n -d {folder_name} -d www.{folder_name}"
    
else:
    bashCommand = f"certbot certonly -a standalone -n -d {folder_name}"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
print('certificate getted.\n')

print('rewriting nginx with certificate...')
with open(file_dir, 'w+') as f:
    config=SSH_CONFIG.replace('$FOLDER$',folder_name).replace('$DOMAIN$',domain_name)
    
    f.write(config)
print('nginx with certificate rewrited.\n')

print('settup chown 443...')
bashCommand = f"sudo chown -R www-data:www-data /var/www/html/{folder_name}"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
print('chown setted.\n')

print('restarting nginx with certificate...')
bashCommand = "systemctl restart nginx"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
print('nginx with certificate restarted.\n')