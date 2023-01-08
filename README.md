# Bioinspired Direct-Drive Legged Robot: Design Optimization of 5-bar Parallel Linkage Using OpenMDAO

The develop of quadrupedal robots and adaptable system control is becoming an increasing topic with the growing demand for using robot to explore unknown,
hazardous environment. In this project, we aim to improve the mobility of quadruped by lowering the inertia effect of parallel linkage limbs, namely, optimizing the length of the linkage to reduce the mass. 
However, there is a trade-off between the linkage length and the working space. We thus define an adjustable end-effector trajectory as our minimum working space basing on some of the leading-edge quadrupedal robot, 
ex: [Stanford Doggo](https://arxiv.org/abs/1905.04254), [Ghost Minitaur](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/9837/98370I/Gait-development-on-Minitaur-a-direct-drive-quadrupedal-robot/10.1117/12.2231105.short) 
and [MIT Cheetah](https://journals.sagepub.com/doi/full/10.1177/0278364917694244). To make both ends meet, we implement [OpenMDAO](https://openmdao.org/), which is an open-source framework for efficient multidisciplinary optimization, 
to produce our optimal design of parallel linkage.
