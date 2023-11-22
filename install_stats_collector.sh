#/usr/bin/venv bash -v

tar xvfz stats_collector.tar.gz
mkdir /opt/stats_collector
cp -r ./stats_collector/* /opt/stats_collector/
cd /opt/stats_collector
python -m venv /opt/stats_collector/venv
. /opt/stats_collector/venv/bin/activate
python -m pip install --upgrade -r requirements.txt
deactivate
chown -R root:www-data /opt/stats_collector
chmod -R 775 /opt/stats_collector
cp ./stats_collector.service /etc/systemd/system/
cp stats_collector /etc/nginx/sites-enabled/
cp default /etc/nginx/sites-enabled/default
systemctl daemon-reload
systemctl start stats_collector.service
systemctl enable stats_collector.service
systemctl restart nginx
