$! /usr/bin/venv bash -vx
#
# by the time this script runs your project has all you need
# only thing left is installing
#
sudo mkdir /opt/stats_collector
sudo cp -r ./stats_collector/* /opt/stats_collector/
sudo cd /opt/stats_collector
sudo python -m venv /opt/stats_collector/venv
sudo . /opt/stats_collector/venv/bin/activate
sudo python -m pip install --upgrade -r requirements.txt
sudo chown -R :www-data /opt/stats_collector
sudo chmod -R 775 /opt/stats_collector
sudo cp ./stats_collector.service /etc/systemd/system/
sudo cp stats_collector /etc/nginx/sites-enabled/
sudo cp default /etc/nginx/sites-enabled/default
sudo systemctl daemon-reload
sudo systemctl start stats_collector.service
sudo systemctl enable stats_collector.service
sudo systemctl restart nginx
