<div align="center">

# 🧬 Anti-Viral Drug Design

### Using Model-Based Reinforcement Learning and Generative Models

*An AI-driven pipeline that generates, optimizes, and validates candidate antiviral molecules in silico.*

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Deep Learning](https://img.shields.io/badge/Deep%20Learning-VAE%20%7C%20GNN-orange)
![Reinforcement Learning](https://img.shields.io/badge/RL-PPO%20%7C%20DQN%20%7C%20A2C-green)
![Domain](https://img.shields.io/badge/Domain-Drug%20Discovery-blueviolet)
![Status](https://img.shields.io/badge/Status-Research%20Project-informational)

</div>

---

## 📖 Overview

Traditional antiviral drug discovery relies on high-throughput screening and trial-and-error experimentation, which is slow, expensive, and struggles to keep pace with rapidly mutating viruses. Most computational approaches use *either* generative models for molecule design *or* reinforcement learning (RL) for optimization, without a unified framework that balances multiple drug properties at once.

This project proposes a **hybrid framework** that combines:

- **Generative models** (Variational Autoencoder, with Graph Neural Network support) to create novel, drug-like molecular structures from SMILES representations
- **Model-based reinforcement learning** to iteratively optimize the generated molecules
- **An adaptive, multi-objective reward function** balancing binding affinity, drug-likeness, toxicity, and ADMET properties
- **Deep learning–based binding affinity prediction** to score candidates against viral targets
- **Validation and filtering** using Tanimoto similarity analysis and molecular simulation-based screening

> This work is limited to virtual (in silico) experiments. Generated candidates require further experimental validation before any therapeutic claims can be made.

---

## 🔬 Pipeline

```
┌──────────────────┐   ┌────────────────────┐   ┌──────────────────────────┐
│ 1. Data          │──▶│ 2. Molecular       │──▶│ 3. RL Optimization       │
│ Collection &     │   │ Generation         │   │ (reward-guided,          │
│ Preprocessing    │   │ (VAE / GNN)        │   │ model-based)             │
└──────────────────┘   └────────────────────┘   └────────────┬─────────────┘
                                                             │
┌──────────────────┐   ┌────────────────────┐   ┌────────────▼─────────────┐
│ 6. Final         │◀──│ 5. Validation &    │◀──│ 4. Binding Affinity      │
│ Candidate        │   │ Similarity Analysis│   │ Prediction (Deep         │
│ Selection        │   │ (Tanimoto)         │   │ Learning)                │
└──────────────────┘   └────────────────────┘   └──────────────────────────┘
```

| Stage | Description |
|-------|-------------|
| **Data preprocessing** | Antiviral peptide/molecular data curated and encoded (SMILES-style sequence representations) |
| **Molecular generation** | A VAE learns a latent space of drug-like structures and samples novel candidates |
| **RL optimization** | Agents refine generated molecules using a reward signal; PPO, A2C, and DQN were compared |
| **Adaptive reward** | Rewards structural novelty, binding affinity, drug-likeness, toxicity, and ADMET properties |
| **Binding affinity prediction** | Deep learning predictor estimates drug–target binding strength |
| **Validation & filtering** | Tanimoto similarity to known antivirals and property-based filtering remove weak candidates |

---

## 📊 Dataset

**[AVPdb](http://crdd.osdd.net/servers/avpdb/)** is a manually curated database of experimentally validated antiviral peptides:

- **2,683** experimentally validated antiviral peptides (including **624** modified peptides)
- Targets roughly **60** medically important viruses
- Includes sequences, source organisms, target viruses, cell lines, assay types, and efficacy data

The dataset was **balanced across target viruses** to prevent the models from overfitting to dominant classes (e.g., HIV, HCV). Peptide lengths cluster mainly around 15–20 and 35–40 residues.

> Qureshi A. et al., *AVPdb: a database of experimentally validated antiviral peptides targeting medically important viruses*, Nucleic Acids Research, 42(D1), D1147–D1153, 2014.

---

## 📈 Results

### Reinforcement Learning Comparison

| Algorithm | Behavior | Approx. peak accuracy |
|-----------|----------|----------------------|
| **DQN** | Stable, consistent improvement; best overall | > 0.55 |
| **PPO** | Large reward gain, from about −400 to positive | ~ 0.50 |
| **A2C** | Little to no reward gain; poor convergence in this setup | ~ 0.38 |

DQN and PPO were identified as the more suitable choices for optimizing molecular candidates in this framework.

### Model Training

- **VAE:** training loss decreases steadily over 50 epochs and stabilizes, indicating a well-structured latent space for sampling new candidates.
- **Binding affinity model:** MSE loss drops from about 0.0875 to about 0.083 and plateaus after roughly 10 epochs.

### Molecular Similarity

The average Tanimoto similarity between generated and reference antivirals is **0.6412**, meaning generated molecules stay moderately similar to known antivirals (preserving drug-like features) while still allowing novel variation.

### Candidate Evaluation

Top candidates are ranked by a composite score combining binding affinity, similarity to known antivirals, and target affinity. Each is also checked against:

- Molecular weight (MW), LogP, H-bond donors/acceptors (HBD/HBA)
- Topological polar surface area (TPSA) and rotatable bonds
- Lipinski rule violations and ADMET score

Candidates target viruses including **Hepatitis C, Influenza A, HIV, and SARS-CoV-2**.

### Interactive Classification Demo

A lightweight web interface (**AntiViral Drug Classification**) accepts a peptide sequence, source organism, and family, then predicts the target virus with a confidence score. For example, a VAE-generated sequence was classified with **92.57%** probability.

---

## 🗂️ Repository Structure

```
Anti-Viral-Drug-Design/
├── Antiviral Drug Design/   # Project code, notebooks, and data/artifacts
├── README.md
└── (LICENSE, requirements.txt: recommended additions)
```

> Open the `Antiviral Drug Design/` folder for the implementation files.

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.9+
- A machine with at least 4 GB RAM (a GPU is recommended for training)

### Installation

```bash
git clone https://github.com/Siddhartha80/Anti-Viral-Drug-Design.git
cd Anti-Viral-Drug-Design

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Usage

```bash
cd "Antiviral Drug Design"
jupyter notebook                # open and run the notebooks in order
```

---

## 🛠️ Tech Stack

- **Language:** Python
- **Deep learning:** PyTorch / TensorFlow (VAE, GNN, binding affinity predictor)
- **Reinforcement learning:** PPO, A2C, DQN
- **Cheminformatics:** RDKit (SMILES handling, Tanimoto similarity, descriptors)
- **Data & visualization:** NumPy, Pandas, Matplotlib, Seaborn
- **Demo UI:** Streamlit-style web interface

---

## 🚀 Future Work

- Larger and more diverse datasets
- Advanced protein structure prediction tools
- Enhanced adaptive reward functions
- Exploration of hybrid generative architectures
- Expanded validation pipeline and cloud deployment
- Explainability framework integration
- Experimental testing with bioinformatics and pharmacology experts

---

## 📚 Publication

This repository accompanies the paper:

> **Anti-Viral Drug Design Using Model-Based RL and Generative Models**
> Poli Vamsi Vardhan Reddy, Vempalli Surya, M Ramya Sree, Santhanalakshmi S, Mettu Siddhartha
> Department of Computer Science and Engineering, Amrita School of Computing, Bengaluru, Amrita Vishwa Vidyapeetham, India

### Citation

```bibtex
@inproceedings{reddy2025antiviral,
  title     = {Anti-Viral Drug Design Using Model-Based RL and Generative Models},
  author    = {Reddy, Poli Vamsi Vardhan and Surya, Vempalli and Sree, M Ramya and
               Santhanalakshmi, S and Siddhartha, Mettu},
  institution = {Amrita Vishwa Vidyapeetham, Bengaluru, India},
  year      = {2025}
}
```

*(Update the venue and year once the publication details are final.)*

---

## 👥 Authors

| Name | Role |
|------|------|
| Poli Vamsi Vardhan Reddy | Author |
| Vempalli Surya | Author |
| M Ramya Sree | Author |
| Santhanalakshmi S | Faculty guide |
| [Mettu Siddhartha](https://github.com/Siddhartha80) | Author |

---

## 📬 Contact

**Mettu Siddhartha** · [LinkedIn](https://linkedin.com/in/siddhartha-mettu/) · [GitHub](https://github.com/Siddhartha80) · smettu12@asu.edu

---

## ⚠️ Disclaimer

This project is for research and educational purposes only. All results come from computational simulations; none of the generated molecules have been experimentally validated or should be used for medical purposes.

---

<div align="center">

⭐ If you find this project useful, consider giving it a star!

</div>
