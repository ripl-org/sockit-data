library(tidyverse)
library(ggplot2)
library(ggsci)

args      <- commandArgs(trailingOnly = TRUE)
data_file <- args[1]
pdf_file  <- args[2]

sources <- list(
  "acs_all" = "Employment (All) - American Community Survey",
  "acs_fulltime" = "Employment (Full-time) - American Community Survey",
  "oes" = "Employment - Occupational Employment and Wage Statistics",
  "nlx" = "Job Postings - NLx Research Hub"
)

data <- read_csv(data_file) %>%
  mutate(
    acs_all = 100.0 * acs_all / sum(acs_all),
    acs_fulltime = 100.0 * acs_fulltime / sum(acs_fulltime),
    oes = 100.0 * oes / sum(oes),
    nlx = 100.0 * nlx / sum(nlx),
  ) %>%
  pivot_longer(cols = names(sources), names_to = "source", values_to = "percent") %>%
  mutate(
    label = as.factor(paste(soc2, acs_label)),
    soc2 = NULL,
    acs_label = NULL,
    year = as.factor(year),
    source = factor(source, levels = rev(names(sources)), labels = rev(sources))
  )

print(head(data))

ymax <- as.integer(max(data$percent)) + 2

g <- ggplot(data, aes(source, percent, fill = source)) +
  geom_col(width = 0.75) +
  coord_flip() +
  scale_x_discrete(limits = rev) +
  scale_y_continuous(
    breaks = seq(0, ymax),
    labels = sapply(seq(0, ymax), function(y) { paste0(y, "%") })
  ) +
  scale_fill_npg() +
  guides(
    fill = guide_legend(
      nrow = length(sources),
      byrow = TRUE,
      title = NULL
    )
  ) +
  theme_minimal() +
  theme(
    axis.title = element_blank(),
    axis.text.x = element_text(size = 6, angle = 90),
    axis.text.y = element_blank(),
    axis.ticks.y = element_blank(),
    legend.position = "bottom",
    legend.text = element_text(size = 7),
    panel.grid = element_blank(),
    panel.grid.major.x = element_line(color = "gray70", size = 0.125, linetype = 1),
    strip.text.x = element_text(size = 10, hjust = 0),
    strip.text.y = element_text(size = 7, hjust = 0, angle = 0)
  ) +
  facet_grid(label ~ year)

ggsave(
  filename = pdf_file,
  plot = g,
  width = 7.5,
  height = 9
)
