import os
import configparser
from pathlib import Path
import argparse
import sys
from pathlib import Path

class HyprConf:
    def __init__(self):
        self.config_path = Path.home() / ".config/hypr/hyprland.conf"
        self.backup_path = self.config_path.with_suffix('.conf.backup')

    def backup_config(self):
        """Создает бэкап конфига"""
        if self.config_path.exists():
            import shutil
            shutil.copy2(self.config_path, self.backup_path)
            print(f"Бэкап создан: {self.backup_path}")

    def add_autostart(self, command):
        """Добавляет команду в автозагрузку"""
        autostart_line = f"exec-once = {command}\n"

        with open(self.config_path, 'a') as f:
            f.write(f"\n# Автозагрузка: {command}\n")
            f.write(autostart_line)
            
        print(f"Добавлен бинд: {key_combo} -> {command}")
        
    def interactive_mode(self):
        """Интерактивный режим"""
        print("🎛️  Hyprland Configurator")

        while True:
            print("\n чё те надо")
            print("1- автозапуск")
            print("2-прога на бинд")
            print("3-шоколада ")

            choice = int(input("\nНу чё те надо всё-таки (1-3) ")).strip

            if choice == 1:
                command = input("Ок автозапуск")
                if command:
                    self.add_autostart(command)
            
            elif choice == 2:
               key_combo = ("Ок бинд, какой(например SUPER, Y)").scrip()
               command = input("А какая команда то?").scrip()
               if key_combo and command:
                   self.add_bind(key_combo, command)

            elif choice == 3:
                print("Ну и иди нахуй со своим шоколадом")
                break
            
            else:
                print("Чё?")


if __name__ == "__main__":
    configurator = HyprConf()
    configurator.backup_config()
    configurator.interactive_mode()
