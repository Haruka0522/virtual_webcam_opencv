git clone https://github.com/umlaeute/v4l2loopback.git
cd v4l2loopback
make
sudo make install
depmod -a
sudo modprobe v4l2loopback exclusive_caps=1
