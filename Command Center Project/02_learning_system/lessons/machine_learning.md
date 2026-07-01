# Production‑Grade Machine Learning Lesson  
**Goal:** Equip engineers and data scientists with the fundamentals, tooling, and best practices needed to design, train, evaluate, and deploy machine‑learning models in a real‑world environment.  

---

## 1. Overview & Learning Objectives  

| Objective | What you’ll be able to do |
|----------|---------------------------|
| **Understand core ML concepts** | Explain supervised/unsupervised learning, bias‑variance trade‑off, overfitting, and why production models differ from research prototypes. |
| **Build reproducible data pipelines** | Use version control, data‑versioning tools, and automated preprocessing. |
| **Select & train appropriate models** | Choose algorithms for tabular, image, text, or time‑series data; apply hyper‑parameter tuning and cross‑validation. |
| **Evaluate models rigorously** | Apply proper train/validation/test splits, appropriate metrics, and cross‑validation strategies. |
| **Package & serve models** | Serialize models (ONNX/Joblib), containerize with Docker, and expose inference via a lightweight API (FastAPI). |
| **Apply production best practices** | Implement CI/CD, monitoring, logging, and ethical safeguards for ML systems. |

---

## 2. Core Machine‑Learning Concepts  

| Concept | Why it matters in production |
|---------|------------------------------|
| **Supervised vs. Unsupervised** | Determines the loss function, evaluation metric, and data labeling requirements. |
| **Bias‑Variance Trade‑off** | Guides model complexity; over‑fitting leads to poor generalization on new data. |
| **Regularization (L1/L2, dropout, early stopping)** | Controls variance without sacrificing predictive power. |
| **Feature Engineering & Scaling** | Directly impacts convergence speed and final performance. |
| **Model Interpretability** | Enables debugging, regulatory compliance, and stakeholder trust. |

---

## 3. Data Engineering Foundations  

1. **Acquisition** – Pull data from relational DBs, APIs, or streaming sources.  
2. **Cleaning** – Handle missing values, outliers, and schema drift.  
3. **Feature Store** – Centralize engineered features for training & inference (e.g., Feast, Hopsworks).  
4. **Versioning** – Use DVC, Git LFS, or MLflow to lock data snapshots.  

```python
# Example: Load a CSV with pandas & basic sanity checks
import pandas as pd

df = pd.read_csv('sales_data.csv')
print(df.head())
print(df.info())
```

---

## 4. Model Selection & Training  

| Algorithm | Typical Use‑Case | Key Hyper‑parameters |
|-----------|------------------|----------------------|
| **Linear / Logistic Regression** | Baseline, high‑dimensional sparse data | Regularization strength (C), activation function |
| **Tree‑Based (RandomForest, XGBoost, LightGBM)** | Tabular classification/regression | Number of trees, max depth, learning rate |
| **Neural Networks (Keras / PyTorch)** | Unstructured data, sequential patterns | Hidden units, dropout, batch size, optimizer |
| **Clustering (K‑means, DBSCAN)** | Unsupervised segmentation | Number of clusters, distance metric |

### 4.1 Scikit‑learn Pipeline Example  

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# 1️⃣ Define features & target
X = df[['age', 'income', 'square_feet']]
y = df['price']

# 2️⃣ Train/validation split (80/20) – keep a hold‑out test set for final evaluation
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3️⃣ Column transformer: scale numeric features, one‑hot encode categoricals
numeric_features = ['age', 'income']
categorical_features = ['city']

preprocess = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ]
)

# 4️⃣ Model + pipeline
model = Pipeline(steps=[
    ('preprocess', preprocess),
    ('rf', RandomForestRegressor(
        n_estimators=200,
        max_depth=None,
        random_state=42
    ))
])

# 5️⃣ Fit
model.fit(X_train, y_train)

# 6️⃣ Predict & evaluate
preds = model.predict(X_test)
print(f'MAE: {mean_absolute_error(y_test, preds):.2f}')
print(f'R²: {r2_score(y_test, preds):.4f}')
```

### 4.2 Hyper‑parameter Tuning with Optuna  

```python
import optuna

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 20),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3)
    }
    clf = RandomForestRegressor(**params, random_state=42)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_val)
    return mean_absolute_error(y_val, preds)

study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=30)
print(f'Best trial: {study.best_params}')
```

---

## 5. Model Serialization & Experiment Tracking  

| Tool | Primary Use |
|------|-------------|
| **Joblib / Pickle** | Quick serialization of scikit‑learn models (binary). |
| **ONNX** | Cross‑framework model export; enables inference on CPU/GPU with TensorFlow Lite, OpenVINO, etc. |
| **MLflow** | Centralized tracking of runs, parameters, artifacts, and model versioning. |
| **DVC** | Git‑compatible data versioning (large blobs). |

```python
# Save a scikit‑learn pipeline to the local DVC index
import dvc

@dvc.command()
def save_model():
    import joblib
    dvc.add('model.pkl', model)          # joblib is preferred for sklearn models
    print("Model saved to DVC index.")

# Later, in CI/CD:
# dvc checkout --recursive model.pkl
```

---

## 6. Containerization & Deployment  

### 6.1 Minimal Dockerfile (FastAPI + ONNX)

```dockerfile
# ---- Build stage -------------------------------------------------
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ---- Runtime stage ------------------------------------------------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

`requirements.txt`

```
fastapi
uvicorn[standard]
torch   # or tensorflow, onnxruntime, etc.
joblib
mlflow
```

### 6.2 FastAPI Inference Service  

```python
# main.py
from fastapi import FastAPI
import joblib

app = FastAPI()
model = joblib.load("model.pkl")          # path to saved scikit‑learn model

@app.get("/predict")
def predict(price: float):
    # Expect a JSON payload {"price": 350000}
    features = [{"price": price}]
    pred = model.predict(features)
    return {"predicted_price": round(pred[0], 2)}
```

Build & run:

```bash
docker build -t ml-service .
docker run -p 8080:8080 -v $(pwd):/app ml-service
```

---

## 7. Production Best Practices  

| Area | Recommended Practice |
|------|----------------------|
| **CI/CD** | Automate test suites (unit, integration) and model validation on each PR; use GitHub Actions or GitLab CI. |
| **Observability** | Export structured logs (JSON), metrics (Prometheus), and traces (OpenTelemetry). |
| **Scaling** | Deploy inference containers behind a load balancer; use Kubernetes HPA for auto‑scaling based on CPU/memory or request latency. |
| **Security** | Enforce TLS, validate input schemas, and apply RBAC on the API gateway. |
| **Data Drift & Monitoring** | Set up drift detectors (e.g., KolibriAI, Evidently AI) that alert when feature distributions diverge. |
| **Model Retraining** | Schedule periodic retraining pipelines (e.g., weekly) using DVC + Airflow/Kubeflow Pipelines. |
| **Ethics & Fairness** | Conduct bias audits, document model cards, and provide explainability (SHAP/LIME). |

---

## 8. End‑to‑End Mini‑Project: House‑Price Prediction  

1. **Data ingestion** – Load `housing.csv` from S3 or a local bucket.  
2. **Preprocessing** – Impute missing values, encode categorical city names, scale numeric features.  
3. **Model training** – Use the pipeline above with Optuna hyper‑parameter tuning.  
4. **Export** – Save the final model to `model.pkl` and push it to an artifact repository (e.g., S3).  
5. **Containerize** – Build a Docker image that runs the FastAPI service.  
6. **Deploy** – Deploy on a cloud VM or managed Kubernetes cluster; expose `/predict` endpoint.  

*(Full script would be ~150 lines; the snippets above illustrate the critical steps.)*

---

## 9. Quiz – Test Your Understanding  

**Q1.** *Explain the difference between bias and variance in a model, and why both need to be balanced for production models.*  
A. **Bias** is the error from erroneous assumptions in the learning algorithm; high bias leads to under‑fitting. **Variance** is the error from sensitivity to small fluctuations in training data; high variance leads to over‑fitting. Production models require a balance—often achieved by regularization, cross‑validation, or ensembling.

---

**Q2.** *Which serialization format is most suitable for exporting a scikit‑learn pipeline that includes preprocessing steps and hyper‑parameter tuning results?*  
A. **ONNX** – enables inference on multiple runtimes (TensorFlow, PyTorch, OpenVINO) while preserving scikit‑learn model state; ideal when you need cross‑framework compatibility.

---

**Q3.** *Describe two key practices for monitoring a deployed ML service and how they help maintain model quality.*  
A. **Logging & Metrics:** Capture inference latency, error rates, and feature distribution statistics in a centralized observability platform (e.g., Prometheus + Grafana). This provides early detection of performance degradation or data drift.  
**Model Drift Alerts:** Use statistical tests (e.g., Kolmogorov‑Smirnov) on incoming feature distributions; trigger automated retraining pipelines when significant divergence is observed.

---

*Answer key:* Q1 – as above; Q2 – ONNX; Q3 – detailed description of logging/metrics and drift detection.  

---

### 🎓 Takeaway  

Machine learning in production is **more than just training a model**—it’s about building robust pipelines, ensuring reproducibility, delivering models that can be scaled safely, and continuously monitoring them. By mastering the concepts, tools, and practices outlined above, you’re equipped to move from notebook experiments to reliable, enterprise‑grade AI services.  

Happy modeling! 🚀

## Quiz
- **Q1:** Explain the difference between bias and variance in a model, and discuss how both need to be balanced to achieve good performance in production environments.  
- **Q2:** Which serialization format is most suitable for exporting a scikit‑learn pipeline that includes preprocessing steps and hyper‑parameter tuning results, and what are the advantages of using it over other formats?  
- **Q3:** Describe two specific practices for monitoring a deployed machine‑learning service and explain how each practice helps maintain model quality over time.