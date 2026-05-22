FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# Fix yarn GPG key issue by removing its repository
RUN rm -f /etc/apt/sources.list.d/yarn.list

# Install OS dependencies required by Ren'Py
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        git \
        ccache \
        python3-dev \
        python3-pip \
        python3-venv \
        libassimp-dev \
        libavcodec-dev \
        libavformat-dev \
        libswresample-dev \
        libswscale-dev \
        libharfbuzz-dev \
        libfreetype6-dev \
        libfribidi-dev \
        libsdl2-dev \
        libsdl2-image-dev \
        libsdl2-gfx-dev \
        libsdl2-mixer-dev \
        libsdl2-ttf-dev \
        libjpeg-dev \
        pkg-config \
        libdecor-0-0 \
        libdecor-0-plugin-1-cairo \
        libdecor-0-plugin-1-gtk \
        libgtk-3-0 \
        libcanberra-gtk3-module \
        adwaita-icon-theme \
        gsettings-desktop-schemas \
        libegl1 \
        libegl1-mesa-dev \
        libgl1-mesa-dri \
        libwayland-egl1 \
        wayland-protocols

# Install uv package manager globally
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh

# Copy in the task scripts
COPY create.sh /usr/local/bin/
COPY start.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/create.sh /usr/local/bin/start.sh
