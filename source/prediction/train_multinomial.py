import lightgbm as lgb
import numpy as np
import pandas as pd
import re
import sys
from auc_mu import auc_mu
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
    model_file,
    soc4_file
) = sys.argv[1:]
random_seed = int(random_seed)

skills = [
    re.sub(r"[^A-Za-z0-9_]+", "_", skill)
    for skill in pd.read_csv(skills_file, index_col="skill_id").skill
]

y_train = np.load(y_train_file, allow_pickle=True)

soc4_lookup = {soc4: i for i, soc4 in enumerate(np.unique(y_train))}
with open(soc4_file, "w") as f:
    print("soc4_id,soc4", file=f)
    for soc4, i in soc4_lookup.items():
        print(i, soc4, sep=",", file=f)

train = lgb.Dataset(
    sparse.load_npz(X_train_file),
    label=[soc4_lookup[soc4] for soc4 in y_train],
    feature_name=skills
)

validate = lgb.Dataset(
    sparse.load_npz(X_validate_file),
    label=[soc4_lookup[soc4] for soc4 in np.load(y_validate_file, allow_pickle=True)],
    feature_name=skills
)

X_test = sparse.load_npz(X_test_file)
y_test = np.array([soc4_lookup[soc4] for soc4 in np.load(y_test_file, allow_pickle=True)])

model = lgb.train(
    {
        "objective": "multiclass",
        "num_class": len(soc4_lookup),
        "random_seed": random_seed,
        "num_iterations": 1000,
        "metric": "auc_mu"
    },
    train_set=train,
    valid_sets=[validate],
    callbacks=[lgb.early_stopping(stopping_rounds=50)]
)

model.save_model(model_file, num_iteration=model.best_iteration)

y_hat = model.predict(X_test, num_iteration=model.best_iteration)

print("Test AUC_MU:", auc_mu(y_test, y_hat))
