# Prosthetic-MI-BCI  

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](#)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#LICENSE)  
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](#)  

A toggle-based motor-imagery BCI pipeline for prosthetic grasp control.  
Collect EEG, train a subject-specific classifier, and run inference on an embedded device—all in one repo.  

---

## 🚀 Table of Contents

1. [Features](#features)  
2. [Architecture](#architecture)  
3. [Quick Start](#quick-start)  
4. [Usage](#usage)  
5. [Diagram](#bci-pipeline-flow-diagram)  
6. [Configuration](#configuration)  
7. [Contributing](#contributing)  
8. [License](#license)  

---

## ✨ Features

- **Offline collection**: grab 5–8 min of EEG, segment into epochs.  
- **Online calibration**: real-time feedback with threshold adaptation.  
- **Embedded inference**: run lightweight LDA or quantized MLP on Raspberry Pi Zero/Coral/MCU.  
- **Toggle FSM**: single mental “hit” flips hand open/close state.  
- **Extensible**: add new commands, build new front-ends, swap hardware interfaces.  

---

## 🏗 Architecture

1. **collect** – record & save raw/epoched EEG (BIDS-EEG HDF5 or FIF)  
2. **train**   – fine-tune classifier & threshold with live feedback  
3. **export**  – serialize model ( `.pkl` / `.tflite` ) + metadata  
4. **infer**   – embedded runtime loads model, runs sliding-window toggle logic  

---

## 🚀 Quick Start

1. **Clone**  
   ```bash
   git clone https://github.com/fletchere171/Prosthetic-MI-BCI.git
   cd Prosthetic-MI-BCI
