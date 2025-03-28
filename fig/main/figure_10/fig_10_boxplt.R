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
  mutate(profile=recode_factor(profile,"1"="Full slab","4"="Through"),
         noWood=recode_factor(noWood,"0"="without wood","1"="with wood"))
 # ####################################
 # # Boxplots of maximum forces between experiments without wood and with wood per profile
 # ####################################
 p2 <- ggplot(all_dat, aes(x=profile, y=Zzm,fill=as.factor(reorder(noWood, -Res))))+
   geom_boxplot(alpha=0.8)+
   theme_bw()+
   theme(legend.position="top",legend.text=element_text(size=20),text = element_text(size=20),axis.title.y = element_text(angle = 90, vjust = 0.5,size = 20),axis.text.x = element_text(angle = 0,hjust = 0.5, vjust = 0.5),axis.title.x = element_text(vjust = 0.5,size = 20),axis.title.y.right = element_text(angle = 0, vjust = 0.5))+
   scale_y_continuous(breaks = scales::breaks_extended(n = 5), limits = c(2,25))+
   labs( x="",y = expression(italic(F[Z][max])~" [N]"))+
   geom_vline(aes(xintercept=1.5),linetype="dashed",colour="black",size=0.7)+
   #scale_color_manual(values = c("#bdbdbd", "#A27146"),labels=c("without wood","with wood"), name = "")+
   scale_fill_manual(values = c("#A27146","#bdbdbd"),labels=c("with woody debris","without woody debris"), name = "")+
   coord_cartesian(clip = 'off') +
   annotation_custom(g1, x = 0.84, y = -4, ymax = 2.03, xmax = 1.16)+
   annotation_custom(g2, x = 1.84, y = -4, ymax = 2.03, xmax = 2.16)
 p2
 ggsave("fig/main/figure_10/Fzmax.png", plot = p2, device = png, height = 15, width = 22.5, dpi = 300, units = "cm")
 
 

 