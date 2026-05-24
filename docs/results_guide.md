# Results Guide

Fig. 2 shows representative synthetic random-field realizations and their spectrum-driven structure.

Figs. 3-4 report relative distortion (RD), where zero means the method matches LX at the same discretization and seed. Positive values indicate higher SSE than LX.

Figs. 5-6 summarize computational time. Read these on log scales: slope reflects how strongly each method grows with discretization size R.

Fig. 7 overlays scaled analytical complexity curves with measured mean times. Agreement in slope is more important than absolute magnitude because Big-O ignores constants.

Fig. 8 compares iterations to CVT for Lloyd-family methods. Fewer iterations mean the initialization is closer to a stable tassellation.

Fig. 9 reports M1-M4, the PDF and autocorrelation error metrics. Lower values indicate quanta that better preserve one-point distributions and spatial dependence.

Figs. 2.8-2.14 belong to the seismic application. They compare Monte Carlo intensity-measure maps against weighted FQ-IDCVT quanta for exceedance probabilities and autocorrelation structure.
