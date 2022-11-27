import os
import pandas as pd

env = Environment(ENV=os.environ)

DOI = "10.5281/zenodo.7319953" # DOI of the replication files at Zenodo
TOP_MATCHES = 3 # Number of matches to consider in validation
RANDOM_SEED = 167566

# Input files from Zenodo
env.Command(
    target=[
        "input/job_title_acronyms.csv",
        "input/job_title_nouns.txt",
        "input/job_title_schedule_terms.txt",
        "input/LICENSE.txt",
        "input/nlx_company_names.txt",
        "input/nlx_job_skill_matrix.npz",
        "input/nlx_soc_freq.csv",
        "input/nlx_soc_job_matrix.npz",
        "input/nlx_titles.csv",
        "input/nlx_titles_management.json",
        "input/nlx_titles_soccer_batch1_results.csv",
        "input/nlx_titles_soccer_batch2_results.csv",
        "input/skills_review.csv",
        "input/skills_alternative.csv",
        "input/soc_2018.csv",
        "input/soc_2010_to_2018_crosswalk.csv",
        "input/us_places.txt"
    ],
    source=[
        Value(DOI)
    ],
    action=f"zenodo_get -o input/ -d $SOURCE"
)

# Filter NLx titles
env.Command(
    target=[
        "scratch/nlx_titles_filtered.csv",
        "scratch/nlx_titles_filtered.log"
    ],
    source=[
        "source/nlx_titles_filtered.py",
        "input/nlx_titles.csv",
        "input/nlx_company_names.txt",
        "input/us_places.txt",
        "input/job_title_schedule_terms.txt",
        "input/job_title_nouns.txt"
    ],
    action="python $SOURCES ${TARGETS[0]} > ${TARGETS[1]}"
)

# Extract management titles and words
# NOTE: The titles and words below were submitted to the
# O*NET Code Connector to identify the top 1-2 SOC code
# matches, producing:
#   input/nlx_titles_management.json
env.Command(
    target=[
        "scratch/nlx_titles_management.csv",
        "scratch/nlx_titles_management_words.csv"
    ],
    source=[
        "source/nlx_titles_management.py",
        "input/nlx_titles.csv",
        "input/nlx_company_names.txt",
        "input/us_places.txt",
        "input/job_title_schedule_terms.txt",
    ],
    action="python $SOURCES $TARGETS"
)

# Prepare SOCcer batches
# NOTE: The SOCcer batches below were manually submitted to the
# SOCcer web interface on 2022-09-05, producing:
#   input/nlx_titles_soccer_batch1_results.csv
#   input/nlx_titles_soccer_batch2_results.csv
env.Command(
    target=[
        "scratch/nlx_titles_soccer_batch1.csv",
        "scratch/nlx_titles_soccer_batch2.csv"
    ],
    source=[
        "source/nlx_titles_soccer.py",
        "scratch/nlx_titles_filtered.csv"
    ],
    action="python $SOURCES $TARGETS"
)

# Acronyms lookup table
env.Command(
    target=[
        "output/sockit/data/lookups/acronyms.json"
    ],
    source=[
        "source/acronyms.py",
        "input/job_title_acronyms.csv"
    ],
    action="python $SOURCES $TARGETS"
)

# Job titles prefix tree and title override prefix tree
env.Command(
    target=[
        "output/sockit/data/tries/job_titles.json",
        "output/sockit/data/tries/job_titles_override.json"
    ],
    source=[
        "source/job_titles.py",
        "input/nlx_titles_management.json",
        "input/soc_2010_to_2018_crosswalk.csv",
        "scratch/nlx_titles_filtered.csv",
        "input/nlx_titles_soccer_batch1_results.csv",
        "input/nlx_titles_soccer_batch2_results.csv",
        "source/job_titles_handcoded.csv"
    ],
    action="python $SOURCES $TARGETS"
)

# Skills prefix tree
env.Command(
    target=[
        "output/sockit/data/tries/skills.json",
        "output/sockit/data/skills.csv"
    ],
    source=[
        "source/skills.py",
        "input/skills_review.csv",
        "input/skills_alternative.csv"
    ],
    action="python $SOURCES $TARGETS"
)

# SOC-skill matrix
env.Command(
    target=[
        "output/sockit/data/skill_idf_vector.txt",
        "output/sockit/data/soc_skill_matrix.txt",
        "scratch/soc_skill_matrix.csv"
    ],
    source=[
        "source/soc_skill_matrix.py",
        "input/soc_2018.csv",
        "output/sockit/data/skills.csv",
        "input/nlx_soc_job_matrix.npz",
        "input/nlx_job_skill_matrix.npz"
    ],
    action="python $SOURCES $TARGETS"
)

# SOC distance
env.Command(
    target=[
        "scratch/soc_distance_summary.txt"
    ]+[
        f"scratch/soc_distance_matrix_{d}.csv"
        for d in ["euclidean", "manhattan", "cosine", "kl"]
    ],
    source=[
        "source/soc_distance.py",
        "scratch/soc_skill_matrix.csv",
        "output/sockit/data/skills.csv"
    ],
    action="python $SOURCES $TARGETS"
)

# SOC-skill matrix plot
env.Command(
    target=[
        "output/plots/soc_skill_matrix.pdf"
    ],
    source=[
        "source/plots/soc_skill_matrix.R",
        "input/soc_2018.csv",
        "output/sockit/data/skills.csv",
        "output/sockit/data/soc_skill_matrix.txt"
    ],
    action="Rscript $SOURCES $TARGETS"
)

# SOC similarity plots
env.Command(
    target=[
        "output/plots/soc_similarity.pdf"
    ],
    source=[
        "source/plots/soc_similarity.R",
        "input/soc_2018.csv"
    ]+[
        f"scratch/soc_distance_matrix_{d}.csv"
        for d in ["euclidean", "manhattan", "cosine", "kl"]
    ],
    action="Rscript $SOURCES $TARGETS"
)

# Synthetic job postings (for job parsing validation)
env.Command(
    target=[
        "scratch/synthetic_jobs/sentinel.txt"
    ],
    source=[
        "source/synthetic_jobs.py",
        "input/soc_2018.csv",
        "public-data/onet_db_27_0_text/Occupation Data.txt",
        "public-data/onet_db_27_0_text/Task Statements.txt",
        "public-data/onet_db_27_0_text/Tasks to DWAs.txt",
        "public-data/onet_db_27_0_text/DWA Reference.txt"
    ],
    action="python $SOURCES $TARGETS"
)

# Validate titles
env.Command(
    target=[
        "scratch/validate_titles.csv"
    ],
    source=[
        "source/validate_titles.py",
        "input/soc_2018.csv",
        "public-data/onet_db_27_0_text/Sample of Reported Titles.txt",
        Value(TOP_MATCHES)
    ],
    action="python $SOURCES $TARGETS"
)

# Validate job postings
env.Command(
    target=[
        "scratch/validate_jobs.csv"
    ],
    source=[
        "source/validate_jobs.py",
        "input/soc_2018.csv",
        "scratch/synthetic_jobs/sentinel.txt",
        Value(TOP_MATCHES)
    ],
    action="python $SOURCES $TARGETS"
)

# Matches plot
env.Command(
    target=[
        "output/plots/matches.pdf"
    ],
    source=[
        "source/plots/matches.R",
        "scratch/validate_employment.csv",
        "scratch/validate_jobs.csv",
        "scratch/validate_titles.csv"
    ],
    action="Rscript $SOURCES $TARGETS"
)

# Validate employment
env.Command(
    target=[
        "scratch/validate_employment.csv"
    ],
    source=[
        "source/validate_employment.py",
        "input/nlx_soc_freq.csv",
        "public-data/employment.csv"
    ],
    action="python $SOURCES $TARGETS"
)

# Employment plot
env.Command(
    target=[
        "output/plots/employment.pdf"
    ],
    source=[
        "source/plots/employment.R",
        "scratch/validate_employment.csv"
    ],
    action="Rscript $SOURCES $TARGETS"
)

# Validate openings
env.Command(
    target=[
        "scratch/validate_openings.csv"
    ],
    source=[
        "source/validate_openings.py",
        "input/nlx_soc_freq.csv",
        "public-data/openings.csv"
    ],
    action="python $SOURCES $TARGETS"
)

# Employment plot
env.Command(
    target=[
        "output/plots/openings.pdf"
    ],
    source=[
        "source/plots/openings.R",
        "scratch/validate_openings.csv"
    ],
    action="Rscript $SOURCES $TARGETS"
)


### PREDICTIVE MODELS ###

# Define outcomes as 1 for SOCs >=0.1 probability
env.Command(
    target=[
        "scratch/prediction/outcome_counts.csv",
        "scratch/prediction/outcomes.npz"
    ],
    source=[
        "source/prediction/outcomes.py",
        "input/soc_2018.csv",
        "input/nlx_soc_job_matrix.npz"
    ],
    action="python $SOURCES $TARGETS"
)

# Define multinomial outcome using the most probable SOC4
env.Command(
    target=[
        "scratch/prediction/outcomes_multinomial.npy"
    ],
    source=[
        "source/prediction/outcomes_multinomial.py",
        "input/soc_2018.csv",
        "input/nlx_soc_job_matrix.npz"
    ],
    action="python $SOURCES $TARGETS"
)

# Split into train/validate/test sets
env.Command(
    target=[
        "scratch/prediction/X_train.npz",
        "scratch/prediction/X_validate.npz",
        "scratch/prediction/X_test.npz"
    ],
    source=[
        "source/prediction/split.py",
        "input/nlx_job_skill_matrix.npz",
        Value(RANDOM_SEED)
    ],
    action="python $SOURCES $TARGETS"
)
env.Command(
    target=[
        "scratch/prediction/y_train.npz",
        "scratch/prediction/y_validate.npz",
        "scratch/prediction/y_test.npz"
    ],
    source=[
        "source/prediction/split.py",
        "scratch/prediction/outcomes.npz",
        Value(RANDOM_SEED)
    ],
    action="python $SOURCES $TARGETS"
)
env.Command(
    target=[
        "scratch/prediction/ym_train.npy",
        "scratch/prediction/ym_validate.npy",
        "scratch/prediction/ym_test.npy"
    ],
    source=[
        "source/prediction/split.py",
        "scratch/prediction/outcomes_multinomial.npy",
        Value(RANDOM_SEED)
    ],
    action="python $SOURCES $TARGETS"
)

# Train individual classifiers
socs = pd.read_csv("source/prediction/soc_2018.csv", index_col="soc_id")
# Skip SOCs that fail to train
socs = [
    (i, soc)
    for i, soc in socs.soc.items()
    if soc not in [251069, 251082, 393099, 472053, 475043, 499064, 516092, 536032, 536099, 551012, 551016, 552011, 552012, 553012]
]
for i, soc in socs:
    env.Command(
        target=[
            f"scratch/prediction/models/{soc}.txt"
        ],
        source=[
            "source/prediction/train.py",
            "scratch/prediction/X_train.npz",
            "scratch/prediction/y_train.npz",
            "scratch/prediction/X_validate.npz",
            "scratch/prediction/y_validate.npz",
            "scratch/prediction/X_test.npz",
            "scratch/prediction/y_test.npz",
            "output/sockit/data/skills.csv",
            Value(RANDOM_SEED),
            Value(i),
            Value(soc)
        ],
        action="python $SOURCES $TARGETS >${TARGET}.log"
    )

# AUCs of individual classifiers
env.Depends(
    env.Command(
        target=[
            f"scratch/prediction/auc.csv"
        ],
        source=[
            "source/prediction/auc.py",
            "source/prediction/soc_2018.csv"
        ],
        action="python $SOURCES $TARGETS"
    ),
    [
        f"scratch/prediction/models/{soc}.txt"
        for i, soc in socs
    ]
)

# AUC plots
env.Command(
    target=[
        "output/plots/prediction_auc.pdf"
    ],
    source=[
        "source/plots/prediction_auc.R",
        "scratch/prediction/auc.csv"
    ],
    action="Rscript $SOURCES $TARGETS"
)

# Train multinomial classifier
env.Command(
    target=[
        f"scratch/prediction/models/multinomial.txt",
        "scratch/prediction/soc4.csv"
    ],
    source=[
        "source/prediction/train_multinomial.py",
        "scratch/prediction/X_train.npz",
        "scratch/prediction/ym_train.npy",
        "scratch/prediction/X_validate.npz",
        "scratch/prediction/ym_validate.npy",
        "scratch/prediction/X_test.npz",
        "scratch/prediction/ym_test.npy",
        "output/sockit/data/skills.csv",
        Value(RANDOM_SEED)
    ],
    action="python $SOURCES $TARGETS >${TARGET}.log"
)
