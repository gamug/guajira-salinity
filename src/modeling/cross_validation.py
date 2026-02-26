import os
import pandas as pd, numpy as np
import plotly.graph_objects as go, plotly.subplots as sp
from sklearn.base import clone
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import label_binarize
from sklearn.metrics import f1_score, balanced_accuracy_score, roc_auc_score, roc_curve, auc



def add_roc_traces(fig: go.Figure, n_classes: int, i: int, y_bin: list, test: list, probas_: list) -> go.Figure:
    # --- Curvas ROC por clase ---
    for j in range(n_classes):
        fpr, tpr, _ = roc_curve(y_bin[test][:, j], probas_[:, j])
        roc_auc = auc(fpr, tpr)
        
        fig.add_trace(go.Scatter(
            x=fpr, y=tpr,
            mode='lines',
            name=f'Fold {i+1} - Clase {j} (AUC={roc_auc:.2f})',
            opacity=0.6
        ))
    return fig

def add_roc_layout(fig: go.Figure) -> go.Figure:
    # Línea diagonal (clasificador aleatorio)
    fig.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1],
        mode='lines',
        line=dict(dash='dash', color='gray'),
        showlegend=True,
        name='Random'
    ))

    fig.update_layout(
        title="Curvas ROC (OvR, 3 clases) con Cross-Validation",
        xaxis_title="False Positive Rate",
        yaxis_title="True Positive Rate",
        legend_title="Curvas por fold/clase",
        width=690,
        height=400
    )
    return fig

def plot_metrics(results: pd.DataFrame) -> go.Figure:
    # Crear subplots: 1 fila, 3 columnas
    fig = sp.make_subplots(
        rows=1, cols=3,
        subplot_titles=("F1_weighted", "Balanced_accuracy", "ROC_AUC_OVR_Weighted")
    )

    # Violin plot F1_weighted
    fig.add_trace(
        go.Violin(y=results["F1_weighted"], box_visible=True, meanline_visible=True, name="F1_weighted"),
        row=1, col=1
    )

    # Violin plot Balanced_accuracy
    fig.add_trace(
        go.Violin(y=results["Balanced_accuracy"], box_visible=True, meanline_visible=True, name="Balanced_accuracy"),
        row=1, col=2
    )

    # Violin plot ROC_AUC_OVR_Weighted
    fig.add_trace(
        go.Violin(y=results["ROC_AUC_OVR_Weighted"], box_visible=True, meanline_visible=True, name="ROC_AUC_OVR_Weighted"),
        row=1, col=3
    )

    # Ajustar layout
    fig.update_layout(
        title="Violin plots de métricas en validación cruzada",
        width=690,
        height=400
    )
    fig.update_annotations(font=dict(size=12))
    fig.update_xaxes(tickfont=dict(size=10))

    fig.update_yaxes(tickfont=dict(size=10))
    return fig

def cross_validate(base_model,  X: pd.DataFrame, y: pd.DataFrame, folds: int=5):
    classes = np.unique(y)
    y_bin = label_binarize(y, classes=classes)
    n_classes = y_bin.shape[1]
    cv = StratifiedKFold(n_splits=folds, shuffle=True, random_state=42)

    # Almacenar métricas
    metrics = []

    # Figura interactiva
    roc = go.Figure()

    for i, (train, test) in enumerate(cv.split(X, y)):
        model = clone(base_model)
        model.fit(X.iloc[train], y.iloc[train])
        probas_ = model.predict_proba(X.iloc[test])
        preds = model.predict(X.iloc[test])
        
        # --- Métricas ---
        f1_w = f1_score(y.iloc[test], preds, average="weighted")
        bal_acc = balanced_accuracy_score(y.iloc[test], preds)
        roc_auc_w = roc_auc_score(y_bin[test], probas_, average="weighted", multi_class="ovr")
        
        metrics.append([i+1, f1_w, bal_acc, roc_auc_w])
        
        roc = add_roc_traces(roc, n_classes, i, y_bin, test, probas_)

    roc = add_roc_layout(roc)
    model = clone(base_model)
    model.fit(X, y)
    # --- Resultados en tabla ---
    df_results = pd.DataFrame(metrics, columns=["Fold", "F1_weighted", "Balanced_accuracy", "ROC_AUC_OVR_Weighted"])
    violin = plot_metrics(df_results)
    return roc, violin, model

# def get_training_inputs() -> dict:
#     dataset = pd.read_csv(os.path.join('files', 'data', 'datasets', 'salinity_curated.csv'))
#     encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
#     # encoded_data = encoder.fit(dataset[['class_hidr']])
#     X = dataset.drop('CATEGORIA_SAL', axis=1)
#     encoded_data = encoder.fit_transform(X[['class_hidr']])
#     encoded_data = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(['class_hidr'])).reset_index(drop=True)
#     X = X.drop('class_hidr', axis=1).join(encoded_data)
#     le = LabelEncoder()
#     y = le.fit_transform(dataset['CATEGORIA_SAL'])
#     smote = SMOTE(random_state=42)
#     X_resampled, y_resampled = smote.fit_resample(X, y)
#     y_resampled = pd.DataFrame(data=y_resampled, columns=['CATEGORIA_SAL'])
#     pipeline = Pipeline([
#         ('scaler', MinMaxScaler()),
#         ('randomforest', OneVsRestClassifier(RandomForestClassifier(n_estimators=100, random_state=42)))
#     ])
#     training_inputs = {
#         'dataset': dataset, 'X': X_resampled, 'y': y_resampled,
#         'encoder': encoder, 'label_encoder': le, 'pipeline': pipeline
#     }
#     return training_inputs
