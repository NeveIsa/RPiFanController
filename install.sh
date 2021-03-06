
echo "---------------------------"
echo "Need the following tools->"
echo "iwgetid"
echo "raspi-config"
echo "vcgencmd in /opt/vc/bin/vcgencmd"
echo "---------------------------"



echo "-----------------------"
echo "Installing raspi-config"
echo "-----------------------"

yay -S raspi-config || true


echo "Please configure I2C in raspi-config"
sleep 2
raspi-config

echo "--------------------------------"
echo "Installing python-raspberry-gpio"
echo "--------------------------------"
yay -S python-raspberry-gpio

echo "---------------------------------"
echo "Installing from pip using req.txt"
echo "---------------------------------"
pip install -r req.txt

echo "---------------------------------"
echo "Adding $USER to i2c group"
echo "---------------------------------"
adduser $USER i2c

echo "---------------------------------"
echo "Adding pifan service"
echo "---------------------------------"
sudo cp pifan.service /etc/systemd/system

echo "---------------------------------"
echo "Enabling pifan.service"
echo "---------------------------------"
sudo systemctl enable pifan


echo "---------------------------------"
echo "Starting pifan.service"
echo "---------------------------------"
sudo systemctl start pifan
sleep 3
sudo systemctl status pifan




