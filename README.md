HyprConfEditor (HCE)

HyprConfEditor (HCE) is a lightweight, terminal-based tool for managing and editing your Hyprland configuration.
It’s designed to simplify everyday tweaks — no need to manually dig through large .conf files.

Even beginners can use it: choose a category → adjust settings → save.
Fast, minimal, and fully offline.

✨ Features

📁 Automatic detection of your hyprland.conf

🖥 Monitor management

add new monitors

edit existing monitor entries

🎨 Edit appearance, workspace, and window behavior settings

💾 Automatic backup before every save

🔍 Clean parsing with RegEx (no broken configs)

🟢 Zero dependencies — works out-of-the-box with Python

📦 Installation
git clone https://github.com/skvxrec/HyprConfEditor
cd HyprConfEditor
python3 HyprConfEditor.py


If you have Python, you're good to go.

🧭 Usage

Launch HCE:

python3 HyprConfEditor.py


Select the section you want to modify (e.g., monitors).

Adjust the parameters.

Press Save — HCE will automatically create a backup and update your config.

🎯 Example: Adding a monitor

Enter something like:

DP-1 1920x1080@60 0x0 1


HCE will generate a proper monitor= line and insert it into your Hyprland config.

🗂 Project structure
HyprConfEditor/
 ├── HyprConfEditor.py   # main program
 ├── LICENSE
 └── README.md

🤝 Contributing

Issues, ideas, and PRs are welcome.
HCE is a small “indie-style” project that grows with the community.

📜 License

MIT License — feel free to use, modify, and distribute.

💬 Author

skvxrec — Linux enthusiast, coder, and creator of HCE.
