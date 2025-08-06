
# WESTERN GOVERNORS UNIVERSITY

## D682 - Atmospheric Observations ML

--- 

## Overview:
  
This program uses a Linear Regression ML model to compare, and then extrapulate from the given columns  
of atmospheric data. Several optimization technics and evaluation metrics are delpoyed to create an accurate model.


Overall Structure:
- Retrieve data
- Sort based on Health Risk Score index (HRS)
- Calculate regression lines based on data columns
- Develop a regression line to mirror the HRS line
- Test ~ Evaluate ~ Amend
- Cycle later until satisfied

Testing Cycle:
- Train data
- Test data with current variables
- Alter variables with boosting function
- Evaluate results 

*By running main.py, this program analyzes the given data, giving weights to columns that more closely align with the  
desired metric (in   this case HRS). To adapt this model to another use case, the data being analyzed and csv reading  
functions would have to be altered to match the new files format. column and row information would have to be  
interchanged with the new data for the given problem. If ran with this new data, the model would be able to preform  
Linear Regression analysis and function just as the current program does.*

---

## Outcomes:
Original Model:
```
Average Error: 6.7068
Mean Absolute Percentage Error:  68.2 %
R-Squared:  0.46539002027071996
RMS Error:  71.42 
```
Optimized Model:
```
Average Error: 0.6599
Mean Absolute Percentage Error:  6.86 %
R-Squared:  0.5003
RMS Error:  0.7 
```
*  Before the optimization, the estimated values for each HRS are seen to have a large error, including a MAPE of 68.2%.  
After the use of weighted averaging, pruning, L1 and L2 regularization, quantization and boosting, the now trained  
model is observed to have reached lower error metrics of Average Error, RMSE, and MAPE (now with a score of 7.74%).  
Thus, the optimization techniques utilized are seen to provide a more accurate prediction proven by the lesser error margins.

---

## Future Optimizations:
 - better randomization for test/train row assignment
 - could alter boosting function: changing accuracy and time complexity
 - boosting could be configured more so off of best-fitting evaluation metrics
 
---

## Notes:
Air Quality Index = Health Index (without Misc data)  
Misc = DateTime data  
