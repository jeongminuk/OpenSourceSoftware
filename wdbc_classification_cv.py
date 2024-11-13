import numpy as np
from sklearn import datasets, model_selection
from xgboost import XGBClassifier

if __name__ == '__main__':
    # Load a dataset
    wdbc = datasets.load_breast_cancer()

    # Train a model using XGBClassifier with balanced parameters
    model = XGBClassifier(
        n_estimators=1000,       # Moderate number of trees for faster training
        learning_rate=0.01,      # Low learning rate for steady improvements
        max_depth=6,             # Depth to capture complex patterns without overfitting
        subsample=0.85,          # Slightly larger subset of data to improve generalization
        colsample_bytree=0.85,   # Slightly larger subset of features
        objective='binary:logistic',
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    cv_results = model_selection.cross_validate(model, wdbc.data, wdbc.target, cv=5, return_train_score=True)

    # Evaluate the model
    acc_train = np.mean(cv_results['train_score'])
    acc_test = np.mean(cv_results['test_score'])
    print(f'* Accuracy @ training data: {acc_train:.3f}')
    print(f'* Accuracy @ test data: {acc_test:.3f}')
    print(f'* Your score: {max(10 + 100 * (acc_test - 0.9), 0):.0f}')
