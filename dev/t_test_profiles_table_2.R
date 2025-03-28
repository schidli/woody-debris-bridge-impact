# Laden der notwendigen Bibliothek
library(dplyr)

# Daten einlesen
data <- read.csv("dat/processed/data_all.csv",
                 header = T,
                 sep = ",",
                 dec = ".",
                 stringsAsFactors=FALSE)
# define depended variable
# FYmax--> Yy
# FZmin --> Zz
# FZmax --> Zzm
dvariable<-"Yy"

# Funktion zum Testen auf Normalverteilung und Durchführen des geeigneten Tests
perform_tests <- function(data, noWood_value, dvariable) {
  # Filtern der Daten nach Profil
  data_profile <- data %>% filter(noWood == noWood_value)
  
  # Test auf Normalverteilung für noWood=1 und noWood=0
  shapiro_profile_1 <- shapiro.test(data_profile[[dvariable]][data_profile$profile == 1])
  shapiro_profile_4 <- shapiro.test(data_profile[[dvariable]][data_profile$profile == 4])
  
  cat("\nShapiro-Wilk Test für woody =", noWood_value, "und profile=1:\n")
  print(shapiro_profile_1)
  cat("\nShapiro-Wilk Test für woody =", noWood_value, "und profile=4:\n")
  print(shapiro_profile_4)
  
  # Entscheidung basierend auf den Shapiro-Wilk Tests
  if (shapiro_profile_1$p.value > 0.05 & shapiro_profile_4$p.value > 0.05) {
    cat("\nBeide Gruppen sind normalverteilt. Durchführung des T-Tests für wood =", noWood_value, ":\n")
    t_test_result <- t.test(data_profile[[dvariable]] ~ data_profile$profile)
    print(t_test_result)
    return(t_test_result)
  } else {
    cat("\nMindestens eine Gruppe ist nicht normalverteilt. Durchführung des Mann-Whitney U-Tests für wood =", noWood_value, ":\n")
    mann_whitney_result <- wilcox.test(data_profile[[dvariable]] ~ data_profile$profile)
    print(mann_whitney_result)
    return(mann_whitney_result)
  }
}

# Tests für noWood=0
test_result_wood_0 <- perform_tests(data, 0, dvariable)

# Tests für noWood=1
test_result_wood_1 <- perform_tests(data, 1, dvariable)

# Funktion zur Ausgabe der Ergebnisse bei alpha=0.05
print_test_results <- function(test_result, noWood_value) {
  if ("statistic" %in% names(test_result)) {
    cat("\nErgebnisse des Tests für wood =", noWood_value, "bei alpha = 0.05:\n")
    cat("Test-Statistik:", test_result$statistic, "\n")
    cat("p-Wert:", test_result$p.value, "\n")
    if (test_result$p.value < 0.05) {
      cat("Ergebnis: Signifikant (p < 0.05) - Nullhypothese ablehnen, die Mittelwerte/Verteilungen sind unterschiedlich.\n")
    } else {
      cat("Ergebnis: Nicht signifikant (p >= 0.05) - Nullhypothese nicht ablehnen, die Mittelwerte/Verteilungen sind gleich.\n")
    }
  }
}

# Ergebnisse für noWood=0
print_test_results(test_result_wood_0, 0)

# Ergebnisse für noWood=1
print_test_results(test_result_wood_1, 1)