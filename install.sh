
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
