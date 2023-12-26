#!/usr/bin/env bash
#a Bash script that sets up your web servers for the deployment of web_static

# Install Nginx if not already installed
if ! dpkg -l | grep -q nginx; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi

# Stop Nginx service
sudo service nginx stop

# Create directories and sub-directories and change ownership
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared
# sudo chown -R ubuntu:ubuntu /data/

# Create a symbolic link to /test/ as current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership of directory and sub-files after creting sym link
sudo chown -R ubuntu:ubuntu /data/

# Create a fake HTML file
sudo echo "<html>
<head></head>
<body><p>
SOMETHING NICE IS COMING HERE SOON!
</p></body>
</html>" > /data/web_static/releases/test/index.html

# Backup config and relink symbolic link
sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sudo sed -i '/server_name _;/a \\tlocation /hbnb_static { \n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# Restart Nginx service
sudo service nginx start

exit 0
