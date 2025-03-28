## Grainsize distribution
library(ggplot2)
require(scales)
require(MASS)

## read data-------------------------------------------------------------
granular <- read.csv("fig/main/figure_2/granular2024.csv",
                     header = T,
                     sep = ";",
                     dec = ",",
                     stringsAsFactors=FALSE)
granular.dm <- granular[1:25,1]
granular.proz <- granular[1:25,2]*100
granular <- data.frame(granular.dm,granular.proz)



## Plot-------------------------------------------------------------
# granular ---------------

p1<- ggplot(data = granular, 
       aes(x = granular.dm, y=granular.proz))+ 
  geom_line(aes(y=granular.proz),linetype=1,lwd=1,color = "black")+
  #geom_line(aes(y=viskos.proz, color="seagreen4"),linetype=1,lwd=1)+
  
  annotation_logticks(sides="b")+
  scale_x_continuous(trans = 'log10',
                     breaks = c(0.0001,0.001,0.01,0.1,1,10,100),
                     labels = as.character(c(0.0001,0.001,0.01,0.1,1,10,100)))+
  #scale_y_continuous(breaks = c(seq(0,1,0.1)))+
  geom_vline(xintercept = c(0.002,0.063,2),linetype=3)+
  geom_vline(xintercept = c(2,4,8,10,22.4),linetype=2)+
  annotate(geom = "rect", xmin = 0.0002, xmax = 2, ymin = 0, ymax = 100,
           fill = "#f0b27a", alpha = 0.4) +
  annotate(geom = "rect", xmin = 2, xmax = 4, ymin = 0, ymax = 100,
           fill = "#e59866", alpha = 0.4) +
  annotate(geom = "rect", xmin = 4, xmax = 8, ymin = 0, ymax = 100,
           fill = "#dc7633", alpha = 0.4) +
  annotate(geom = "rect", xmin = 8, xmax = 10, ymin = 0, ymax = 100,
           fill = "#ca6f1e", alpha = 0.5) +
  annotate(geom = "rect", xmin = 10, xmax = 22.4, ymin = 0, ymax = 100,
           fill = "#6e2c00", alpha = 0.5) +
  theme_bw()+
  theme(legend.position ="",panel.grid.minor.y=element_blank(),text = element_text(size=15),axis.title.y = element_text(angle = 90, vjust = 0.5,size = 15),axis.title.x = element_text(vjust = 0.5,size = 15))+
  labs(x = "Particle size [mm]", y = "Percent finer [%]")
ggsave("gsd.png", plot = p1, device = png, height = 10, width = 16, dpi = 300, units = "cm")

