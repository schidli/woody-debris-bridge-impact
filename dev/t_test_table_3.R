library(dplyr)

# Load data
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
# Function for testing for normal distribution and performing the appropriate test
perform_tests <- function(data, profile_value, dvariable) {
  # Filtern der Daten nach Profil
  data_profile <- data %>% filter(profile == profile_value)
  # Test for normal distribution for noWood=1 and noWood=0
  shapiro_noWood <- shapiro.test(data_profile[[dvariable]][data_profile$noWood == 0])
  shapiro_Wood <- shapiro.test(data_profile[[dvariable]][data_profile$noWood == 1])
  
  cat("\nShapiro-Wilk Test für profile =", profile_value, "und Wood:\n")
  print(shapiro_Wood)
  cat("\nShapiro-Wilk Test für profile =", profile_value, "und noWood:\n")
  print(shapiro_noWood)
  
  #  Decision based on the Shapiro-Wilk tests
  if (shapiro_Wood$p.value > 0.05 & shapiro_noWood$p.value > 0.05) {
    cat("\nBeide Gruppen sind normalverteilt. Durchführung des T-Tests für profile =", profile_value, ":\n")
    t_test_result <- t.test(data_profile[[dvariable]] ~ data_profile$noWood)
    print(t_test_result)
    return(t_test_result)
  } else {
    cat("\nMindestens eine Gruppe ist nicht normalverteilt. Durchführung des Mann-Whitney U-Tests für profile =", profile_value, ":\n")
    mann_whitney_result <- wilcox.test(data_profile[[dvariable]] ~ data_profile$noWood)
    print(mann_whitney_result)
    return(mann_whitney_result)
  }
}

# Tests for profile=1
test_result_profile_1 <- perform_tests(data, 1, dvariable)

# Tests for profile=4
test_result_profile_4 <- perform_tests(data, 4, dvariable)

# Function for outputting the results at alpha=0.05
print_test_results <- function(test_result, profile_value) {
  if ("statistic" %in% names(test_result)) {
    cat("\nErgebnisse des Tests für profile =", profile_value, "bei alpha = 0.05:\n")
    cat("Test-Statistik:", test_result$statistic, "\n")
    cat("p-Wert:", test_result$p.value, "\n")
    if (test_result$p.value < 0.05) {
      cat("Ergebnis: Signifikant (p < 0.05) - Nullhypothese ablehnen, die Mittelwerte/Verteilungen sind unterschiedlich.\n")
    } else {
      cat("Ergebnis: Nicht signifikant (p >= 0.05) - Nullhypothese nicht ablehnen, die Mittelwerte/Verteilungen sind gleich.\n")
    }
  }
}

# Profile=1
print_test_results(test_result_profile_1, 1)

# Profile=4
print_test_results(test_result_profile_4, 4)
