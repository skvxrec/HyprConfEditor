import os
import shutil
from pathlib import Path

class HyprConf:
    def __init__(self):
        self.config_path = Path.home() / ".config/hypr/hyprland.conf"
        self.backup_path = self.config_path.with_suffix('.conf.backup')

    def backup_config(self):
        """Создает бэкап конфига"""
        try:
            if self.config_path.exists():
                shutil.copy2(self.config_path, self.backup_path)
                print(f"✅ Backup created: {self.backup_path}")
                return True
            else:
                print("❌ Cfg was not found!")
                return False
        except Exception as e:
            print(f"❌ error while creating backup: {e}")
            return False

    def add_autostart(self, command):
        """Добавляет команду в автозагрузку"""
        autostart_line = f"exec-once = {command}\n"

        with open(self.config_path, 'a') as f:
            f.write(f"\n# Authostart: {command}\n")
            f.write(autostart_line)

            print(f"✅ Added to config: {command}")  # Добавили сообщение
            return True
        # except Exception as e:
        #      print(f"❌ Ошибка при создании автозагрузки: {e}")
        #      return False
            
    def add_bind(self, key_combo, command):
        #Добавляет бинд на команду
        bind_line = f"bind = {key_combo}, exec, {command}\n"

        with open(self.config_path, 'a') as f:
            f.write(f"\n# bind {key_combo} {command}\n")
            f.write(bind_line)
            
        print(f"Added to config: {key_combo} -> {command}")
        
    def interactive_mode(self):
        """Интерактивный режим"""
        print("🎛️  Hyprland Configurator")

        if not self.backup_config():
            print("Continue with out back up")

        while True:
            print("\n what do u need?")
            print("1- autostart command")
            print("2- command on bint")
            print("3-exit")

            choice = input("\nSo?(1-3) ").strip()

            if choice == '1':
                command = input("autostart: ")
                if command:
                    self.add_autostart(command)
            
            
            elif choice == '2':
               key_combo = input("bind(e.g. SUPER, Y): ").strip()
               command = input("command: ").strip()
               if key_combo and command:
                   self.add_bind(key_combo, command)

            elif choice == '3':
                print("bb twin")
                input("press enter to exit")
                break
            
            else:
                print("wdym?")


if __name__ == "__main__":
    try:
        print(" Hi twin")
        configurator = HyprConf()
        configurator.interactive_mode()
    except Exception as e:
        print(f"💥 smth wrong: {e}")
        import traceback
        traceback.print_exc()
        input("press enter")