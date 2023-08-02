# █ █▀▄▀█ █▀█ █▀█ █▀█ ▀█▀ █▀
# █ █░▀░█ █▀▀ █▄█ █▀▄ ░█░ ▄█

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.command import lazy
import os
import subprocess

#################################################################################
#################################################################################





# ▄▀█ █░█ ▀█▀ █▀█ █▀ ▀█▀ ▄▀█ █▀█ ▀█▀
# █▀█ █▄█ ░█░ █▄█ ▄█ ░█░ █▀█ █▀▄ ░█░

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.local/bin/qstart'])

#################################################################################
#################################################################################





# █▄▀ █▀▀ █▄█ █▀
# █░█ ██▄ ░█░ ▄█

# Variables:
mod = "mod4"
alt = "mod1"
ctrl = "control"


# Scripts
home = os.path.expanduser('~')
terminal = home + '/.local/bin/qterm'
volume = home + '/.local/bin/qvolume'
launcher = home + '/.local/bin/qmenu'
screenshot = home + '/.local/bin/qscreenshot'
browser = 'brave'
gui_file_manager = 'thunar'
gui_editor = 'emacsclient -c -a emacs'
tui_editor = 'kitty -e lvim'
tui_file_manager = 'kitty -e ranger'
notify_cmd = 'dunstify -u low -h string:x-dunst-stack-tag:qtileconfig'

keys = [
    # Launcher ---------------------
    Key([mod], "d", lazy.spawn(launcher)),

    # Control qtile ---------------
    Key([mod, ctrl], "r",
        lazy.reload_config(),
        lazy.spawn(notify_cmd + ' "Configuration Reloaded!"')),

    Key([mod, ctrl], "s",
        lazy.restart(),
        lazy.spawn(notify_cmd + ' "Restarting Qtile..."')),

    Key([mod, ctrl], "q",
        lazy.shutdown(),
        lazy.spawn(notify_cmd + ' "Exiting Qtile..."')),


    # Terminal -------------
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod, "shift"], "Return", lazy.spawn(terminal + ' --float')),
    Key([mod, alt], "Return", lazy.spawn(terminal + ' --full')),

    # Kill window ---------------
    Key([mod], "q", lazy.window.kill()),

    # Switch focus --------------------
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),


    # Move windows -----------------------------------
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),


    # Resize windows
    Key([mod, ctrl], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete()),

    Key([mod, ctrl], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add()),

    Key([mod, ctrl], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster()),

    Key([mod, ctrl], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster()),


    # Toggle floating & fullscreen ----------------------
    Key([mod], "space", lazy.window.toggle_floating()),\
    Key([mod], "f", lazy.window.toggle_fullscreen()),


    # Control volume ----------------------------
    Key([], "XF86AudioRaiseVolume", lazy.spawn(volume + ' --up')),
    Key([], "XF86AudioLowerVolume", lazy.spawn(volume + ' --down')),
    Key([], "XF86AudioMute", lazy.spawn(volume + ' --toggle')),


    # Screenshot
    Key([], "Print", lazy.spawn(screenshot + ' --full')),
    Key([mod], "Print", lazy.spawn(screenshot + ' --crop')),


    # Gui apps ----------
    KeyChord([mod], "g", [
        Key([], "b", lazy.spawn(browser),
            desc="Launch web browser"),

        Key([], "f", lazy.spawn(gui_file_manager),
            desc="Launch file-manager"),

        Key([], "e", lazy.spawn(gui_editor),
            desc="Launch emacs"),
    ]),


    # Tui apps ----------------------
    KeyChord([mod], "t", [
        Key([], "l", lazy.spawn(tui_editor),
            desc="Launch lvim"),

        Key([], "r", lazy.spawn(tui_file_manager),
            desc="Launch ranger"),
    ])
]

#################################################################################
#################################################################################





# █▀▀ █▀█ █▀█ █░█ █▀█ █▀
# █▄█ █▀▄ █▄█ █▄█ █▀▀ ▄█

NUM_SCREENS = 3
NUM_GROUPS = 8
GROUP_MAP = {}
GROUP_LIST = []

# Here we create two objects:
# 1) A dict, "GROUP_MAP", which has a key relating to the screen index. The value is another dict
#    where groups are numbered from 1 to NUM_GROUPS. The value is a unique group name.
# 2) A list of all groups. Each group has a unique name but the label is between 1 and NUM_GROUPS
for screen in range(NUM_SCREENS):
    screen_dict = {}
    for group in range(NUM_GROUPS):
        name = f"{screen * NUM_GROUPS + group}"
        group_num = group + 1
        screen_dict[group_num] = name
        GROUP_LIST.append(Group(name, label=str(group_num)))
    GROUP_MAP[screen] = screen_dict

@lazy.function
def switch_group(qtile, group_num):
    """
    This function looks up the unique group name for group number on the current screen
    and then displays that group.
    """
    group_name = GROUP_MAP[qtile.current_screen.index + 1][group_num]
    qtile.groups_map[group_name].toscreen()


@lazy.window.function
def move_window_to_group(window, group_num, switch_group=False, toggle=False):
    """
    This function looks up the unique group name for group number on the current screen
    and then moves the window to that group.
    """   
    group_name = GROUP_MAP[window.qtile.current_screen.index + 1][group_num]
    window.togroup(group_name, switch_group, toggle)

# Groups should be set to our group list
groups = GROUP_LIST

# We bind keys mod + 1-8 to call our function to display a group depending on the focused screen
# mod + shift + 1-8 moves window to that group on the active screen
for i in range(NUM_GROUPS):
    keys.append(Key([mod], str(i + 1), switch_group(i + 1)))
    keys.append(Key([mod, "shift"], str(i + 1), move_window_to_group(i + 1, switch_group=True)))

# mod + control + 1-3 moves window to current group on that screen
for i in range(NUM_SCREENS):
    keys.append(Key([mod, "control"], str(i + 1), lazy.window.toscreen(i)))

###################################################################################################
###################################################################################################





# █░░ ▄▀█ █▄█ █▀█ █░█ ▀█▀ █▀
# █▄▄ █▀█ ░█░ █▄█ █▄█ ░█░ ▄█


## Layouts ------------------------------
var_bg_color = '#2e3440'
var_active_bg_color = '#81A1C1'
var_active_fg_color = '#2e3440'
var_inactive_bg_color = '#3d4555'
var_inactive_fg_color = '#D8DEE9'
var_urgent_bg_color = '#BF616A'
var_urgent_fg_color = '#D8DEE9'
var_section_fg_color = '#EBCB8B'
var_active_color = '#81A1C1'
var_normal_color = '#3d4555'
var_border_width = 2
var_margin = [5,5,5,5]
var_gap_top = 45
var_gap_bottom = 5
var_gap_left = 5
var_gap_right = 5
var_font_name = 'JetBrainsMono Nerd Font'

layouts = [

	# Emulate the behavior of XMonad's ThreeColumns layout.
    layout.MonadThreeCol(
		align=0,
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		change_ratio=0.05,
		change_size=20,
		main_centered=True,
		margin=0,
		max_ratio=0.75,
		min_ratio=0.25,
		min_secondary_size=85,
		new_client_position='top',
		ratio=0.5,
		single_border_width=None,
		single_margin=None    
    ),
	# Layout inspired by bspwm
    layout.Bsp(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_on_single=False,
		border_width=var_border_width,
		fair=True,
		grow_amount=10,
		lower_right=True,
		margin=var_margin,
		margin_on_single=None,
		ratio=1.6,
		wrap_clients=False
    ),

	# This layout divides the screen into a matrix of equally sized cells and places one window in each cell.
    layout.Matrix(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,    
		columns=2,
		margin=var_margin
    ),

	# Maximized layout
    layout.Max(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,    
		margin=0
    ),

	# Emulate the behavior of XMonad's default tiling scheme.
    layout.MonadTall(
		align=0,
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		change_ratio=0.05,
		change_size=20,
		margin=0,
		max_ratio=0.75,
		min_ratio=0.25,
		min_secondary_size=85,
		new_client_position='after_current',
		ratio=0.5,
		single_border_width=None,
		single_margin=None
    ),

	# Emulate the behavior of XMonad's horizontal tiling scheme.
    layout.MonadWide(
		align=0,
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		change_ratio=0.05,
		change_size=20,
		margin=0,
		max_ratio=0.75,
		min_ratio=0.25,
		min_secondary_size=85,
		new_client_position='after_current',
		ratio=0.5,
		single_border_width=None,
		single_margin=None    
    ),

	# Tries to tile all windows in the width/height ratio passed in
    layout.RatioTile(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		fancy=False,
		margin=var_margin,
		ratio=1.618,
		ratio_increment=0.1
    ),

	# This layout cuts piece of screen_rect and places a single window on that piece, and delegates other window placement to other layout
    layout.Slice(
		match=None,
		side='left',
		width=256
    ),

	# A mathematical layout, Renders windows in a spiral form by splitting the screen based on a selected ratio.
    layout.Spiral(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		clockwise=True,
		main_pane='left',
		main_pane_ratio=None,
		margin=0,
		new_client_position='top',
		ratio=0.6180469715698392,
		ratio_increment=0.1
    ),
    
	# A layout composed of stacks of windows
    layout.Stack(
		autosplit=False,
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		fair=False,
		margin=var_margin,
		num_stacks=2
    ),

	# A layout with two stacks of windows dividing the screen
    layout.Tile(
		add_after_last=False,
		add_on_top=True,
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_on_single=False,
		border_width=var_border_width,
		expand=True,
		margin=var_margin,
		margin_on_single=None,
		master_length=1,
		master_match=None,
		max_ratio=0.85,
		min_ratio=0.15,
		ratio=0.618,
		ratio_increment=0.05,
		shift_windows=False
    ),

	# This layout works just like Max but displays tree of the windows at the left border of the screen_rect, which allows you to overview all opened windows.
    layout.TreeTab(
		active_bg=var_active_bg_color,
		active_fg=var_active_fg_color,
		bg_color=var_bg_color,
		border_width=var_border_width,
		font=var_font_name,
		fontshadow=None,
		fontsize=14,
		inactive_bg=var_inactive_bg_color,
		inactive_fg=var_inactive_fg_color,
		level_shift=0,
		margin_left=0,
		margin_y=0,
		padding_left=10,
		padding_x=10,
		padding_y=10,
		panel_width=200,
		place_right=False,
		previous_on_rm=False,
		section_bottom=0,
		section_fg=var_section_fg_color,
		section_fontsize=14,
		section_left=10,
		section_padding=10,
		section_top=10,
		sections=['Default'],
		urgent_bg=var_urgent_bg_color,
		urgent_fg=var_urgent_fg_color,
		vspace=5
    ),

	# Tiling layout that works nice on vertically mounted monitors
    layout.VerticalTile(
		border_focus=var_active_color,
		border_normal=var_normal_color,
		border_width=var_border_width,
		margin=var_margin
    ),

	# A layout with single active windows, and few other previews at the right
    layout.Zoomy(
		columnwidth=300,
		margin=var_margin,
		property_big='1.0',
		property_name='ZOOM',
		property_small='0.1'
    )
]

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])

###################################################################################################
###################################################################################################





# █▀ █▀▀ █▀█ █▀▀ █▀▀ █▄░█ █▀
# ▄█ █▄▄ █▀▄ ██▄ ██▄ █░▀█ ▄█

widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
            widget.Spacer(
                length=15,
                background='#282738'),

            widget.Image(
                filename='~/.config/qtile/Assets/launch_Icon.png',
                margin=2,
                background='#282738',
                mouse_callbacks={"Button1":"power"}),

            widget.Image(
                filename='~/.config/qtile/Assets/6.png'),


            widget.GroupBox(
                fontsize=24,
                borderwidth=3,
                highlight_method='block',
                active='#CAA9E0',
                block_highlight_text_color="#91B1F0",
                highlight_color='#4B427E',
                inactive='#282738',
                foreground='#4B427E',
                background='#353446',
                this_current_screen_border='#353446',
                this_screen_border='#353446',
                other_current_screen_border='#353446',
                other_screen_border='#353446',
                urgent_border='#353446',
                rounded=True,
                disable_drag=True),

            widget.Spacer(
                length=8,
                background='#353446'),


            widget.Image(
                filename='~/.config/qtile/Assets/1.png'),


            widget.Image(
                filename='~/.config/qtile/Assets/layout.png',
                background="#353446"),

            widget.CurrentLayout(
                background='#353446',
                foreground='#CAA9E0',
                fmt='{}',
                font="JetBrains Mono Bold",
                fontsize=13),


            widget.Image(
                filename='~/.config/qtile/Assets/5.png'),


            widget.Image(
                filename='~/.config/qtile/Assets/search.png',
                margin=2,
                background='#282738',
                mouse_callbacks={"Button1": search}),

            widget.TextBox(
                fmt='Search',
                background='#282738',
                font="JetBrains Mono Bold",
                fontsize=13,
                foreground='#CAA9E0',
                mouse_callbacks={"Button1": search}),


            widget.Image(
                filename='~/.config/qtile/Assets/4.png'),


            widget.WindowName(
                background = '#353446',
                format = "{name}",
                font='JetBrains Mono Bold',
                foreground='#CAA9E0',
                empty_group_string = 'Desktop',
                fontsize=13),


            widget.Image(
                filename='~/.config/qtile/Assets/3.png'),


            widget.Systray(
                background='#282738',
                fontsize=2),


            widget.TextBox(
                text=' ',
                background='#282738'),


            widget.Image(
                filename='~/.config/qtile/Assets/6.png',
                background='#353446'),

            widget.Image(
                filename='~/.config/qtile/Assets/Misc/ram.png',
                background='#353446'),


            widget.Spacer(
                length=-7,
                background='#353446'),


            widget.Memory(
                background='#353446',
                format='{MemUsed: .0f}{mm}',
                foreground='#CAA9E0',
                font="JetBrains Mono Bold",
                fontsize=13,
                update_interval=5),

            widget.Image(
                filename='~/.config/qtile/Assets/2.png'),


            widget.Spacer(
                length=8,
                background='#353446'),


            widget.BatteryIcon(
                theme_path='~/.config/qtile/Assets/Battery/',
                background='#353446',
                scale=1),

            widget.Battery(
                font='JetBrains Mono Bold',
                background='#353446',
                foreground='#CAA9E0',
                format='{percent:2.0%}',
                fontsize=13),

            widget.Image(
                filename='~/.config/qtile/Assets/2.png'),

            widget.Spacer(
                length=8,
                background='#353446'),

            widget.Volume(
                font='JetBrainsMono Nerd Font',
                theme_path='~/.config/qtile/Assets/Volume/',
                emoji=True,
                fontsize=13,
                background='#353446'),

            widget.Spacer(
                length=-5,
                background='#353446'),

            widget.Volume(
                font='JetBrains Mono Bold',
                background='#353446',
                foreground='#CAA9E0',
                fontsize=13,
            ),

            widget.Image(
                filename='~/.config/qtile/Assets/5.png',
                background='#353446',
            ),

            widget.Image(
                filename='~/.config/qtile/Assets/Misc/clock.png',
                background='#282738',
                margin_y=6,
                margin_x=5),

            widget.Clock(
                format='%I:%M %p',
                background='#282738',
                foreground='#CAA9E0',
                font="JetBrains Mono Bold",
                fontsize=13),

            widget.Spacer(
                length=18,
                background='#282738'),
    
    ]

    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

#######################################################################################
#######################################################################################





# █▀▄▀█ █▀█ █░█ █▀ █▀▀
# █░▀░█ █▄█ █▄█ ▄█ ██▄

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

######################################################################################
######################################################################################





# █▀▄▀█ █ █▀ █▀▀
# █░▀░█ █ ▄█ █▄▄

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

#######################################################################################
#######################################################################################
