library(tidyverse)
library(ggplot2)
library(ggsci)

args      <- commandArgs(trailingOnly = TRUE)
data_file <- args[1]
pdf_file  <- args[2]

sources = list(
  "jolts" = "Openings - BLS JOLTS",
  "nlx" = "Job Postings - NLx Research Hub",
  "nlx_scaled" = "Job Postings (Scaled) - NLx Research Hub"
)

states <- c("CA", "TX", "FL", "NY", "PA")
openings <- read_csv(data_file)
data <- group_by(openings, year, month) %>%
  summarize(nlx = sum(nlx), jolts = sum(jolts)) %>%
  mutate(state = "National") %>%
  ungroup()

multiplier <- drop_na(data)
multiplier <- sum(multiplier$jolts) / sum(multiplier$nlx)
print(multiplier)

for (s in states) {
  data <- bind_rows(data, filter(openings, state == s))
}
print(unique(data$state))
states <- c("National", states)

data <- data %>%
  mutate(
    nlx_scaled = nlx * multiplier
  ) %>%
  pivot_longer(cols = c("nlx", "nlx_scaled", "jolts"), names_to = "source", values_to = "openings") %>%
  mutate(
    yrmo = as.Date(paste0(year, "-", month, "-01")),
    openings = openings / 1000,
    state = factor(state, levels = states),
    source = factor(source, levels = names(sources), labels = sources)
  )

g <- ggplot(data, aes(yrmo, openings, color = source)) +
  geom_line() +
  expand_limits(y = 0) +
  scale_color_npg() +
  guides(
    color = guide_legend(
      nrow = length(sources),
      byrow = TRUE,
      title = NULL
    )
  ) +
  labs(
    x = "Year/Month",
    y = "Openings (Thousands)"
  ) +
  theme_minimal() +
  theme(
    axis.line = element_line(size = 0.25, linetype = "solid", color = "black"),
    axis.ticks = element_line(),
    axis.title = element_text(size = 7),
    axis.text.x = element_text(size = 6),
    axis.text.y = element_text(size = 6),
    legend.position = "bottom",
    legend.text = element_text(size = 7),
    panel.grid = element_blank(),
    panel.grid.major.y = element_line(size = 0.125, linetype = "solid", color = "gray50"),
    strip.text.y = element_text(size = 7, hjust = 0, angle = 0)
  ) +
  facet_grid(state ~ ., scales = "free_y")

ggsave(
  filename = pdf_file,
  plot = g,
  width = 7.5,
  height = 9
)
