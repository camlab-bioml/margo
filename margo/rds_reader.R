local({r <- getOption("repos")
       r["CRAN"] <- "http://cran.r-project.org" 
       options(repos=r)
})
if("argparse" %in% rownames(installed.packages()) == FALSE) {install.packages("argparse")}
if("SingleCellExperiment" %in% rownames(installed.packages()) == FALSE) {
  if("BiocManager" %in% rownames(installed.packages()) == FALSE) {install.packages("BiocManager")}
  BiocManager::install("SingleCellExperiment")
}
if("Seurat" %in% rownames(installed.packages()) == FALSE) {install.packages("Seurat")}

suppressPackageStartupMessages({
  library(Seurat)
  library(SingleCellExperiment)
  library(argparse)
})
options(warn=-1)

parser <- ArgumentParser(description='Input .rds file to be processed')
parser$add_argument('rds_in', type='character', help='input rds file')
parser$add_argument('csv_out', type='character', help='output csv file')
args <- parser$parse_args()

rds <- readRDS(args$rds_in)

features = NULL
if (class(rds) == "SingleCellExperiment") {features = t(rownames(rds))}
if (class(rds) == "Seurat") {features <- t(rownames(rds@raw.data))}
# print(features)
write.csv(features, args$csv_out, row.names=TRUE)


# Rscript rds_reader.R ../tests/test-data/test_rds.rds ../tests/test-data/test_rds.csv
