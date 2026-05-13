#!/bin/bash
sudo usermod -a -G video,render vscode || true
sudo chown -R vscode:vscode /home/vscode/.cache /home/vscode/.ccache tmp
uv sync || true
echo 'source ~/.venv-renpy/bin/activate' >> ~/.bashrc
source ~/.venv-renpy/bin/activate
./run.sh --build
