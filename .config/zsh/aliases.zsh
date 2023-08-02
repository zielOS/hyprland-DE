#!/bin/sh

# git aliases
alias cl='git clone'
alias g='lazygit'

# zsh aliases
alias zsh-update="find "$ZDOTDIR/plugins" -type d -exec test -e '{}/.git' ';' -print0 | xargs -I {} -0 git -C {} pull -q"
alias f='zi'

# Pacman-related alias
alias em-syncn='sudo emerge --ask --verbose --update --newuse --deep @world --jobs=10'
alias em-syncc='sudo emerge --ask --quiet --update --changed-use --deep @world --jobs=10'
alias em-install='sudo emerge -av --jobs=5'
alias em-remove='sudo emerge -pv --depclean'
alias em-search='sudo emerge --search | sudo emerge --searchdesc'
alias pac-clean='sudo eclean-dist --deep | sudo emerge --depclean'
alias use='sudo lvim /etc/portage/package.use'

# scripts-related aliases
# alias hyprbar='sudo lvim /usr/local/bin/hyprbar'
# alias hyprhotkeys='sudo lvim /usr/local/bin/hyprhotkeys'
# alias hypridle='sudo lvim /usr/local/bin/hypridle'
# alias hyprkeyring='sudo lvim /usr/local/bin/hyprkeyring'
# alias hyprland-nvidia='sudo lvim /usr/local/bin/hyprland-nvidia'
# alias hyprlock='sudo lvim /usr/local/bin/hyprlock'
# alias hyprlogout='sudo lvim /usr/local/bin/hyprlogout'
# alias hyprmenu='sudo lvim /usr/local/bin/hyprmenu'
# alias hyprpolkit='sudo lvim /usr/local/bin/hyprpolkit'
# alias hyprshot='sudo lvim /usr/local/bin/hyprshot'
# alias hyprsome='sudo lvim /usr/local/bin/hyprsome'
# alias hyprstart='sudo lvim /usr/local/bin/hyprstart'
# alias hyprterm='sudo lvim /usr/local/bin/hyprterm'
# alias hyprtheme='sudo lvim /usr/local/bin/hyprtheme'
# alias hyprwall='sudo lvim /usr/local/bin/hyprwall'


# makepkg-related aliases
# alias mkpkg='makepkg -si  --noconfirm'
# alias mkpkg-conf='makepkg -si --noconfirm --config $HOME/.config/makepkg/makepkg.conf'

# Misc-related aliases
alias audit='sudo lynis audit system'
alias update-grub='sudo grub-mkconfig -o /boot/grub/grub.cfg'
alias grub-conf='sudo lvim /etc/default/grub'
alias Rm='sudo rm -rf'
# alias htkey-load='sudo pkill -HUP swhkd'
alias emacs_stop='emacsclient -e "(kill-emacs)"'
alias snapper='sudo lvim /etc/snapper/configs/root'
alias aa-status='sudo aa-status'

if [[ $TERM == "xterm-kitty" ]]; then
  alias ssh="kitty +kitten ssh"
fi

case "$(uname -s)" in

Darwin)
	# echo 'Mac OS X'
	alias ls='ls -G'
	;;

Linux)
	alias ls='ls --color=auto'
	;;

CYGWIN* | MINGW32* | MSYS* | MINGW*)
	# echo 'MS Windows'
	;;
*)
	# echo 'Other OS'
	;;
esac
