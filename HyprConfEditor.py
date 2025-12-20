import os
import shutil
from pathlib import Path
import subprocess
import re

class HyprConf:
    def __init__(self):
        self.config_path = Path.home() / ".config/hypr/hyprland.conf"
        self.backup_path = self.config_path.with_suffix('.conf.backup')
        self.hyprpaper_config = Path.home() / ".config/hypr/hyprpaper.conf"
        self.fish_path = Path.home() / ".config/fish/config.fish"
    
    def backup_config(self):
        """Creates config backup"""
        try:
            if self.config_path.exists():
                shutil.copy2(self.config_path, self.backup_path)
                print(f"✅ Backup created: {self.backup_path}")
                return True
            else:
                print("❌ Config file not found!")
                return False
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False

    def check_hyprland_config(self):
        """Checks if hyprland config exists"""
        if not self.config_path.exists():
            print("❌ Hyprland config not found!")
            print(f"Expected path: {self.config_path}")
            return False
        return True
    
    def check_fish_conf(self):
    #"""Checks if fish config exists"""
        if not self.fish_path.exists():
            print("❌ Fish config not found!")
            print(f"Expected path: {self.config_path}")
            return False
        return True

    def check_hyprpaper_config(self):
        """Checks if hyprpaper config exists and asks to create if not"""
        if not self.hyprpaper_config.exists():
            print("❌ Hyprpaper config not found!")
            choice = input("Create new hyprpaper config? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                # Create directory if needed
                self.hyprpaper_config.parent.mkdir(parents=True, exist_ok=True)
                # Create basic hyprpaper config
                with open(self.hyprpaper_config, 'w') as f:
                    f.write("# Hyprpaper config created by HyprConfEditor\n")
                print("✅ Created new hyprpaper config")
                return True
            else:
                print("⚠️  Returning to menu...")
                return False
        return True

    def add_autostart(self, command):
        """Adds command to autostart"""
        if not self.check_hyprland_config():
            return False
            
        autostart_line = f"exec-once = {command}\n"

        with open(self.config_path, 'a') as f:
            f.write(f"\n# Autostart: {command}\n")
            f.write(autostart_line)

        print(f"✅ Added to config: {command}")
        return True
            
    def add_bind(self, key_combo, command):
        """Adds keybind for command"""
        if not self.check_hyprland_config():
            return False
            
        bind_line = f"bind = {key_combo}, exec, {command}\n"

        with open(self.config_path, 'a') as f:
            f.write(f"\n# Bind {key_combo} {command}\n")
            f.write(bind_line)
            
        print(f"✅ Added to config: {key_combo} -> {command}")
        return True
        
    def set_wallpaper(self, wallpaper_path, monitor="all"):
        """Sets wallpaper in hyprpaper"""
        if not self.check_hyprpaper_config():
            return False
            
        try:
            # Check if wallpaper file exists
            if not os.path.exists(wallpaper_path):
                print(f"❌ Wallpaper file not found: {wallpaper_path}")
                return False
            
            wallpaper_path = os.path.abspath(wallpaper_path)

            # Read current hyprpaper config
            with open(self.hyprpaper_config, 'r') as f:
                lines = f.readlines()

            # Find existing wallpaper settings
            new_lines = []
            
            for line in lines:
                # Remove old wallpaper settings for this monitor
                if monitor == "all" and (
                line.strip().startswith("wallpaper") or 
                line.strip().startswith("preload")
                ):
                    continue
                elif monitor != "all" and line.strip().startswith(f"wallpaper,{monitor},") and line.strip().startswith(f"preload"):
                    continue
                else:
                    new_lines.append(line)
            
            # Add wallpaper setting
            if monitor == "all":
                new_lines.append(f"preload = {wallpaper_path}\n")
                new_lines.append(f"wallpaper = ,{wallpaper_path}\n")
            else:
                new_lines.append(f"preload = {wallpaper_path}\n")
                new_lines.append(f"wallpaper = {monitor},{wallpaper_path}\n")
            
            # Write updated config
            with open(self.hyprpaper_config, 'w') as f:
                f.writelines(new_lines)
            
            print(f"✅ Wallpaper set: {wallpaper_path}")
            
            # Reload hyprpaper
            self.reload_hyprpaper()
            return True
            
        except Exception as e:
            print(f"❌ Error setting wallpaper: {e}")
            return False
    
    def reload_hyprpaper(self):
        """Reloads hyprpaper"""
        try:
            subprocess.run(["pkill", "hyprpaper"], capture_output=True)
            subprocess.Popen(["hyprpaper"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("✅ Hyprpaper reloaded")
            return True
        except Exception as e:
            print(f"⚠️  Failed to reload hyprpaper: {e}")
            return False
    
    def list_monitors(self):
        """Gets monitor list via hyprctl"""
        try:
            result = subprocess.run(
                ["hyprctl", "monitors"], 
                capture_output=True, 
                text=True
            )
            monitors = []
            for line in result.stdout.split('\n'):
                match = re.search(r'Monitor\s+([^\s]+)\s*\(', line)
                if match:
                    monitors.append(match.group(1))
            return monitors
        except Exception as e:
            print(f"❌ Failed to get monitor list: {e}")
            return ["all"]

    def add_monitor_interactive(self):
        """Interactive monitor addition"""
        name = input("Monitor name (e.g., HDMI-A-1, DP-1): ").strip()
        resolution = input("Resolution (e.g., 1920x1080): ").strip()
        refresh_rate = input("Refresh rate (e.g., 144): ").strip()
        position = input("Position (e.g., 0x0): ").strip()
        
        # Validate inputs
        if not name or not resolution or not refresh_rate or not position:
            print("❌ All fields are required!")
            return False
        
        # Call confirmation method
        return self.monitor_add_request(name, resolution, refresh_rate, position)

    def monitor_add_command(self, name, resolution, refresh_rate, position):
        """Adds monitor line to config"""
        if not self.check_hyprland_config():
            return False

        monitor_line = f"monitor = {name}, {resolution}@{refresh_rate}, {position}, 1"
        print(f"📺 Adding monitor: {monitor_line}")
        
        try:
            with open(self.config_path, 'a') as f:
                f.write(f"\n# Monitor added via HCE\n")
                f.write(f"{monitor_line}\n")
            print("✅ Monitor configuration added successfully!")
            return True
        except Exception as e:
            print(f"❌ Error writing to config: {e}")
            return False

    def monitor_add_request(self, name, resolution, refresh_rate, position):
        """Confirmation before adding monitor"""
        monitor_line = f"monitor = {name}, {resolution}@{refresh_rate}, {position}, 1"
        
        while True:
            ynm = input(f"\n{monitor_line}\nIs this correct? (y/n): ").strip().lower()
            
            if ynm == 'y':
                return self.monitor_add_command(name, resolution, refresh_rate, position)
            elif ynm == 'n':
                print("↩️  Let's try again...")
                return self.add_monitor_interactive()
            else:
                print("❓ Please enter 'y' or 'n'")

    def fishalias(self):
        old_command = input("old command: ")
        new_command = input("new command: ")
        falias_line = f'alias {new_command}="{old_command}"'
        return self.fishalias_request(old_command, new_command, falias_line)


    def fishalias_write(self, old_command, new_command, falias_line):
        if not self.check_fish_conf():
            return False

        print(f"adding alias {falias_line}")
        try:
            with open(self.fish_path, 'a') as f:
                f.write("\n# Alias added via HCE\n")
                f.write(f"{falias_line}\n")
            print("✅ Alias added successfully!")
            return True
        except Exception as e:
            print(f"❌ Error writing to config: {e}")
            return False

        
    def fishalias_request(self, old_command, new_command, falias_line):
        while True:
            ynfa = input(f"{falias_line}, correct? (y/n): ").lower()

            if ynfa == 'y':
                return self.fishalias_write(old_command, new_command, falias_line)
            elif ynfa == 'n':
                print("↩️  Let's try again...")
                return self.fishalias()
            else:
                print("❓ Please enter 'y' or 'n'")



    def interactive_mode(self):
        """Interactive mode"""
        print("🎛️  Hyprland Configurator")

        if not self.check_hyprland_config():
            print("❌ Cannot continue without hyprland config")
            input("Press Enter to exit")
            return

        if not self.backup_config():
            print("⚠️  Continuing without backup")

        while True:
            print("\nWhat do you need twin?")
            print("1 - Add autostart command")
            print("2 - Add keybind")
            print("3 - Set wallpaper")
            print("4 - Add monitor")
            print("5 - Add alias to fish")
            print("6 - Exit")

            choice = input("\nSo? (1-5): ").strip()

            if choice == '1':
                command = input("Autostart command: ")
                if command:
                    self.add_autostart(command)
            
            elif choice == '2':
                key_combo = input("Keybind (e.g. SUPER, Y): ").strip()
                command = input("Command: ").strip()
                if key_combo and command:
                    self.add_bind(key_combo, command)

            elif choice == '3':
                wallpaper_path = input("Wallpaper path: ").strip()
                if wallpaper_path:
                    monitors = self.list_monitors()
                    if len(monitors) > 1:
                        print("Available monitors:")
                        for i, monitor in enumerate(monitors):
                            print(f"  {i} - {monitor}")
                        print(f"  {len(monitors)} - All monitors")
                        
                        monitor_choice = input("Choose monitor: ").strip()
                        try:
                            if int(monitor_choice) == len(monitors):
                                monitor = "all"
                            else:
                                monitor = monitors[int(monitor_choice)]
                        except:
                            monitor = "all"
                            print("⚠️  Using all monitors")
                    else:
                        monitor = "all"
                    
                    self.set_wallpaper(wallpaper_path, monitor)
            
            elif choice == '4':
                self.add_monitor_interactive()

            elif choice == '5':
                self.fishalias()
        
            elif choice == '6':
                print("BB twin 👋")
                input("Press Enter to exit")
                break
            
            else:
                print("❓ Wdym? Choose 1-5")


if __name__ == "__main__":
    try:
        print("Hi twin! 🚀")
        configurator = HyprConf()
        configurator.interactive_mode()
    except Exception as e:
        print(f"💥 Something went wrong: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter")
