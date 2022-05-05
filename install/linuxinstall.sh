#!/bin/bash

while true; do
  read -p "The Smoothie installation script is in early stages and only currently works for Arch Linux and its distributions, do you wish to try this script? [Y/N] " yn
  case $yn in
      [Yy]*) break;;
      [Nn]*) exit;;
      *) echo "Please answer Y/y or N/n.";;
  esac
done

# Check for pacman, in order to validate if the user is using Arch Linux.
if command -v /usr/bin/pacman >/dev/null; then
  echo "Pacman will be used for installing dependencies."
else
  echo "Pacman is NOT installed, please use Arch Linux or a Arch Linux based distribution."
  exit
fi

if command -v /usr/bin/sudo >/dev/null; then
  echo "Sudo is installed, will be used!"
  export elevate=sudo
elif command -v /usr/bin/doas >/dev/null; then
  echo "Doas is installed, will be used!"
  export elevate=doas
else
  while true; do
    read -p "No priviledge helper is installed, install sudo for use? [Y/N] " yn
    case $yn in
        [Yy]* ) su -c 'pacman -S --noconfirm --needed'; break;;
        [Nn]* ) echo "You will need to install doas/sudo manually then."; exit;;
        * ) echo "Please answer Y/y or N/n.";;
    esac
  done
fi

# Check if git is installed
if command -v /usr/bin/git >/dev/null 2>&1; then
  echo "Git is installed!"
else
  echo "Git is NOT installed, installing it with your package manager..."
  $elevated pacman -S --noconfirm --needed git
  exit
fi

# Check for yay AUR helper.
if command -v /usr/bin/yay >/dev/null; then
  echo "Yay AUR helper is installed!"
else
  while true; do
    read -p "Yay is NOT installed! Would you like us to automatically install it for you? [Y/N] " yn
    case $yn in
        [Yy]* ) git clone https://aur.archlinux.org/yay && cd yay && makepkg -si --noconfirm --needed && cd .. && rm -rf yay/; break;;
        [Nn]* ) echo "You will need to install yay manually then."; exit;;
        * ) echo "Please answer Y/y or N/n.";;
    esac
  done
fi



# Check if python is installed
if command -v /usr/bin/python3 >/dev/null 2>&1; then
  echo "Python 3 is installed!"
else
  echo "Python 3 is NOT installed, installing it with your package manager..."
  $elevate pacman -S --noconfirm --needed python
  exit
fi


# INSTALL ################################################

echo "Installing AUR dependencies..."
yay -S --noconfirm --needed vapoursynth vapoursynth-plugin-svpflow1 vapoursynth-plugin-svpflow2-bin vapoursynth-plugin-havsfunc

echo "Finishing up..."
# Aquire sudo and automate
$elevate cp ../plugins/*.py /usr/lib/python3*/site-packages/
$elevate curl https://github.com/couleurm/vs-frameblender/releases/download/1.2/vs-frameblender-1.2.so -o /usr/lib/vapoursynth/vs-frameblender-1.2.so

if [[ $SHELL == "/bin/bash" ]]; then
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

echo "Thank you for installing Smoothie. Please join our discord server 'discord.gg/CTT', it would mean the best to us!"
echo "The command is 'sm', make sure to reopen your terminal or sign out and log into your bash session for the command to apply."
exit
