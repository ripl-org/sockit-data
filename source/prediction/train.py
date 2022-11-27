import lightgbm as lgb
import pandas as pd
import re
import sys
from scipy import sparse
from sklearn.metrics import roc_auc_score

(
    X_train_file,
    y_train_file,
    X_validate_file,
    y_validate_file,
    X_test_file,
    y_test_file,
    skills_file,
    random_seed,
    i,
    soc,
    model_file
) = sys.argv[1:]
random_seed = int(random_seed)
i = int(i)

skills = [
    re.sub(r"[^A-Za-z0-9_]+", "_", skill)
    for skill in pd.read_csv(skills_file, index_col="skill_id").skill
]

train = lgb.Dataset(
    sparse.load_npz(X_train_file),
    label=sparse.load_npz(y_train_file)[:,i].toarray().flatten(),
    feature_name=skills
)

validate = lgb.Dataset(
    sparse.load_npz(X_validate_file),
    label=sparse.load_npz(y_validate_file)[:,i].toarray().flatten(),
    feature_name=skills
)

X_test = sparse.load_npz(X_test_file)
y_test = sparse.load_npz(y_test_file)[:,i].toarray().flatten()

model = lgb.train(
    {
        "objective": "binary",
        "random_seed": random_seed,
        "num_iterations": 1000,
        "metric": "auc"
    },
    train_set=train,
    valid_sets=[validate],
    callbacks=[lgb.early_stopping(stopping_rounds=50)]
)

model.save_model(model_file, num_iteration=model.best_iteration)

y_hat = model.predict(X_test, num_iteration=model.best_iteration)

print("Test AUC:", roc_auc_score(y_test, y_hat))
