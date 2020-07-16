# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 14:42:46 2019

@author: DATAmadness
"""

##################################################
# A function that will accept a pandas dataframe
# and auto-transforms columns that exceeds threshold value
#  -  Offers choice between boxcox or log / exponential transformation
#  -  Automatically handles negative values
#  -  Auto recognizes positive /negative skewness

# Further documentation available here:
# https://datamadness.github.io/Skewness_Auto_Transform




import seaborn as sns
import numpy as np
import math
import scipy.stats as ss
import matplotlib.pyplot as plt
from IPython.display import display, Markdown, Latex

def skew_autotransform(DF, include = None, exclude = None, plot = False, threshold = 1, exp = False):
    
    #Get list of column names that should be processed based on input parameters
    if include is None and exclude is None:
        colnames = DF.columns.values
    elif include is not None:
        colnames = include
    elif exclude is not None:
        colnames = [item for item in list(DF.columns.values) if item not in exclude]
    else:
        print('No columns to process!')
    
    #Helper function that checks if all values are positive
    def make_positive(series):
        minimum = np.amin(series)
        #If minimum is negative, offset all values by a constant to move all values to positive teritory
        if minimum <= 0:
            series = series + abs(minimum) + 0.01
        return series
    
    
    #Go throug desired columns in DataFrame
    for col in colnames:
        #Get column skewness
        skew = DF[col].skew()
        transformed = True
        
        if plot:
            #Prep the plot of original data
            #sns.set_style("white")
            plt.style.use('fivethirtyeight')
            sns.set_palette("Blues_r")
            fig, axes = plt.subplots(1, 2, figsize=(10, 5))
            ax1 = sns.distplot(DF[col], ax=axes[0])
            
            ax1.set_xlabel('Original ' + col, fontsize = 12)

            
        
        #If skewness is larger than threshold and positively skewed; If yes, apply appropriate transformation
        if abs(skew) > threshold and skew > 0:
            skewType = 'positive'
            #Make sure all values are positive
            DF[col] = make_positive(DF[col])
            
            if exp:
               #Apply log transformation 
               DF[col] = DF[col].apply(math.log)
            else:
                #Apply boxcox transformation
                DF[col] = ss.boxcox(DF[col])[0]
            skew_new = DF[col].skew()
         
        elif abs(skew) > threshold and skew < 0:
            skewType = 'negative'
            #Make sure all values are positive
            DF[col] = make_positive(DF[col])
            
            if exp:
               #Apply exp transformation 
               DF[col] = DF[col].pow(10)
            else:
                #Apply boxcox transformation
                DF[col] = ss.boxcox(DF[col])[0]
            skew_new = DF[col].skew()
        
        else:
            #Flag if no transformation was performed
            transformed = False
            skew_new = skew
        
        #Compare before and after if plot is True
        if plot:
            display(Markdown('------------------------------------------------------')  )   
            if transformed:
                
                display(Markdown('**%s had %s skewness of %2.2f**' %(str(col), str(skewType), skew)))
                display(Markdown('**Transformation yielded skewness of %2.2f**' %(skew_new)))
                sns.set_palette("Set2")

                ax2 = sns.distplot(DF[col], ax=axes[1], color = 'r')
                ax2.set(xlabel='Transformed ' + col)
                ax2.set_xlabel('Transformed ' + col, fontsize = 12)

                
                plt.show()
            else:
                display(Markdown('**NO TRANSFORMATION APPLIED FOR %s . Skewness = %2.2f**' %(col, skew)))
                sns.set_context("paper", rc={"font.size":5,"axes.titlesize":5,"axes.labelsize":3})   

                ax2 = sns.distplot(DF[col], ax=axes[1])
                ax2.set_xlabel('Transformed ' + col, fontsize = 12)
                
                plt.show()
                
                

    return DF





