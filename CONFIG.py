FIRST_CONFIG="""server {listen 80;
 root /var/www/html/$FOLDER$/public;
 index index.php index.html;
 server_name $DOMAIN$; 
  location / { try_files $uri $uri/ =404; } 
  location ~ \.php$ { 
      include snippets/fastcgi-php.conf;
      fastcgi_pass unix:/var/run/php/php7.3-fpm.sock;
       }
      location ~ /\.ht { deny all; }}"""

SSH_CONFIG="""
server {
    listen 80;

    server_name $DOMAIN$;
    return 301 https://$FOLDER$$request_uri;
}
server { 
  server_name $DOMAIN$;
ssl_certificate "/etc/letsencrypt/live/$FOLDER$/fullchain.pem"; 
ssl_certificate_key "/etc/letsencrypt/live/$FOLDER$/privkey.pem"; 
ssl_ciphers EECDH:+AES256:-3DES:RSA+AES:!NULL:!RC4; 
ssl_prefer_server_ciphers on;
ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
charset UTF-8; 
listen 443 ssl http2;
root /var/www/html/$FOLDER$/public;
error_page 404 /index.php;
index index.php index.html;
location / { try_files $uri $uri/ /index.php?$query_string; }
 location = /favicon.ico 
 { access_log off; log_not_found off; } 
 location = /robots.txt {
      access_log off; log_not_found off; }
       
        location ~ \.php$  {
            include snippets/fastcgi-php.conf; 
       fastcgi_pass unix:/var/run/php/php7.3-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name; } 
        location ~ /\.ht { deny all; }
         }
"""

