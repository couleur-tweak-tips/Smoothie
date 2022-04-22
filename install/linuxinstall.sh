#!/bin/sh
while true; do
    read -p "NOTICE: Smoothie is in early stages and has only been tested on Arch Linux, do you wish to try this script? [Y/N]" yn
    case $yn in
        [Yy]* ) continue;;
        [Nn]* ) exit;;
        * ) echo "Please answer y or n.";;
    esac
done

echo "Welcome to the Smoothie installation script!"
echo "Please make sure you have Git and Python installed."
sleep 3
echo "Please do not press any button during the installation."
echo "Checking for required packages..."
# CHECKING #########################

# Check if python is installed
if command -v /usr/bin/python3 >/dev/null 2>&1
then
  echo "Python 3 is installed!"
else
  echo "Python 3 is not installed, please install it with your package manager."
  exit
fi

# Check if git is installed
if command -v /usr/bin/git >/dev/null 2>&1
then
  echo "Git is installed!"
else
  echo "Git is not installed, please install it with your package manager."
  exit
fi

###################################################


# Aquire sudo/su and automate
if command -v /usr/bin/sudo >/dev/null 2>&1
then
  echo "Sudo is installed, will use that for prvileges!"  # POSIX compliant, works on every shell that supports this [bash, zsh and tons more]
    sudo cp ./plugins/*.py /usr/lib/python*/site-packages/ && curl https://github.com/couleurm/vs-frameblender/releases/download/1.2/vs-frameblender-1.2.so -o /usr/lib/vapoursynth/vs-frameblender-1.2.so
else
  echo "Sudo is not installed, will use su for privileges!"
  su -c 'cp ./plugins/*.py /usr/lib/python*/site-packages/ && curl https://github.com/couleurm/vs-frameblender/releases/download/1.2/vs-frameblender-1.2.so -o /usr/lib/vapoursynth/vs-frameblender-1.2.so'
fi

# ENDING #################################################
echo "Finishing up..."
echo "alias sm='python $PWD/smoothie.py'" >> $HOME/.bashrc
echo "Thank you for installing Smoothie. Please join our discord server 'discord.gg/CTT', it would mean the best to us!"
echo "We added a alias to your bashrc for quick use of smoothie."
exit
