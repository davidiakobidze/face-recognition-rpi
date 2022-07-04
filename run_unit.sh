export DISPLAY=:0.0
sudo xset s 0 0 -display :0
sudo xset dpms 0 0 0 -display :0
sudo xset s noblank -display :0
sudo xset s off -dpms -display :0
source /opt/intel/openvino/bin/setupvars.sh
exec matchbox-window-manager &
exec "python3" "main.py"
while true; do
  exec "python3" "main.py"
done