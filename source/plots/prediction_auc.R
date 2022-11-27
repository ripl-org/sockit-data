library(tidyverse)
library(ggplot2)
library(ggsci)
library(gridExtra)

args      <- commandArgs(trailingOnly = TRUE)
data_file <- args[1]
pdf_file  <- args[2]

data <- read_csv(data_file)

# Drop models with low N of true positive
data <- data %>%
  filter(n >= 10) %>%
  mutate(
    group = as.factor(case_when(
      n > 1000 ~ "1000+",
      n > 100  ~ "100-999",
      TRUE     ~ "10-99"
    )),
    logn = log10(n)
  )

# Plot N vs test AUC
g1 <- ggplot(data, aes(logn, test_auc, group = group, color = group)) +
  geom_point(shape = 1) +
  expand_limits(y = 0) +
  scale_color_npg() +
  guides(
    color = guide_legend(
      title = NULL
    )
  ) +
  labs(
    x = "log10(# of True Positives)",
    y = "Test AUC"
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
  )

# Plot validation AUC vs test AUC
g2 <- ggplot(data, aes(valid_auc, test_auc, group = group, color = group)) +
  geom_point(shape = 1) +
  expand_limits(x = 0, y = 0) +
  scale_color_npg() +
  guides(
    color = guide_legend(
      title = NULL
    )
  ) +
  labs(
    x = "Validation AUC",
    y = "Test AUC"
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
  )

# Save plot
ggsave(
  filename = pdf_file,
  plot = grid.arrange(g1, g2, nrow = 1),
  width = 7.5,
  height = 4.5
)
