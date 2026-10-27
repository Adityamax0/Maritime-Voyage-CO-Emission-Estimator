# 🚢 Maritime Voyage CO₂ Emission Estimator

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Pipeline-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end Machine Learning pipeline and interactive web interface to predict Scope 1 greenhouse gas ($CO_2$) emissions for short-haul commercial maritime operations. 

Trained on operational voyage data, this project models physical interactions between vessel deadweight types, meteorological resistance, propulsion fuel types, and route distances to deliver accurate emission estimates without relying on direct fuel consumption shortcuts.

---

## 📌 Table of Contents
- [Problem Overview](#-problem-overview)
- [Key Features](#-key-features)
- [Model Architecture & Metrics](#-model-architecture--metrics)
- [Dataset Characteristics](#-dataset-characteristics)
- [Project Structure](#-project-structure)
- [Local Setup & Installation](#-local-setup--installation)
- [Interactive Application](#-interactive-application)
- [Deployment](#-deployment)
- [License](#-license)

---

## 🌊 Problem Overview

Maritime shipping contributes roughly 3% of global anthropogenic greenhouse gas emissions. For maritime logistics providers, charterers, and port authorities, estimating Scope 1 emissions prior to departure is essential for fuel bunkering strategies, ESG compliance, and green corridor planning.

Traditional regression often relies on fuel consumption as an input; however, actual fuel consumption is unknown prior to a voyage. This system estimates emissions **ex-ante** using operational specifications:
* **Vessel Classification** (Displacement profile)
* **Meteorological State** (Wave resistance and drag)
* **Fuel Grade** (Carbon intensity per unit mass)
* **Transit Distance & Engine Thermal Efficiency**

---

## ⚡ Key Features

* **Production-Grade Sklearn Pipeline:** Encapsulates `ColumnTransformer` with `OneHotEncoder(drop='first', handle_unknown='ignore')` and `RandomForestRegressor`, eliminating train-test data leakage and categorical encoding mismatches.
* **Calibrated Operational Bounds:** Enforces strict domain validation ($20\text{ nm} - 500\text{ nm}$) to prevent decision-tree extrapolation errors on unseen voyage lengths.
* **Streamlit UI:** Provides an interactive interface featuring instant $CO_2$ forecasts and fuel burn intensity metrics ($\text{MT} / \text{nm}$).
* **Zero Dependency Persistence:** Serialized into a single production `.pkl` pipeline artifact for clean separation between model logic and web application code.

---

## 📊 Model Architecture & Metrics

* **Algorithm:** Random Forest Regressor (`n_estimators=100`, `max_depth=12`, `random_state=42`)
* **Preprocessing:** `scikit-learn` `ColumnTransformer` (categorical one-hot encoding + numerical passthrough)

### Validation Performance (20% Unseen Test Set)

| Metric | Score | Physical Significance |
| :--- | :--- | :--- |
| **$R^2$ Score** | **0.9411** | Explains $>94\%$ of the variance in vessel $CO_2$ emissions |
| **Mean Absolute Error (MAE)** | **1,989.23 MT** | Average prediction deviation across short-haul operational voyages |
| **Root Mean Squared Error (RMSE)** | **3,498.00 MT** | Penalizes high-displacement tanker variance |

### Feature Importance Drivers
1. **Voyage Distance:** $\approx 94\%$ relative contribution (