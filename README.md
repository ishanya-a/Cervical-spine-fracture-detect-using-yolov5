# Cervical Spine Fracture Detection

This project aims to detect cervical spine fractures using YOLOv5 object detection model. It utilizes the RSNA 2022 Cervical Spine Fracture Detection Challenge dataset, which consists of 2019 3D CT scans of the cervical spine area.

## Getting Started

### Prerequisites

Make sure you have the following software installed:
- [7zip](https://www.7-zip.org/)
- [Visual Studio Code](https://code.visualstudio.com/)

### Installation

1. **Extract the folder**: Use 7zip or any other extraction tool to unzip the downloaded folder.
2. **Open in VS Code**: Open Visual Studio Code and navigate to the extracted folder.
3. **Project Requirements Command**: Run the following command in your terminal to install the required Python packages:
   ```bash
   pip install flask==1.1.1 werkzeug==0.15.6 itsdangerous==2.0.1 jinja2==3.0.3 opencv-python==4.5.3.56 tensorflow==2.4.0 keras==2.4.3 pillow==8.1.0 imutils==0.5.4 pandas==1.2.1 matplotlib==3.3.4 protobuf==3.19.0 numpy==1.19.5 scikit-learn==0.24.1 torch
**Run Project Command:** Execute the following command in your terminal to run the project:
python mySite.py


Dataset
- **Source:** RSNA 2022 Cervical Spine Fracture Detection Challenge dataset
- **Description:** This dataset consists of 2019 3D CT scans of the cervical spine area. Each CT scan is made up of roughly 100 to 800 slices of varying thickness and is labeled with a binary vector of length 7. The dataset also includes a set of 81 3D segmentations that provide pixel-perfect descriptions of the vertebrae. These segmentations were used to train the YOLOv5 object detection model to locate vertebrae on the CT scan slices. Additionally, the dataset includes bounding boxes that indicate areas of interest, such as damaged areas.
