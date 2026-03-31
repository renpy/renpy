FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

# Fix yarn GPG key issue by removing its repository
RUN rm -f /etc/apt/sources.list.d/yarn.list

# Install OS dependencies required by Ren'Py
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
        python3-dev \
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
        libgtk-3-0 \
        libcanberra-gtk3-module \
        adwaita-icon-theme \
        gsettings-desktop-schemas \
        libegl1 \
        libegl1-mesa-dev \
        libgl1-mesa-dri \
        libwayland-egl1 \
        wayland-protocols \
        xauth \
        x11-xserver-utils \
        libglx-mesa0 \
        libxkbcommon-dev \
        libgtk-3-dev \
        meson \
        ninja-build \
        git \
        ccache \
    && git clone --depth 1 --branch 0.2.2 https://gitlab.freedesktop.org/libdecor/libdecor.git /tmp/libdecor \
    && cd /tmp/libdecor \
    && meson setup build --buildtype release -Ddemo=false --prefix=/usr \
    && ninja -C build \
    && ninja -C build install \
    && rm -rf /tmp/libdecor

# Install uv package manager globally
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="/usr/local/bin" sh
