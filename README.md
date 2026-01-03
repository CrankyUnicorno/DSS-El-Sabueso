# DSS "El Sabueso" — Customer Loyalty Predictor

Decision Support System for **Perrito Reciclado** that predicts customer loyalty and suggests marketing actions using a pre-trained Decision Tree (CART). Built with Streamlit for an interactive UI.

## What This Project Does
- Predicts whether a customer will be a **frequent** or **sporadic** buyer.
- Provides **probability of return** and tailored marketing recommendations.
- Supports two workflows: **Manual entry** and **Lookup existing customer** from an Excel database.

## Project Structure
- `README.md`: This documentation file.
- [LICENSE](LICENSE): MIT License for the project.
- .gitignore: Git ignore rules.
- data/: Folder containing the Excel data file.
  - data/: Datos_Entrenamiento_Final.xlsx: Training/lookup data with sheet `CLIENTES`.
- models/: Folder containing model artifacts (.pkl files).
  - models/: modelo_perrito.pkl: Trained Decision Tree model.
  - models/: columnas_modelo.pkl: Expected feature columns for inference.
  - models/: traductor_respuestas.pkl: Label encoder for predictions.
- notebooks/: Jupyter notebooks used for model training and experimentation.
  - notebooks/: Perrito.ipynb: Model training and evaluation notebook.
- [app.py](app.py): Streamlit app (UI + inference logic).
- [requirements.txt](requirements.txt): Python dependencies that are required to run the app.

## Prerequisites
- Python 3.10+
- Recommended: virtual environment (`venv` or `conda`).
- The three `.pkl` artifacts and the Excel file must be placed in the project root, don't worry, they are included in the repo for demonstration purposes.

## Setup
1) Clone and enter the project folder:
```bash
git clone https://github.com/CrankyUnicorno/DSS-El-Sabueso.git
cd DSS-El-Sabueso
```
2) Create and activate a virtual environment (example with `venv`):
```bash
python -m venv .venv
./.venv/Scripts/activate    # Windows
source .venv/bin/activate   # macOS/Linux
```
3) Install dependencies:
```bash
pip install -r requirements.txt
```
4) Add the model artifacts and data in the project root, dont worry they are already here for demo purposes:
```
modelo_perrito.pkl
columnas_modelo.pkl
traductor_respuestas.pkl
Datos_Entrenamiento_Final.xlsx
```

## Running the App Locally
```bash
streamlit run app.py
```
Then open the URL shown in the terminal (default: `http://localhost:8501`).

## How the App Works
1. Loads the trained Decision Tree, feature column list, and label encoder with Streamlit caching.
2. Optionally loads `Datos_Entrenamiento_Final.xlsx` to let you search existing customers (sheet `CLIENTES`).
3. Builds a feature row from user inputs, one-hot encodes categorical fields, and reindexes to `columnas_modelo`.
4. Runs `predict` and `predict_proba` to get class and loyalty probability.
5. Maps the probability to a recommendation tier with actionable suggestions.

## Using the Interface
- **Mode selector:** Choose *Nuevo Cliente (Manual)* or *Buscar Cliente Existente*.
- **Search mode:** Pick a customer; defaults are auto-filled from Excel. If the file is missing, the UI shows an error.
- **Manual mode:** Enter age, spend, visits, contact medium, gender, pet type, profession, and marital status.
- **Calculate Prediction:** Displays probability, predicted class, tiered recommendation, progress bar, and debug view of model inputs.

## Data Expectations
- Excel sheet name: `CLIENTES`.
- Required columns (trimmed for spaces):
  - `ID CLIENTE`, `NOMBRE CLIENTE`, `EDAD`, `CANTIDAD GASTADA`, `VECES COMPRADO EN LA TIENDA`, `MEDIO CONTACTO`, `SEXO`, `TIPO MASCOTA`, `PROFESION`, `ESTADO CIVIL`.
- Feature columns used at inference must match `columnas_modelo.pkl` exactly after one-hot encoding.

## Troubleshooting
- **Missing .pkl or Excel files:** The app shows an error; ensure the four artifacts are in the project root.
- **Shape mismatch errors:** Confirm the `columnas_modelo.pkl` matches the training-time one-hot columns and that categorical values are consistent.
- **Streamlit not launching:** Verify the virtual environment is active and dependencies are installed; try `python -m streamlit run app.py`.

## Customization
- Update recommendation logic in `obtener_recomendacion` inside [app.py](app.py).
- Swap the model by retraining and exporting new `modelo_perrito.pkl`, `columnas_modelo.pkl`, and `traductor_respuestas.pkl` with aligned feature engineering.
- Adjust UI defaults in `defaults` within [app.py](app.py).

## Deployment Notes
- Streamlit can be deployed to Streamlit Community Cloud, Render, or similar. Ensure model artifacts and Excel are available to the runtime (e.g., uploaded as app assets or fetched from object storage).
- For Docker, copy the four artifacts into the image and expose port 8501.

## License
The project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
