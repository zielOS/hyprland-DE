#!/bin/bash

echo "Installing Dot files"
cd && sudo rm -R ~/.config/
cd && mkdir ~/.config  

ln -s $HOME/.dots/hypr/ $HOME/.config/
ln -s $HOME/.dots/hypr/eww $HOME/.config/
ln -s $HOME/.dots/hypr/lazygit $HOME/.config/
ln -s $HOME/.dots/hypr/mpv $HOME/.config/
ln -s $HOME/.dots/hypr/ranger $HOME/.config/
ln -s $HOME/.dots/hypr/zsh $HOME/.config/
ln -s $HOME/.dots/hypr/.zshrc $HOME/
ln -s $HOME/.dots/hypr/gammastep $HOME/.config/
ln -s $HOME/.dots/hypr/gtklock $HOME/.config/
ln -s $HOME/.dots/hypr/ranger $HOME/.config/
ln -s $HOME/.dots/hypr/vifm $HOME/.config/
ln -s $HOME/.dots/hypr/sxiv $HOME/.config/
ln -s $HOME/.dots/electron-flags.conf $HOME/.config/
ln -s $HOME/.dots/electron13-flags.conf $HOME/.config/

echo "Setting up lunarvim"
cd && mkdir ~/.npm-global && npm config set prefix '~/.npm-global'
cd && LV_BRANCH='release-1.3/neovim-0.9' bash <(curl -s https://raw.githubusercontent.com/LunarVim/LunarVim/release-1.3/neovim-0.9/utils/installer/install.sh)
sudo rm -R $HOME/.config/lvim
ln -s $HOME/.dots/hypr/lvim ~/.config/

echo "Setting Up Systemd"
sudo systemctl set-default graphical.target 
systemctl --user enable --now wireplumber.service pipewire-pulse.socket pipewire.socket pipewire-pulse.service pipewire.service pipewire-pulse.socket pipewire.socket pipewire-pulse.service pipewire.service


curl -fsSL https://fnm.vercel.app/install | bash
zsh <(curl -s https://raw.githubusercontent.com/zap-zsh/zap/master/install.zsh)
chsh -s $(which zsh)
