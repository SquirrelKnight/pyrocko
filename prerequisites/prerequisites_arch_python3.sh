#!/bin/bash

sudo pacman -Syu --noconfirm --needed \
    git make gcc patch python python-setuptools python-pip python-wheel \
    python-numpy python-scipy python-matplotlib \
    python-pyqt5 qt5-webengine qt5-svg qt5-webkit \
    python-cairo python-progressbar \
    python-requests python-yaml python-jinja \
    python-nose python-coverage
