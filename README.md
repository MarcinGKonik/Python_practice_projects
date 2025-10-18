# FPV Drone Triangulation

This project uses the ODAS library and a sound recognition model to triangulate the position of FPV drones.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/fpv-drone-triangulation.git
    cd fpv-drone-triangulation
    ```

2.  **Initialize and update the ODAS submodule:**
    ```bash
    git submodule init
    git submodule update
    ```

3.  **Install ODAS dependencies:**
    ```bash
    sudo apt-get update
    sudo apt-get install -y libfftw3-dev libconfig-dev libasound2-dev libpulse-dev
    ```

4.  **Build the ODAS library:**
    ```bash
    cd odas
    mkdir build
    cd build
    cmake ../
    make
    cd ../..
    ```

5.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Train the sound recognition model:**
    ```bash
    python train_model.py
    ```

2.  **Process audio and triangulate the drone's position:**
    ```bash
    python process_audio.py
    ```
