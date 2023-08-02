#!/bin/bash

git clone https://aur.archlinux.org/yay-bin.git
cd yay-bin
makepkg -si && cd
yay -S hyprland-nvidia-git
yay -S hyprsome-git
yay -S pyprland
yay -S gtklock
yay -S swhkd-git
yay -S planify
yay -S papirus-folders-catppuccin-git 
yay -S catppuccin-gtk-theme-mocha 
yay -S catppuccin-cursors-mocha 
yay -S ckb-next 
yay -S insync 
yay -S picom-ftlabs-git 
yay -S brave-bin
yay -S aide
yay -S snapper 
yay -S snap-pac-grub
yay -S fnm
yay -S snapd
yay -S zoom
yay -S mullvad-vpn
yay -S zramd
yay -S nodejs-neovim
yay -S eww-x11-git
 
sudo systemctl set-default graphical.target 
systemctl --user enable --now wireplumber.service pipewire-pulse.socket pipewire.socket pipewire-pulse.service pipewire.service pipewire-pulse.socket pipewire.socket pipewire-pulse.service pipewire.service && sudo systemctl enable zramd ckb-next-daemon

echo "Setup flatpak"
flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo


echo "Setting Up Systemd"
sudo systemctl set-default graphical.target 
systemctl --user enable --now wireplumber.service pipewire-pulse.socket pipewire.socket pipewire-pulse.service pipewire.service pipewire-pulse.socket pipewire.socket pipewire-pulse.service pipewire.service

cd && mkdir ~/.npm-global && npm config set prefix '~/.npm-global' 

zsh <(curl -s https://raw.githubusercontent.com/zap-zsh/zap/master/install.zsh)
