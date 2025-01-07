Simply want to test my coding skills to make a frontend GUI that is attached to a backend that has YT-DLP installed. 

FIRST CONFIGURE AND INSTALL YT-DLP IN THE BACKEND.
sudo apt install pip
sudo pip install --upgrade --force-reinstall "git+https://github.com/ytdl-org/youtube-dl.git"

IN ADDITION (but not available in current release) YOUTUBE-DL
git clone https://github.com/ytdl-org/youtube-dl.git youtube-dl
cd youtube-dl/
make youtube-dl
sudo cp youtube-dl /usr/local/bin/
