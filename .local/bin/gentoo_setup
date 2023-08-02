*** BTRFS
cfdisk /dev/nvme0n1 && mkfs.vfat -F 32 /dev/nvme0n1p1 && cryptsetup -c aes-xts-plain64 -s 512 -y luksFormat /dev/nvme0n1p2 && cryptsetup luksOpen /dev/nvme0n1p2 cryptroot && mkfs.btrfs /dev/mapper/cryptroot && mkdir /mnt/gentoo && mount /dev/mapper/cryptroot /mnt/gentoo && btrfs subvolume create /mnt/gentoo/@ && btrfs subvolume create /mnt/gentoo/@/.snapshots && mkdir /mnt/gentoo/@/.snapshots/1 && btrfs subvolume create /mnt/gentoo/@/.snapshots/1/snapshot && mkdir -p /mnt/gentoo/@/boot/grub2/ && btrfs subvolume create /mnt/gentoo/@/boot/grub2/i386-pc && btrfs subvolume create /mnt/gentoo/@/boot/grub2/x86_64-efi && btrfs subvolume create /mnt/gentoo/@/home && btrfs subvolume create /mnt/gentoo/@/opt && btrfs subvolume create /mnt/gentoo/@/root && btrfs subvolume create /mnt/gentoo/@/srv && btrfs subvolume create /mnt/gentoo/@/tmp && mkdir /mnt/gentoo/@/usr/ && btrfs subvolume create /mnt/gentoo/@/usr/local && btrfs subvolume create /mnt/gentoo/@/var && btrfs subvolume create /mnt/gentoo/@/var/log && btrfs subvolume create /mnt/gentoo/@/var/log/audit && chattr +c /mnt/gentoo/@/var && nvim /mnt/gentoo/@/.snapshots/1/info.xml

<?xml version="1.0"?>
<snapshot>
  <type>single</type>
  <num>1</num>
  <date>$DATE</date>
  <description>first root filesystem</description>
</snapshot>

btrfs subvolume set-default $(btrfs subvolume list /mnt/gentoo | grep "@/.snapshots/1/snapshot" | grep -oP '(?<=ID )[0-9]+') /mnt/gentoo && umount /mnt/gentoo 

mkdir /mnt/gentoo/.snapshots && mkdir -p /mnt/gentoo/boot/grub2/i386-pc && mkdir -p /mnt/gentoo/boot/grub2/x86_64-efi && mkdir /mnt/gentoo/home && mkdir /mnt/gentoo/opt && mkdir /mnt/gentoo/srv && mkdir /mnt/gentoo/tmp && mkdir -p /mnt/gentoo/usr/local && mkdir -p /mnt/gentoo/var/log/audit

mount /dev/mapper/cryptroot /mnt/gentoo -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@ && mount /dev/mapper/cryptroot /mnt/gentoo/.snapshots -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/.snapshots && mount /dev/mapper/cryptroot /mnt/gentoo/boot/grub2/i386-pc -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/boot/grub2/i386-pc && mount /dev/mapper/cryptroot /mnt/gentoo/boot/grub2/x86_64-efi -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/boot/grub2/x86_64-efi && mount /dev/mapper/cryptroot /mnt/gentoo/home -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/home && mount /dev/mapper/cryptroot /mnt/gentoo/opt -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/opt &&  mount /dev/mapper/cryptroot /mnt/gentoo/root -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/root && mount /dev/mapper/cryptroot /mnt/gentoo/srv -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/srv && mount /dev/mapper/cryptroot /mnt/gentoo/tmp -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/tmp && mount /dev/mapper/cryptroot /mnt/gentoo/usr/local -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/usr/local && mount /dev/mapper/cryptroot /mnt/gentoo/var -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/var && mount /dev/mapper/cryptroot /mnt/gentoo/var/log -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/var/log &&  mount /dev/mapper/cryptroot /mnt/gentoo/var/log/audit -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/var/log/audit  
 

* Download gentoo

cd /mnt/gentoo && wget https://distfiles.gentoo.org/releases/amd64/autobuilds/20230723T170155Z/stage3-amd64-hardened-openrc-20230723T170155Z.tar.xz && tar xpvf stage3-*.tar.xz --xattrs-include='*.*' --numeric-owner


*** make.conf
rm -R /mnt/gentoo/etc/portage/make.conf && nano -w /mnt/gentoo/etc/portage/make.conf

# These settings were set by the catalyst build script that automatically
# built this stage.
# Please consult /usr/share/portage/config/make.conf.example for a more
# detailed example.
#NTHREADS="22"
#source /etc/portage/make.conf.lto
COMMON_FLAGS="-march=native -O3 -pipe"
CPU_FLAGS_X86="aes avx avx2 f16c fma3 mmx mmxext pclmul popcnt rdrand sha sse sse2 sse3 sse4_1 sse4_2 ssse3"
CFLAGS="${COMMON_FLAGS}"
CXXFLAGS="${COMMON_FLAGS}"
FCFLAGS="${COMMON_FLAGS}"
FFLAGS="${COMMON_FLAGS}"
RUSTFLAGS="-C opt-level=3 -C target-cpu=native"
MAKEOPTS="-j22"
NOCOMMON_OVERRIDE_LIBTOOL="yes"
ACCEPT_KEYWORDS="~amd64"
ACCEPT_LICENSE="*"
VIDEO_CARDS="nvidia intel"
USE="-elogind systemd -gnome -berkdb -kde -ccache -tpm zstd policykit \
      clamav -coreaudio -ios -ipod -ieee1394 -motif gtk pulseaudio qt5 qt6 \
      -emboss -3dfx -altivec -smartcard -ibm -wayland -nls -nas pam clang  \
      -neon -nntp -cups -quicktime nvidia sound-server -vim apparmor \
      pie gui X upower hardened udev alsa audit dbus tiff jpeg lto pgo \
      -accessibility -bluetooth -handbook"
#RUBY_TARGETS="ruby24 ruby25"
# NOTE: This stage was built with the bindist Use flag enabled
PORTDIR="/var/db/repos/gentoo"
DISTDIR="/var/cache/distfiles"
PKGDIR="/var/cache/binpkgs"

# This sets the language of build output to English.
# Please keep this setting intact when reporting bugs.
LC_MESSAGES=C
GRUB_PLATFORMS="efi-64"



**** keywords
rm -R /mnt/gentoo/etc/portage/package.accept_keywords && nano -w /mnt/gentoo/etc/portage/package.accept_keywords

=app-backup/grub-btrfs-9999 ** ~amd64
=x11-misc/picom-9999 ** ~amd64
=x11-wm/qtile-9999 ** ~amd64
=x11-misc/sxhkd-9999 ** ~amd64
=x11-misc/ly-9999 ** ~amd64
=gui-apps/eww-9999 ** ~amd64
=x11-misc/jgmenu-9999 ** ~amd64
=media-sound/pamixer-9999 ** ~amd64

nano -w /mnt/gentoo/etc/portage/profile/use.mask
-lto
-gmp-autoupdate

mkdir -p /mnt/gentoo/etc/portage/profile/ && nano -w /mnt/gentoo/etc/portage/profile/package.provided

sys-kernel/gentoo-sources-6.4.7
app-text/texlive-9999
app-text/texlive-core-9999
dev-tex/latexdiff-9999
dev-texlive/texlive-basic-9999
dev-texlive/texlive-fontsextra-9999
dev-texlive/texlive-fontsrecommended-9999
dev-texlive/texlive-fontutils-9999
dev-texlive/texlive-formatsextra-9999
dev-texlive/texlive-latex-9999
dev-texlive/texlive-latexextra-9999
dev-texlive/texlive-latexrecommended-9999
dev-texlive/texlive-luatex-9999
dev-texlive/texlive-mathscience-9999
dev-texlive/texlive-plaingeneric-9999
dev-texlive/texlive-pstricks-9999
dev-texlive/texlive-xetex-9999
dev-tex/tex4ht-999999999999
virtual/latex-base-1.0
virtual/tex-base-9999

rm -R /mnt/gentoo/etc/portage/package.use && nano -w /mnt/gentoo/etc/portage/package.use

*/* PYTHON_TARGETS: python3_11
app-editors/neovim lto
net-libs/nodejs lto npm 
dev-lang/rust clippy miri rust-analyzer rustfmt system-llvm rust-src
net-p2p/transmission -gtk qt5 qt6
sys-config/ltoize keep-nocommon clang
dev-util/cmake -emacs ncurses -qt5
media-fonts/iosevka X iosevka-aile
app-text/xmlto text
gnome-base/gvfs udisks
dev-libs/libdbusmenu gtk3
app-crypt/gcr gtk
sys-apps/kmod zstd
sys-boot/grub:2 device-mapper
app-admin/sysstat lto lm-sensors
sys-libs/zlib minizip
app-text/poppler cairo
dev-lang/python lto pgo ensurepip tk hardened
sys-devel/gcc lto pgo graphite jit default-stack-clash-protection
sys-apps/firejail apparmor private-home
app-editors/emacs alsa dynamic-loading gfile gmp -gtk gui gzip-el harfbuzz imagemagick inotify jit jpeg motif png ssl svg threads tiff tree-sitter zlib 
app-text/ghostscript-gpl cups
dev-python/PyQt5 widgets
media-sound/pulseaudio -daemon
media-video/pipewire sound-server
sys-apps/kmod tools
sys-apps/xdg-desktop-portal -screencast -geolocation
sys-apps/systemd policykit
media-sound/mpg123 -pulseaudio
media-libs/libpng apng
dev-qt/qtgui eglfs egl dbus
sys-libs/gdbm berkdb
dev-qt/qtwidgets dbus
dev-qt/qtbase opengl egl eglfs gles2-only
dev-qt/qtdeclarative opengl
dev-libs/boost context
dev-libs/boehm-gc cxx
virtual/libcrypt static-libs
sys-libs/libxcrypt static-libs
media-fonts/nerd-fonts jetbrainsmono firacode ubuntu
gui-libs/gtk-layer-shell introspection
net-wireless/wpa_supplicant dbus
net-libs/libssh server
sys-config/ltoize clang
sys-apps/flatpak policykit seccomp
app-admin/keepassxc browser autotype keeshare network yubikey
dev-python/PyQt5 opengl
dev-python/pillow webp
dev-python/QtPy svg printsupport
dev-python/PyQt5 network svg sql printsupport
app-crypt/gnupg nls
app-office/libreoffice branding googledrive gtk gstreamer
dev-libs/boost nls
dev-libs/xmlsec nss
sys-auth/polkit gtk daemon
net-analyzer/snort threads
app-portage/eix optimization strong-security tools
media-gfx/sxiv exif gif jpeg png webp
app-misc/fdupes ncurses
dev-libs/libpcre2 pcre32
dev-qt/qtcore icu
media-libs/libvpx postproc
x11-base/xorg-server xvfb
gui-libs/wlroots tinywl
x11-drivers/nvidia-drivers modules modules-sign
kde-plasma/plasma-meta browser-integration -colord -crash-handler crypt desktop-portal -discover -display-manager -firewall -grub gtk -kwallet -legacy-systray -plymouth -sddm -sdk -smart thunderbolt -wallpapers
kde-apps/okular djvu epub markdown pdf tiff
#lxqt-base/lxqt-meta about -admin archiver desktop-portal -display-manager -filemanager -lximage minimal -nls policykit powermanagement -processviewer -screenshot -sddm -ssh-askpass -sudo -terminal -trash
www-client/firefox X clang dbus geckodriver gmp-autoupdate hardened hwaccel jumbo-build lto openh264 pgo pulseaudio -telemetry -wayland -debug -eme-free jack -libproxy screencast 


rm -R /mnt/gentoo/etc/portage/package.mask && nano -w /mnt/gentoo/etc/portage/package.mask

>=dev-lang/python-12
x11-libs/gtk+::mv
>=sys-devel/gcc-13
>=sys-kernel/gentoo-sources-6.2
>=sys-kernel/linux-headers-6.2

* setup fstab and chroot

mount /dev/nvme0n1p1 /mnt/gentoo/boot && genfstab -U /mnt/gentoo >> /mnt/gentoo/etc/fstab && mkdir --parents /mnt/gentoo/etc/portage/repos.conf && cp /mnt/gentoo/usr/share/portage/config/repos.conf /mnt/gentoo/etc/portage/repos.conf/gentoo.conf && cp --dereference /etc/resolv.conf /mnt/gentoo/etc/ && mount --types proc /proc /mnt/gentoo/proc && mount --rbind /sys /mnt/gentoo/sys && mount --make-rslave /mnt/gentoo/sys && mount --rbind /dev /mnt/gentoo/dev && mount --make-rslave /mnt/gentoo/dev && mount --bind /run /mnt/gentoo/run && mount --make-slave /mnt/gentoo/run && test -L /dev/shm && rm /dev/shm && mkdir /dev/shm && mount -t tmpfs -o nosuid,nodev,noexec shm /dev/shm && chmod 1777 /dev/shm

* chroot-into
chroot /mnt/gentoo /bin/bash
source /etc/profile
export PS1="(chroot) ${PS1}"

emerge-webrsync && emerge --sync && emerge -aq app-eselect/eselect-repository dev-vcs/git --jobs=10 && eselect repository remove gentoo && eselect repository add gentoo git https://github.com/gentoo-mirror/gentoo.git  && emaint sync -r gentoo && eselect repository enable guru lto-overlay mv src_prepare-overlay && emerge --sync && emerge -aq ltoize lto-rebuild --jobs=10 && lto-rebuild -r

* gcc upgrade
emerge -aq sys-devel/gcc && eselect gcc list && eselect gcc set 2 && lto-rebuild -r && emerge --ask --oneshot --usepkg=n sys-devel/libtool && emerge -eq --usepkg=n @world --jobs=10 --keep-going --exclude gcc


* gcc downgrade
revdep-rebuild --library 'libstdc++.so.6' -- --exclude gcc && emerge --ask --oneshot --usepkg=n --verbose sys-devel/libtool


** Systemd
ln -sf ../usr/share/zoneinfo/Canada/Mountain /etc/localtime && nano -w /etc/locale.gen && locale-gen && eselect locale list && eselect locale set 4 && env-update && source /etc/profile && export PS1="(chroot) ${PS1}" && systemd-firstboot --prompt --setup-machine-id 

* initial-packages
emerge --sync && emerge -auvDN @world

* kernel setup
emerge -aq sys-kernel/xanmod-sources sys-fs/genfstab  sys-kernel/linux-firmware sys-kernel/linux-headers sys-kernel/genkernel sys-apps/fwupd sys-fs/cryptsetup sys-firmware/intel-microcode --jobs=10 && eselect kernel set 1 && ls -l /usr/src/linux 

genfstab -U / >> /etc/fstab

genkernel --luks --menuconfig --install all


** miscellenous apps
grub-install --target=x86_64-efi --efi-directory=/boot && grub-install --target=x86_64-efi --efi-directory=/boot --removable && grub-mkconfig -o /boot/grub/grub.cfg

emerge -av --jobs=10  app-arch/unzip app-arch/zip app-arch/unrar sys-fs/btrfs-progs sys-fs/dosfstools net-misc/wget net-misc/curl app-misc/ckb app-admin/sudo app-text/zathura app-text/zathura-meta dev-python/pynvim app-editors/neovim sys-apps/ripgrep dev-util/tree-sitter-cli sys-apps/fd app-shells/zsh app-shells/zsh-completions app-shells/gentoo-zsh-completions app-shells/zoxide app-shells/fzf dev-vcs/lazygit x11-misc/rofi x11-misc/dunst app-forensics/aide sys-apps/rng-tools sys-apps/haveged app-forensics/lynis sys-process/audit app-admin/sysstat sys-process/acct sys-boot/grub sys-apps/mlocate app-misc/tmux x11-themes/papirus-icon-theme x11-misc/jgmenu app-portage/smart-live-rebuild app-portage/gentoolkit media-fonts/nerd-fonts net-im/discord app-text/xournalpp sys-power/power-profiles-daemon app-admin/stow x11-terms/kitty x11-terms/kitty-terminfo x11-terms/kitty-shell-integration app-misc/ranger app-misc/vifm sys-apps/apparmor sys-apps/apparmor-utils sys-libs/libapparmor sec-policy/apparmor-profiles media-sound/pamixer sci-misc/jupyterlab-desktop-bin net-im/zoom app-misc/tealdeer sys-apps/grep x11-wm/qtile kde-misc/krusader app-admin/keepassxc sci-chemistry/pymol kde-plasma/plasma-meta kde-frameworks/krunner kde-apps/ark media-video/vlc kde-apps/spectacle kde-apps/gwenview kde-apps/dolphin kde-apps/kdepim-meta gui-apps/wl-clipboard dev-python/pywlroots x11-base/xwayland x11-libs/libdrm media-libs/libglvnd x11-libs/libxcb media-libs/mesa x11-apps/mesa-progs gui-libs/egl-wayland x11-drivers/nvidia-drivers 




** custom ebuilds 9999
x11-wm/bspwm
x11-misc/sxhkd
x11-misc/picom
x11-misc/jgmenu
media-fonts/nerd-fonts not 9999
gui-apps/eww

passwd && useradd -m -G users,wheel,audio,video,cron -s /bin/bash ahsan && passwd ahsan && EDITOR=nvim visudo

grub-install --target=x86_64-efi --efi-directory=/boot && grub-install --target=x86_64-efi --efi-directory=/boot --removable && grub-mkconfig -o /boot/grub/grub.cfg

nvim /etc/default/grub
:w
GRUB_CMDLINE_LINUX="quiet crypt_root=UUID=6d16f447-973d-49e6-b01d-c6938c732d2e root_trim=yes init=/lib/systemd/systemd"
GRUB_CMDLINE_LINUX_DEFAULT="apparmor=1 security=apparmor nvidia-drm.modeset=1" 

# Setup systemd
systemd-firstboot --prompt --setup-machine-id && systemctl enable NetworkManager fstrim.timer power-profiles-daemon systemd-timesyncd sysstat apparmor auditd nvidia-hibernate.service nvidia-suspend.service nvidia-resume.service nvidia-powerd.service



nvim /etc/modprobe.d/nvidia.conf
options nvidia-drm modeset=1 
options nvidia NVreg_UsePageAttributeTable=1


nvim /etc/modprobe.d/nvidia-power-management.conf
options nvidia NVreg_PreserveVideoMemoryAllocations=1 NVreg_TemporaryFilePath=/tmp


** Snapper setup

sudo umount /.snapshots && sudo rm -r /.snapshots && sudo snapper -c root create-config / && sudo btrfs subvolume delete /.snapshots && sudo mkdir /.snapshots && sudo mount -a && sudo chmod 750 /.snapshots && sudo snapper -c root create-config / && sudo nvim /etc/snapper/configs/root && sudo chmod a+rx /.snapshots/ && sudo systemclt enable snapper-timeline.timer snapper-cleanup.timer grub-btrfs.path 

 -- WARNING -- This system is for the use of authorized users only. Individuals 
 using this computer system without authority or in excess of their authority 
 are subject to having all their activities on this system monitored and 
 recorded by system personnel. Anyone using this system expressly consents to 
 such monitoring and is advised that if such monitoring reveals possible 
 evidence of criminal activity system personal may provide the evidence of such 
 monitoring to law enforcement officials.

#scaling apps
--force-device-scale-factor=1.75 %U

#setup snapper
sudo umount /.snapshots/ && sudo rm -r /.snapshots/ && sudo snapper -c root create-config / && sudo btrfs subvolume delete /.snapshots && sudo mkdir /.snapshots && sudo mount -a && sudo chmod 750 /.snapshots && sudo lvim /etc/snapper/configs/root && sudo systemctl enable --now snapper-timeline.timer && sudo systemctl enable --now snapper-cleanup.timer && yay -S snap-pac-grub snapper-gui

#ivpn installation

  install -Dm755 -g root -o root References/Linux/scripts/_out_bin/ivpn-service "/usr/bin/ivpn-service" && install -Dm700 -g root -o root References/Linux/etc/client.down "/opt/ivpn/etc/client.down" && install -Dm700 -g root -o root References/Linux/etc/client.up "/opt/ivpn/etc/client.up" && install -Dm700 -g root -o root References/Linux/etc/firewall.sh "/opt/ivpn/etc/firewall.sh" && install -Dm700 -g root -o root References/Linux/etc/splittun.sh "/opt/ivpn/etc/splittun.sh" && install -Dm600 -g root -o root References/common/etc/servers.json "/opt/ivpn/etc/servers.json" && install -Dm400 -g root -o root References/common/etc/ca.crt "/opt/ivpn/etc/ca.crt" && install -Dm400 -g root -o root References/common/etc/ta.key "/opt/ivpn/etc/ta.key" && install -Dm755 -g root -o root References/Linux/_deps/wireguard-tools_inst/wg-quick "/opt/ivpn/wireguard-tools/wg-quick" && install -Dm755 -g root -o root References/Linux/_deps/wireguard-tools_inst/wg "/opt/ivpn/wireguard-tools/wg" && install -Dm755 -g root -o root References/Linux/_deps/obfs4proxy_inst/obfs4proxy "$pkgdir/opt/ivpn/obfsproxy/obfs4proxy" && install -Dm755 -g root -o root References/Linux/_deps/dnscryptproxy_inst/dnscrypt-proxy "/opt/ivpn/dnscrypt-proxy/dnscrypt-proxy" && install -Dm400 -g root -o root References/common/etc/dnscrypt-proxy-template.toml "/opt/ivpn/etc/dnscrypt-proxy-template.toml"

sudo lvim /usr/share/gvfs/mounts/network.mount
AutoMount=false

nvim /etc/sysctl.d/harden.conf
kernel.core_pattern=|/bin/false
fs.suid_dumpable=0 
dev.tty.ldisc_autoload=0
fs.protected_fifos=2
fs.protected_regular=2
kernel.kptr_restrict=2
kernel.perf_event_paranoid=3
kernel.sysrq=0
kernel.unprivileged_bpf_disabled=1
kernel.unprivileged_userns_clone=0
net.core.bpf_jit_harden=2
net.ipv4.conf.all.accept_redirects=0
net.ipv4.conf.all.log_martians=1
net.ipv4.conf.all.rp_filter=1
net.ipv4.conf.all.send_redirects=0
net.ipv4.conf.default.accept_redirects=0
net.ipv4.conf.default.log_martians=1
net.ipv6.conf.all.accept_redirects=0
net.ipv6.conf.default.accept_redirects=0


# Emacs packages
use-package no-littering general which-key evil-surround evil-commentary evil-quickscope evil-numbers evil-lion avy ace-link transpose-frame smartparens expand-region visual-fill-column projectile counsel-projectile magit forge git-gutter git-timemachine editorconfig deadgrep counsel swiper ivy-rich ivy-prescient helpful wakatime-mode request activity-watch-mode olivetti keycast doom-themes auto-dim-other-buffers ligature all-the-icons highlight-indent-guides rainbow-delimiters rainbow-mode hl-todo doom-modeline perspective treemacs lsp-mode lsp-treemacs flycheck tree-sitter tree-sitter-langs dap-mode copilot emmet-mode prettier  typescript-mode app-emacs/tex markdown-mode plantuml-mode subed langtool lispy lispyville hy-mode ein jedhy lsp-pyright yapf  yapfify black isort py-isort sphinx-doc pytest  code-cells  json-mode csv-mode yaml-mode dotenv-mode gitignore-templates dockerfile-mode jenkinsfile-mode crontab-mode doc-view org org-contrib  evil-org app-emacs/jupyter ob-hy f  restclient ob-restclient ob-jupyter ob-async org-present hide-mode-line org-make-toc org-attach-screenshot org-transclusion edraw-org


# Sample Systemd Service
[Unit]
Description=

[Service]
ExecStart=

[Install]
WantedBy=multi-user.target    


 
# Post-install chroot
cryptsetup luksOpen /dev/nvme0n1p2 cryptroot && mount /dev/mapper/cryptroot /mnt/gentoo -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@ && mount /dev/mapper/cryptroot /mnt/gentoo/.snapshots -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/.snapshots && mount /dev/mapper/cryptroot /mnt/gentoo/boot/grub2/i386-pc -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/boot/grub2/i386-pc && mount /dev/mapper/cryptroot /mnt/gentoo/boot/grub2/x86_64-efi -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/boot/grub2/x86_64-efi && mount /dev/mapper/cryptroot /mnt/gentoo/home -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/home && mount /dev/mapper/cryptroot /mnt/gentoo/opt -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/opt && mount /dev/mapper/cryptroot /mnt/gentoo/srv -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/srv && mount /dev/mapper/cryptroot /mnt/gentoo/tmp -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/tmp && mount /dev/mapper/cryptroot /mnt/gentoo/usr/local -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/usr/local && mount /dev/mapper/cryptroot /mnt/gentoo/var -o noatime,compress=zstd,space_cache=v2,discard=async,subvol=@/var && cd /mnt/gentoo && mkdir --parents /mnt/gentoo/etc/portage/repos.conf && cp /mnt/gentoo/usr/share/portage/config/repos.conf /mnt/gentoo/etc/portage/repos.conf/gentoo.conf && cp --dereference /etc/resolv.conf /mnt/gentoo/etc/ && mount --types proc /proc /mnt/gentoo/proc && mount --rbind /sys /mnt/gentoo/sys && mount --make-rslave /mnt/gentoo/sys && mount --rbind /dev /mnt/gentoo/dev && mount --make-rslave /mnt/gentoo/dev && mount --bind /run /mnt/gentoo/run && mount --make-slave /mnt/gentoo/run && test -L /dev/shm && rm /dev/shm && mkdir /dev/shm && mount -t tmpfs -o nosuid,nodev,noexec shm /dev/shm && chmod 1777 /dev/shm

chroot /mnt/gentoo /bin/bash
source /etc/profile
export PS1="(chroot) ${PS1}"


