# sockit-data

This tool builds the occupational models that are packaged with
*[sockit](https://github.com/ripl-org/sockit/)*, a natural-language processing
toolkit for modeling structured occupation information and Standard ccupational
Classification (SOC) codes in unstructured text from job titles, job postings,
and resumes.

The methods are described in more detail in the manuscript:

> Nile Dixon, Marcelle Goggins, Ethan Ho, Mark Howison, Joe Long, Emma
> Northcott, Karen Shen, Carrie Yeats. (2022). Occupational models from 42
> million unstructured job postings.

## License

Copyright 2022 Innovative Policy Lab d/b/a Research Improving People's Lives
("RIPL"), Providence, RI. All Rights Reserved.

Your use of the Software License along with any related Documentation, Data,
etc. is governed by the terms and conditions which are available here:
[LICENSE.md](https://github.com/ripl-org/sockit-data/blob/main/LICENSE.md)

Please contact [connect@ripl.org](mailto:connect@ripl.org) to inquire about
commercial use.

## Build Steps

This tool uses the [scons](https://scons.org/) build system. The sequence of
build steps and intermediary files are described in the included
[SConstruct](https://github.com/ripl-org/sockit-data/blob/main/SConstruct) file.

First, install the python (>=3.10) build dependencies with:

    pip install numpy pandas scipy scons sockit==0.3.0 sklearn zenodo-get

Next, install the R (>=4.2) plotting dependencies with:

    Rscript -e 'install.packages(c("tidyverse", "ggplot2", "viridis", "ggsci", "gridExtra"), repos = c("https://cran.r-project.org"))'

Finally, run the `scons` command from the root directory to start the build.
You can instead use `scons -n` for a dry run or `scons -jN` to run on *N*
concurrent processors.

## Input Data

All required replication files are provided as a data set at Zenodo under DOI
[10.5281/zenodo.7319953](https://doi.org/10.5281/zenodo.7319953). This data set
contains the following files:

**job_title_acronyms.csv** (544 records) – acronyms for job titles and the SOC
codes they map to, occurring in sample job titles from the O\*NET 27.0 Database.

**job_title_nouns.txt** (2,514 records) – a manually-curated list of principal
nouns occurring in sample job titles from the O\*NET 27.0 Database.

**job_title_schedule_terms.txt** (26 records) – commonly used phrases and
abbreviations to denote work schedule in job titles; used in job title
filtering.

**LICENSE.txt** - the terms and conditions, also available from this repository
in [LICENSE.md](https://github.com/ripl-org/sockit-data/blob/main/LICENSE.md).

**nlx_company_names.txt** (999 records) – company names for members of
DirectEmployers; used in job title filtering.

**nlx_job_skill_matrix.npz** (dimensions 24,009,146 x 755) – counts of the 755
skill keywords in 24,009,146 job descriptions from the Research Hub, stored as
a scipy compressed sparse column (CSC) matrix in binary format. 

**nlx_soc_freq.csv** (1,022,240 records) – probability-weighted counts of SOC
code associations for Research Hub job postings, distinct by month and job
description content, and aggregated at the month, year, and U.S. state level;
used in technical validation below.

**nlx_soc_job_matrix.npz** (dimensions 867 x 24,009,146) – probabilities of the
867 SOC codes for 24,009,146 job titles from the Research Hub, stored as a
scipy compressed sparse row (CSR) matrix in binary format.

**nlx_titles.csv** (3,179,805 records) – distinct job titles occurring in
42,298,617 records from the Research Hub, after converting job titles to
lowercase, removing extraneous text, and retaining alphabetical characters.

**nlx_titles_management.json** (6,150 records) – a sample of management titles
containing the principal nouns manager, director, supervisor, vp or president,
with their one or two most relevant SOC codes according to the O\*NET Code
Connector.

**nlx_titles_soccer_batch1_results.csv** (500,000 records) – SOCcer results,
including the top 10 most likely SOC 2010 codes with probabilities, for the
first 500,000 filtered job titles (due to a processing limit in SOCcer).

**nlx_titles_soccer_batch2_results.csv** (349,284 records) – SOCcer results for
the remaining 349,284 filtered job titles.

**skills_alternative.txt** (254 records) – alternative terms (e.g. plural/
singular forms) for the curated skill keywords.

**skills_review.csv** (1,075 records) – the results of six reviewers manual
review of 1,075 sampled skill keywords.

**soc_2010_to_2018_crosswalk.csv** (900 records) – the crosswalk between U.S.
Bureau of Labor Statistics' 2010 SOC code and 2018 SOC code systems.

**soc_2018.csv (867 records)** – the 867 6-digit SOC codes in the U.S. Bureau
of Labor Statistics' 2018 SOC code system.

**us_places.txt (430 records)** – 50 state names, 50 state abbreviations, and
330 city names for the largest U.S. cities from Wikipedia; used in job title
filtering.

## Contributors

* [Mark Howison](https://mark.howison.org)
* Joe Long
