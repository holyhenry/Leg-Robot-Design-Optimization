import numpy as np 
import matplotlib.pyplot as plt

DownAMP = 0.01
UpperAMP = 0.05
StanceHeight = 0.18
StepLength = 0.12

CurrentPercent = np.array([a/100+0.01 for a in range(100)])
StancePercent = 0.6
SwingPercent = 1 - StancePercent

x = np.zeros(len(CurrentPercent), dtype=float)
y = np.zeros(len(CurrentPercent), dtype=float)

for i in range(len(CurrentPercent)):
     if (CurrentPercent[i] <= StancePercent):
          x[i] = -(StepLength / 2) + (CurrentPercent[i] / StancePercent) * StepLength
          y[i] =  DownAMP * np.sin(np.pi * CurrentPercent[i] / StancePercent) + StanceHeight
     else:
          x[i] = (StepLength / 2) - ((CurrentPercent[i] - StancePercent) / SwingPercent) * StepLength
          y[i] = -UpperAMP * np.sin(np.pi * (CurrentPercent[i] - StancePercent) / SwingPercent) + StanceHeight

plt.plot(x,y)
plt.plot(x[99],y[99],x[79],y[79],x[59],y[59],x[29],y[29], marker='*')
# plt.title('SineTrajectory')
plt.ylim(0.195,0.125)
plt.grid()
plt.show()