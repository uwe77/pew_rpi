# Start with an ARM-compatible base image
FROM arm32v7/ubuntu:focal

# Set environment variables to non-interactive
# This avoids user interaction hanging the build
ENV DEBIAN_FRONTEND noninteractive
ENV ROS_DISTRO noetic

# Setup the ROS repository
RUN apt-get update && apt-get install -y gnupg2 lsb-release
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# Install ROS Base and rosserial packages
RUN apt-get update && apt-get install -y \
    ros-noetic-ros-base \
    ros-noetic-rosserial \
    ros-noetic-rosserial-arduino \
    ros-noetic-rosserial-python

# Install other useful tools and dependencies
RUN apt-get install -y git wget nano

# Set up the ROS environment
RUN echo "source /opt/ros/noetic/setup.bash" >> /etc/bash.bashrc

RUN apt-get update && apt-get install -y --allow-unauthenticated \
    apt-utils lsb-release build-essential apt-transport-https \
    usbutils unzip coreutils curl git sed sudo tar udev wget vim \
    automake cmake make libusb-1.0-0-dev libatlas-base-dev \
    libopenblas-dev libprotobuf-dev libleveldb-dev libsnappy-dev \
    libopencv-dev libhdf5-serial-dev libgflags-dev libgoogle-glog-dev \
    liblmdb-dev libxslt-dev libxml2-dev libgraphviz-dev protobuf-compiler \
    byacc swig3.0 graphviz gfortran \
    python3-dev python3-numpy python3-scipy python3-yaml python3-nose python3-tk python3-pip 

RUN apt-get update && apt-get install -y --allow-unauthenticated \
    python3-opencv

RUN sudo -H pip3 install --upgrade pip 
RUN sudo -H pip3 install imutils

RUN apt-get update && apt-get install -y python3-pygame
##########################################################################
# Create a new user
RUN useradd -m rosuser && \
    echo "rosuser:rosuser" | chpasswd && \
    adduser rosuser sudo && \
    echo "rosuser ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

USER rosuser
WORKDIR /home/rosuser

# Source the ROS setup for every bash session
RUN echo "source /opt/ros/noetic/setup.bash" >> .bashrc

CMD ["bash"]
