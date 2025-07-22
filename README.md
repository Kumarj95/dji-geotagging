# DJI Drone Frame‑by‑Frame Georeferencing

## Overview

This project synchronises DJI drone **flight logs** (`.CSV`) ([airdata](https://airdata.com/)) with the accompanying **subtitle files** (`.SRT`) to derive per‑frame position **and** orientation (yaw, pitch, roll) for every video frame. The enriched data unlocks applications such as:

- Aerial photogrammetry
- Traffic analytics
- Surveillance and situational awareness
- Precise geo‑localisation of detected objects

DJI embeds latitude/longitude in the SRT file but omits orientation. Meanwhile, the flight log stores orientation data, yet its timestamps differ slightly from the SRT. We bridge that gap with a two‑step heuristic:

1. **Window search** – for the first SRT frame of interest, gather all log‑file rows whose locations fall within a set threshold.
2. **Gimbal‑angle match** – from that subset, choose the first row whose gimbal pitch equals the user‑specified target angle (most videos are recorded at a fixed gimbal angle).

The output is a frame‑aligned stream of position **and** orientation ready for downstream computer‑vision or GIS pipelines.

---

## Requirements

| Tool                      | Purpose                                                                  |
| ------------------------- | ------------------------------------------------------------------------ |
| **Python ≥ 3.9**          | Core scripts                                                             |
| **ExifTool** *(optional)* | Extract video frames and copy GPS/IMU metadata into the resulting images |

> **Tip** – place a sample image from the **same drone model** inside a folder named `Template/`; its metadata will serve as the blueprint for extracted frames.

All Python dependencies are listed in `environment.yml`.

---

## Quick Start

### 1 · Create and activate the environment

```bash
conda env create -f environment.yml
conda activate geotagging
```

### 2 · Arrange your data

```
Data/
├── LogFiles/
│   ├── logfile1.csv
│   └── logfile2.csv
├── SRTFiles/
│   ├── video1.srt
│   ├── video2.srt
│   ├── video3.srt
│   └── video4.srt
├── VideoFiles/
│   ├── video1.MP4
│   ├── video2.MP4
│   ├── video3.MP4
│   └── video4.MP4
├── Output/
└── Template/
    └── template_image.JPG
```

### 3 · Run the script

```bash
python src/main.py Data/LogFiles/logfile1.csv \
    --SRTDir Data/SRTFiles \
    --VideoDir Data/VideoFiles \
    --SaveFrames \
    --FrameDirectory Data/Output/logfile1_frames \
    --SaveJson \
    --JsonPath Data/Output/logfile1.json \
    --Template Data/Template/template_image.JPG
```

Need more options?

```bash
python src/main.py -h
```

---

<!-- ## Roadmap

- **Object‑projection module** – re‑project detection results from image space to world coordinates using camera intrinsics and the extrinsics produced by `src/main.py`.
- **Elevation correction** – integrate digital elevation models (DEMs) for height‑above‑ground accuracy.
 -->
Contributions and pull requests are welcome!
