# Hindi Handwriting Generation Using Advanced Deep Learning Models

This repository contains the code and methodology for generating realistic handwritten Hindi text using advanced deep learning techniques. The project employs a **Pix2Pix model with PatchGAN** for image-to-image translation, focusing on the complexities of Hindi script, such as conjunct characters, diacritical marks, and the shirorekha (horizontal line).

## Table of Contents

-   [Introduction](#introduction)
-   [Features](#features)
-   [Dataset](#dataset)
-   [Model Architecture](#model-architecture)
-   [Evaluation Metrics](#evaluation-metrics)
-   [Results](#results)
-   [Sample Images](#sample-images)

---

## Introduction

Generating handwriting for complex scripts like Hindi is challenging due to intricate character formations and contextual dependencies. This project proposes a novel approach to Hindi handwriting generation by leveraging:

-   Conditional GANs (Pix2Pix architecture with PatchGAN discriminator).
-   A synthetic dataset generated using character-maatra combinations from the CALAM dataset.
-   Evaluation via Handwritten Text Recognition (HTR) models using **Character Accuracy Rate (CAR)** and **Word Accuracy Rate (WAR)** metrics.

![Discriminator Architecture](Images/methodology.jpeg)

---

## Features

-   Generation of realistic Hindi handwritten text from typed text.
-   Integration of shirorekha detection for precise character alignment.
-   Evaluation of handwriting quality using advanced HTR models.

---

## Dataset

### CALAM Dataset

-   Hindi words are synthesized using combinations of characters and maatraas.
-   Shirorekha (horizontal line) detection using **Hough Line Transform** ensures proper alignment of Hindi characters.
-   Filtering invalid combinations ensures a high-quality dataset.

---

## Model Architecture

### Pix2Pix with PatchGAN

-   **Generator**: A U-Net-based model transforms typed text into handwriting images.
    ![Generator Architecture](Images/gen.jpeg)
-   **Discriminator**: A PatchGAN evaluates localized patches to enhance quality and detail.
    ![Discriminator Architecture](Images/disc.jpeg)

### Evaluation Model

-   An HTR model based on CRNN architecture evaluates the legibility of generated text using:
    -   **CTC Loss** for alignment and sequence prediction.
    -   Metrics: **CAR** and **WAR**.

---

## Evaluation Metrics

-   **Character Accuracy Rate (CAR)**: Measures the accuracy of individual character generation.
    -   Formula: \( CAR = 1 - \frac{\text{Edit Distance (Character level)}}{\text{Length of Ground Truth}} \)
-   **Word Accuracy Rate (WAR)**: Evaluates word-level coherence.
    -   Formula: \( WAR = 1 - \frac{\text{Edit Distance (Word level)}}{\text{Length of Ground Truth Words}} \)

---

## Results

-   **CAR**: 23%
-   **WAR**: 0.56%
-   Highlights:
    -   Effective at capturing character nuances.
    -   Challenges remain in generating complex conjuncts and diacritical marks.

---

## Sample Images

**Input Example**:  
![Sample Input Text Image](Images/input.jpeg)  
A synthetically generated Hindi word is used as input to the Pix2Pix model. Each character and maatra is carefully selected according to Hindi grammar rules.

**Output Example**:  
![Sample Output Handwritten Image](Images/output.jpeg)  
The output demonstrates the model’s attempt to capture the subtleties of Hindi script, including ligatures and diacritical marks.

---
