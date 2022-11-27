import numpy as np
import sys
from scipy import sparse
from sklearn.model_selection import train_test_split

(
    data_file,
    random_seed,
    train_file,
    validate_file,
    test_file
) = sys.argv[1:]
random_seed = int(random_seed)

if data_file.endswith("npz"):
    data = sparse.load_npz(data_file)
else:
    data = np.load(data_file, allow_pickle=True)

train, other = train_test_split(data, train_size=0.6, random_state=random_seed)
validate, test = train_test_split(other, train_size=0.5, random_state=random_seed)

if data_file.endswith("npz"):
    sparse.save_npz(train_file, train)
    sparse.save_npz(validate_file, validate)
    sparse.save_npz(test_file, test)
else:
    np.save(train_file, train)
    np.save(validate_file, validate)
    np.save(test_file, test)
