library(tidyverse)
library(ggplot2)
library(viridis)
library(gridExtra)

args               <- commandArgs(trailingOnly = TRUE)
socs_file          <- args[1]
soc_distance_files <- args[2:5]
pdf_file           <- args[6]

socs <- read_csv(socs_file) %>% mutate(soc2 = substr(soc, 1, 2))
soc_labels <- group_by(socs, soc2) %>% summarize(soc = first(soc)) %>% ungroup()

methods <- list(
  "euclidean"="Euclidean Similarity",
  "manhattan"="Manhattan Similarity",
  "cosine"="Cosine Similarity",
  "kl"="Kullback-Leibler Similarity"
)

plot <- do.call(grid.arrange, 
  lapply(
    seq(1, 4),
    function(i) {
      X <- read_csv(soc_distance_files[i]) %>%
        pivot_longer(cols = matches("\\d{6}", perl = TRUE), names_to = "soc2", values_to = "Similarity") %>%
        mutate(
          Similarity = -Similarity,
          soc1 = as.factor(soc),
          soc2 = as.factor(soc2),
          soc = NULL
        )

      ggplot(X, aes(soc2, soc1, fill=Similarity)) +
        geom_raster() + 
        scale_fill_gradientn(colours = viridis(256, option = "D")) +
        scale_x_discrete(breaks = soc_labels$soc, labels = soc_labels$soc2) +
        scale_y_discrete(breaks = soc_labels$soc, labels = soc_labels$soc2) +
        ggtitle(methods[[i]]) +
        labs(x = "SOC Code A", y = "SOC Code B") +
        theme(
          aspect.ratio = 1.0,
          axis.text.x = element_text(size = 5, angle = 90, vjust = 0.5),
          axis.text.y = element_text(size = 5)
        )
    }
  )
)

ggsave(
  filename = pdf_file,
  plot = plot,
  width = 15,
  height = 13.5
)
