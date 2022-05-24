#!/bin/bash

set -eu -o pipefail # if script encounters errors, it immediately exits

while true; do # initial confirmation
read -p "this installation script only works on arch linux and other distrobutions that are arch based, continue? (y/n)" yn
case $yn in
  yY ) echo "proceeding"
    break;;
  nN ) echo "exiting"
    break;;
  * ) echo "enter y/n to continue"
esac
done
  
# does a series of checks to see if you're set for installing

sudo -n true # tests sudo access
test $? -eq 0 || exit 1 "you might wanna have sudo for the installation..."

if hash pacman 2>/dev/null; then # tests pacman
  break
else
  echo "pacman is not installed. please use an arch-based distrobution"
  exit
fi

if hash git 2>/dev/null/; then # tests git
  break
else
  echo "a git installation was not detected in your system, which is required for smoothie. installing now"
  sudo pacman -S --noconfirm --needed git
  exit
fi

if hash yay 2>/dev/null/; then # tests yay
  break
else
  echo "yay is needed for smoothie's installation. installing yay now"
  git clone https://aur.archlinux.org/yay && cd yay && makepkg -si --noconfirm --needed && cd .. && rm -rf yay/
  exit
fi

if hash python 2>/dev/null/; then # tests python
  break
else
  echo "python is needed for smoothie's installation. installing python now"
  sudo pacman -S --noconfirm --needed python
  exit
fi

# installation

echo "checks passed! installing smoothie's depends"
yay -S --noconfirm --needed vapoursynth vapoursynth-plugin-svpflow1 vapoursynth-plugin-svpflow2-bin vapoursynth-plugin-havsfunc

echo "finished installing depends, installing plugins"
sudo cp ../plugins/*.py /usr/lib/python3*/site-packages/
sudo curl https://github.com/couleurm/vs-frameblender/releases/download/1.2/vs-frameblender-1.2.so -o /usr/lib/vapoursynth/vs-frameblender-1.2.so

echo "finished installation! adding smoothie's command line shortcut"
if [[ $SHELL == "/bin/bash" ]]; then # thank you ultratoon
  cd ..
  echo "alias sm='python $PWD/smoothie.py'" >> "$HOME/.bashrc"
elif [[ $SHELL == "/bin/zsh" ]]; then
  cd ..
  echo "alias sm='python $PWD/smoothie.py'" >> "$HOME/.zshrc"
else
  cd ..
  echo "Did not detect what shell you are using, please add this to your shells configuration file:"
  echo "alias sm='python $PWD/smoothie.py'"
fi

echo "thanks for installing smoothie! a lot of people put a lot of time an effort into making this, so please consider joining our discord (https://discord.gg/ctt) for any issues or just to meet the dev team!"
echo "remember to restart your terminal session for the 'sm' shortcut to work!"
exit
