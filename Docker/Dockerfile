# Stage 1: build base image with prequisite packages
FROM argnctu/duckiepond:rpi-melodic

LABEL maintainer="tuanlm@greenglobal.vn"

############################ USER ###############################
# setup environment
ENV DEBIAN_FRONTEND=noninteractive
ENV SHELL=/bin/bash \
    USER=pew \
    NB_UID=1000 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

ENV HOME=/home/${USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    ${USER}

RUN echo "root:root" | chpasswd
RUN echo "${USER}:1717" | chpasswd

##################################################################################
RUN apt-get update && \
    apt-get install -y \
        whiptail \
        lua5.1 \
        alsa-utils \
        initramfs-tools \
        python3-rpi.gpio \
        python3-smbus \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y ros-${ROS_DISTRO}-realsense2-camera && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y ros-melodic-realsense2-description && \
    rm -rf /var/lib/apt/lists/*


RUN apt-get update && apt-get install -y \
    libsuitesparse-dev\
    software-properties-common \
    libusb-1.0-0-dev \
    libx11-dev \
    xorg-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    && rm -rf /var/lib/apt/lists/*

# set the version of the realsense library
ENV LIBREALSENSE_VERSION 2.50.0
RUN cd ${HOME} && git clone https://github.com/IntelRealSense/librealsense.git \
    && cd librealsense \
    && git checkout v${LIBREALSENSE_VERSION} \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make install
# RUN apt-get update
# RUN apt-get install -y librealsense
# RUN wget http://mirrors.ustc.edu.cn/archive.raspberrypi.org/debian/pool/main/r/raspi-config/raspi-config_20201108_all.deb
# RUN dpkg -i raspi-config_20201108_all.deb
# RUN apt install -fy

# ###rpi-update######
# RUN curl -L --output /usr/bin/rpi-update https://raw.githubusercontent.com/Hexxeh/rpi-update/master/rpi-update
# RUN chmod +x /usr/bin/rpi-update
# RUN rpi-update -y

####picamera########
# RUN apt-get -y dist-upgrade
# # RUN rpi-update
# # RUN BRANCH=next rpi-update
# RUN pip3 install git+https://github.com/waveform80/picamera
# RUN apt install -y python3-colorzero

# RUN
# RUN sudo -H pip3 install \
#     RPI.GPIO \
##################################################################################



##################################### setting #####################################
RUN chown -R ${USER}:${USER} ${HOME}/
RUN echo "${USER} ALL=(ALL)  ALL" > /etc/sudoers
RUN usermod -aG video argduckiepond

# setup entrypoint

USER ${USER}

WORKDIR ${HOME}
CMD ["bash"]