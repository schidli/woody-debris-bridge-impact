library(dplyr)
library(ggpubr)
library(rstatix)

if (!requireNamespace("PMCMRplus", quietly = TRUE)) {
  install.packages("PMCMRplus")
}
library(PMCMRplus)

# Load data
data <- read.csv("dat/processed/data_all.csv",
                 header = T,
                 sep = ",",
                 dec = ".",
                 stringsAsFactors=FALSE)
profile_value=1
data_profile <- data %>% filter(profile == profile_value)
conover_result <- PMCMRplus::kwAllPairsConoverTest(h ~ factor(Wood), data = data_profile, p.adjust.method = "bonferroni")
print(conover_result)
dune_result<-dunn_test(h~Wood, data=data_profile, p.adjust.method = "bonferroni")
print(dune_result)
wilcox_result <-pairwise.wilcox.test(data_profile$h,data_profile$Wood,p.adjust="bonferroni")
print(wilcox_result)
wilcox_effect_result<-data_profile %>%
  wilcox_effsize(h~Wood) %>%
  as.data.frame()
print(wilcox_effect_result)




# Function for testing for normal distribution and performing the appropriate test
perform_tests <- function(data, profile_value) {
  # Filter data by profile
  data_profile <- data %>% filter(profile == profile_value)
  
  # Test for normal distribution for each Wood group
  shapiro_results <- data_profile %>%
    group_by(Wood) %>%
    summarise(p_value = shapiro.test(Zzm)$p.value)
  
  print(shapiro_results)
  
  # Decision based on the Shapiro-Wilk tests
  if (all(shapiro_results$p_value > 0.05)) {
    cat("\nAlle Gruppen sind normalverteilt. Durchführung der ANOVA für profile =", profile_value, ":\n")
    anova_result <- aov(Zzm ~ factor(Wood), data = data_profile)
    summary(anova_result)
    conover_result <- PMCMRplus::kwAllPairsConoverTest(Zzm ~ factor(Wood), data = data_profile, p.adjust.method = "bonferroni")
      print(conover_result)
      dune_result<-dunn_test(Zzm~Wood, data=data_profile, p.adjust.method = "bonferroni")
      print(dune_result)
      wilcox_result <-pairwise.wilcox.test(data_profile$Zzm,data_profile$Wood,p.adjust="bonferroni")
      print(wilcox_result)
      wilcox_effect_result<-data_profile %>%
        wilcox_effsize(Zzm~Wood) %>%
        as.data.frame()
      print(wilcox_effect_result)
    return(list(test_type = "ANOVA", result = anova_result))
  } else {
    cat("\nMindestens eine Gruppe ist nicht normalverteilt. Durchführung des Kruskal-Wallis-Tests für profile =", profile_value, ":\n")
    kruskal_result <- kruskal.test(Zzm ~ factor(Wood), data = data_profile)
    print(kruskal_result)
    
    if (kruskal_result$p.value < 0.05) {
      cat("\nKruskal-Wallis-Test ist signifikant. Durchführung des Conover-Iman-Post-Hoc-Tests für profile =", profile_value, ":\n")
      conover_result <- PMCMRplus::kwAllPairsConoverTest(Zzm ~ factor(Wood), data = data_profile, p.adjust.method = "bonferroni")
      print(conover_result)
      dune_result<-dunn_test(Zzm~Wood, data=data_profile, p.adjust.method = "bonferroni")
      print(dune_result)
      wilcox_result <-pairwise.wilcox.test(data_profile$Zzm,data_profile$Wood,p.adjust="bonferroni")
      print(wilcox_result)
      wilcox_effect_result<-data_profile %>%
        wilcox_effsize(Zzm~Wood) %>%
        as.data.frame()
      print(wilcox_effect_result)
      return(list(test_type = "Kruskal-Wallis", kruskal_result = kruskal_result, conover_result = conover_result))
    } else {
      return(list(test_type = "Kruskal-Wallis", kruskal_result = kruskal_result))
      
    }
  }
}

# Tests für profile=1
test_result_profile_1 <- perform_tests(data, 1)

# Tests für profile=4
test_result_profile_4 <- perform_tests(data, 4)
