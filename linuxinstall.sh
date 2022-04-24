#!/bin/sh
set -e

while true; do
  read -p "NOTICE: The Smoothie installation script is in early stages and only currently works for Arch Linux and its distributions, do you wish to try this script? [Y/N] " yn
  case $yn in
      [Yy]* ) break;;
      [Nn]* ) exit;;
      * ) echo "Please answer Y or N!";;
  esac
done

echo "Welcome to the Smoothie installation script!"
echo "Checking and installing dependencies..."
echo " "

# CHECKING #########################

# Check for pacman, in order to validate if the user is using Arch Linux.
if command -v /usr/bin/pacman >/dev/null 2>&1; then
  echo "Pacman will be used for installing dependencies."
else
  echo "Pacman is NOT installed, please use Arch Linux or a Arch Linux based distribution."
  exit
fi

# Check for yay AUR helper.
if command -v /usr/bin/yay >/dev/null 2>&1; then
  echo "Yay AUR helper is installed!"
else
  while true; do
    read -p "Yay is NOT installed! Would you like us to automatically install it for you? [Y/N] " yn
    case $yn in
        [Yy]* ) git clone https://aur.archlinux.org/yay && cd yay && makepkg -si && cd .. && rm -rf yay/; break;;
        [Nn]* ) echo "You will need to install yay manually then."; exit;;
        * ) echo "Please answer Y or N!";;
    esac
  done
fi

# Check for sudo, su -c should NOT be used since you are in a more dangerous environment than sudo.
if command -v /usr/bin/sudo >/dev/null 2>&1; then
  echo "Sudo is installed, will be used!"
else
  echo "Sudo is NOT installed, installing it with your package manager..."
  sudo pacman -S --noconfirm --needed sudo
fi

# Check if python is installed
if command -v /usr/bin/python3 >/dev/null 2>&1; then
  echo "Python 3 is installed!"
else
  echo "Python 3 is NOT installed, installing it with your package manager..."
  sudo pacman -S --noconfirm --needed python
  exit
fi

# Check if git is installed
if command -v /usr/bin/git >/dev/null 2>&1; then
  echo "Git is installed!"
else
  echo "Git is NOT installed, installing it with your package manager..."
  sudo pacman -S --noconfirm --needed git
  exit
fi

# INSTALL ################################################

echo "Installing AUR dependencies..."
yay -S --noconfirm --needed vapoursynth vapoursynth-plugin-svpflow1 vapoursynth-plugin-svpflow2-bin vapoursynth-plugin-havsfunc

echo "Finishing up..."
# Aquire sudo and automate
sudo cp ./plugins/*.py /usr/lib/python*/site-packages/
sudo curl https://github.com/couleurm/vs-frameblender/releases/download/1.2/vs-frameblender-1.2.so -o /usr/lib/vapoursynth/vs-frameblender-1.2.so

if [[ $SHELL=="/bin/bash" ]]; then
  echo "alias sm='python $PWD/smoothie.py'" >> "$HOME/.bashrc"
elif [[ $SHELL=="/usr/bin/zsh" ]]; then
  echo "alias sm='python $PWD/smoothie.py'" >> "$HOME/.zshrc"
else
  echo "Did not detect what shell you are using, please add this to your shells configuration file:"
  echo "alias sm='python $PWD/smoothie.py'"
fi

# ENDING #################################################
echo "Thank you for installing Smoothie. Please join our discord server 'discord.gg/CTT', it would mean the best to us!"
exit 1
