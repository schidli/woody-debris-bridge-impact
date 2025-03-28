library("tidyverse")
library("patchwork")
library(png)
library(grid)
img1 <- readPNG("fig/symbols/Full_slab.png")
g1<- rasterGrob(img1, interpolate=TRUE)

img2 <- readPNG("fig/symbols/Trough.png")
g2<- rasterGrob(img2, interpolate=TRUE)

all_dat<- read.csv("dat/processed/data_all.csv",
                   header = T,
                   sep = ",",
                   dec = ".",
                   stringsAsFactors=FALSE) |>
  mutate(profile=recode_factor(profile,"1"="Full slab","4"="Through"))%>%
  arrange(Wood) %>%
  mutate(Wood = factor(Wood, levels=c("10", "15", "20", "0")))

 # ####################################
 # # Boxplots of maximum forces between experiments without wood and with wood per profile
 # ####################################
 p1 <- ggplot(all_dat, aes(x=profile, y=Yy,fill=as.factor(Wood)))+
   geom_boxplot(alpha=0.8)+
   theme_bw()+
   theme(legend.position="top",legend.text=element_text(size=20),text = element_text(size=20),axis.title.y = element_text(angle = 90, vjust = 0.5,size = 20),axis.text.x = element_text(angle = 0,hjust = 0.5, vjust = 0.5),axis.title.x = element_text(vjust = 0.5,size = 20),axis.title.y.right = element_text(angle = 0, vjust = 0.5))+
   scale_y_continuous(breaks = scales::breaks_extended(n = 5), limits = c(5,125))+
   labs( x="",y = expression(italic(F[Y][max])~" [N]"))+
   geom_vline(aes(xintercept=1.5),linetype="dashed",colour="black",size=0.7)+
   #scale_color_manual(values = c("#bdbdbd", "#A27146"),labels=c("without wood","with wood"), name = "")+
   scale_fill_manual(values = c("#fc4b0e","#fafa19","#0ebf4c","#bdbdbd"),labels=c("logs: 10 cm","logs: 15 cm","logs: 20 cm","no woody debris"), name = "")+
   coord_cartesian(clip = 'off') +
   annotation_custom(g1, x = 0.75, y = -8, ymax = -13, xmax = 1.25)+
   annotation_custom(g2, x = 1.75, y = -8, ymax = -13, xmax = 2.25)
 p1
 ggsave("fig/main/figure_12/Fymax_logs.png", plot = p1, device = png, height = 15, width = 22.5, dpi = 300, units = "cm")
 
 