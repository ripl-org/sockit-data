library(tidyverse)
library(ggplot2)

args         <- commandArgs(trailingOnly = TRUE)
labels_file  <- args[1]
jobs_file    <- args[2]
titles_files <- args[3]
pdf_file     <- args[4]

acs_labels <- read_csv(labels_file) %>%
  select(soc2, acs_label) %>%
  distinct() %>%
  mutate(
    soc2 = as.character(soc2),
    label = paste(soc2, acs_label),
    acs_label = NULL
  ) %>%
  add_row(soc2 = "00", label = "OVERALL")

jobs <- read_csv(jobs_file) %>%
  mutate(soc = as.character(soc)) %>%
  add_row(
    summarize(
      .,
      soc = "00",
      match2 = sum(match2) / n(),
      match3 = sum(match3) / n(),
      match5 = sum(match5) / n(),
      match6 = sum(match6) / n()
    )
  ) %>%
  mutate(soc2 = substr(soc, 1, 2)) %>%
  pivot_longer(cols = starts_with("match"), names_to = "digits", values_to = "match") %>%
  mutate(digits = substr(digits, 6, 7)) %>%
  group_by(soc2, digits) %>%
  summarize(n = n(), percent = 100.0 * sum(match) / n()) %>%
  ungroup() %>%
  mutate(type = "Job Postings")

titles <- read_csv(titles_files) %>%
  select(-title) %>%
  mutate(soc = as.character(soc)) %>%
  add_row(
    summarize(
      .,
      soc = "00",
      match2 = sum(match2) / n(),
      match3 = sum(match3) / n(),
      match5 = sum(match5) / n(),
      match6 = sum(match6) / n()
    )
  ) %>%
  mutate(soc2 = substr(soc, 1, 2)) %>%
  pivot_longer(cols = starts_with("match"), names_to = "digits", values_to = "match") %>%
  mutate(digits = substr(digits, 6, 7)) %>%
  group_by(soc2, digits) %>%
  summarize(n = n(), percent = 100.0 * sum(match) / n()) %>%
  ungroup() %>%
  mutate(type = "Titles")

data <- bind_rows(list(jobs, titles)) %>%
  filter(soc2 != "55") %>%
  left_join(acs_labels, by = c("soc2")) %>%
  mutate(
    label = as.factor(label),
    soc2 = NULL,
    digits = as.factor(digits),
    type = factor(type, levels = c("Titles", "Job Postings"))
  )

print(filter(data, label == "OVERALL"))

g <- ggplot(data, aes(digits, percent)) +
  geom_col(width = 0.75) +
  coord_flip() +
  scale_x_discrete(
    breaks = c("2", "3", "5", "6"),
    limits = rev
  ) +
  scale_y_continuous(
    breaks = seq(0, 100, 10),
    labels = sapply(seq(0, 100, 10), function(y) { paste0(y, "%") })
  ) +
  labs(
    y = "Accuracy",
    x = "# of SOC Digits in Match"
  ) +
  theme_minimal() +
  theme(
    axis.title = element_text(size=7),
    axis.text.x = element_text(size = 6, angle = 90),
    axis.text.y = element_text(size = 4),
    axis.ticks.y = element_blank(),
    panel.grid = element_blank(),
    panel.grid.major.x = element_line(color = "gray70", size = 0.125, linetype = 1),
    strip.text.x = element_text(size = 10, hjust = 0),
    strip.text.y = element_text(size = 7, hjust = 0, angle = 0)
  ) +
  facet_grid(label ~ type)

ggsave(
  filename = pdf_file,
  plot = g,
  width = 7.5,
  height = 9
)
