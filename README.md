# ljudmila-radio
Repo for Experimental Broadcasting workshop run at Ljudmila 3 Dec 2019

## 1/ Assemble materials
RPi  
SD card  
antenna (alligator clip w/wire)  
Power  
Ethernet cable  

## 2/ Enable ETH sharing / network sharing

## 3/ Download + Install wireshark

## 4/ Download + Install Raspbian
wget https://weise7.org/~danja/rpi-broadcast.img.zip  
unzip rpi-broadcast.img.zip  
rm rpi-broadcast.img.zip  
df -h  
sudo umount /dev/sda1  
sudo dd bs=1M if=<dir>/rpi-broadcast.img of=/dev/sda  
sudo eject /dev/sda  
touch /media/chootka/boot/ssh  
sudo eject /dev/sda  

## 5/ Log in to RPi + configure
ssh pi@<ip addr> / raspberry  
to force IP assignment - turn wired connection off/on then power cycle pi  
sudo raspi-config (change password, expand file system)  
sudo apt-get update  
sudo apt-get install -y sox git libsox-fmt-mp3  

## 6/ git clone https://github.com/markondej/fm_transmitter.git  
cd fm_transmitter  
make  
sudo ./fm_transmitter -f 102.9 acoustic_guitar_duet.wav  

## 7/ get scripts and conf files
cd  
git clone https://github.com/chootka/ljudmila-radio.git  
cd ljudmila-radio  
mv PiStation.py ../fm_transmitter  

## 8/ Play MP3s or play through a directory w/wav or mp3
cd music  
unzip fizzarum.zip  
rm fizzarum.zip  
mv * ~/upload  
cd ~/fm_transmitter  
mv *.wav ../upload  
sudo python ./PiStation.py -f 102.9 ../upload/fizzarum/03-vesat.mp3  
sudo python ./PiStation.py -f 102.9 ../upload/  

## 9/ Broadcast from audio input via external USB microphone or sound card
### Via USB headphones w/mic or line in  
arecord -l (list audio devices registered w/system)  
### broadcast from usb microphone or soundcard input (maybe from your phone, other audio source w/3.5mm output)  
sudo python ./PiStation.py -f 102.9 line  

## 9/ Set up web interface
sudo apt install lighttpd php7.3-fpm php7.3-mbstring php7.3-mysql php7.3-curl php7.3-gd php7.3-curl php7.3-zip php7.3-xml  
sudo lighttpd-enable-mod fastcgi-php  
cd ~/ljudmila-radio  
sudo cp -vf conf/15-fastcgi-php.conf /etc/lighttpd/conf-enabled/  
sudo cp -vf conf/php.ini /etc/php/7.3/fpm/  
sudo service lighttpd force-reload  
install simple web UI for uploading  
sudo cp -vf web/* /var/www/html  

## 10/ Set up access point and dnsmasq for captive portal
sudo apt-get install -y hostapd dnsmasq  
nano conf/interfaces  
change wlan0 static address to something unique, 192.168.9x.1  
sudo cp -vf conf/interfaces /etc/network/  
nano conf/hostapd.conf  
- set new wireless access point name + change channel  
sudo cp -vf conf/hostapd.conf /etc/hostapd/  
nano conf/dnsmasq.conf  
change address to address=/#/<ip addr>  
change dhcp address range to match <ip addr> of device  
sudo cp -vf conf/dnsmasq.conf /etc/  
sudo systemctl unmask hostapd  
sudo reboot  