# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-02
### Added
- **Project Organization**: Created dedicated directories for better structure:
  - `models/`: Stores serialized model artifacts (`.pkl`).
  - `data/`: Stores the dataset (`.xlsx`).
  - `docs/`: Added original project documentation ("Proyecto - Apoyo a la Toma de Decisiones.pdf").
  - `notebooks/`: Stores the original training notebook (`.ipynb`) for audit and observation purposes.
- Added `CHANGELOG.md` to track project history.

### Changed
- **Refactor (`app.py`)**: Updated the main application to load resources dynamically using `os.path.join`, improving compatibility across operating systems.
- **Documentation (`README.md`)**: Updated the "Project Structure" section to reflect the new folder organization (`docs/`, `models/`, etc.) and file locations.
- **File Management**: Moved `Datos_Entrenamiento_Final.xlsx`, `modelo_perrito.pkl`, `columnas_modelo.pkl`, `traductor_respuestas.pkl`, and `Perrito.ipynb` from the root to their respective new directories.

## [0.1.0] - 2025-12-10
### Added
- [cite_start]Initial release of **DSS "El Sabueso"** for the "Sistemas de Apoyo a la Toma de Decisiones" course[cite: 2, 3].
- [cite_start]Predictive model trained with Scikit-learn (Decision Tree Classifier)[cite: 368].
- [cite_start]Interactive web interface built with Streamlit[cite: 386].
- [cite_start]Support for "Customer Loyalty" classification and prescriptive retention strategies[cite: 345].