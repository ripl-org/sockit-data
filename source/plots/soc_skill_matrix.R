library(tidyverse)
library(ggplot2)
library(viridis)

args           <- commandArgs(trailingOnly = TRUE)
socs_file      <- args[1]
skills_file    <- args[2]
soc_skill_file <- args[3]
pdf_file       <- args[4]

socs <- read_csv(socs_file) %>% mutate(soc2 = substr(soc, 1, 2))
soc_labels <- group_by(socs, soc2) %>% summarize(soc = first(soc)) %>% ungroup()

skills <- read_csv(skills_file)

X <- read.table(soc_skill_file, header=FALSE) * 1e-6
X$soc <- as.factor(socs$soc)

X <- pivot_longer(X, cols = starts_with("V"), names_to = "skill", values_to = "p") %>%
  mutate(skill = as.factor(skill), `Log Likelihood` = ifelse(p == 0, -15, log(p)))

plot <- ggplot(X, aes(skill, soc, fill=`Log Likelihood`)) +
  geom_raster() +
  scale_fill_gradientn(colours = viridis(256, option = "D")) +
  scale_y_discrete(breaks = soc_labels$soc, labels = soc_labels$soc2) +
  labs(x = "Skills (Alphabetical)", y = "SOC Code") +
  theme(
    aspect.ratio = nrow(skills) / nrow(socs),
    axis.text.x = element_blank(),
    axis.ticks.x = element_blank(),
    axis.text.y = element_text(size = 5)
  )

ggsave(
  filename = pdf_file,
  plot = plot,
  width = 7.5,
  height = 5.5
)
