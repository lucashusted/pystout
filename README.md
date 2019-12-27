# Pystout
A Package To Make Publication Quality Latex Tables From Python Regression Output

Current Issues:
1. No option to add custom rows to the table (forthcoming).
2. No option to look for categorical variables (panel or time dummies) and say "Yes" or "No"
3. This package has been tested with `statsmodels.api.OLS` but not with any other related types of models.

The normal use would be as follows:

```
import statsmodels.api as sm
import pystout
from pystout import pystout

dta = sm.datasets.webuse('auto')

X = sm.add_constant(dta[['mpg','displacement']])

y = dta.price
model1 = sm.OLS(y,X).fit()

X = sm.add_constant(dta[['mpg','displacement','turn']])
model2 = sm.OLS(y,X).fit()

X = sm.add_constant(dta[['displacement','turn']])
model3 = sm.OLS(y,X).fit()


pystout(models=[model1,model2,model3],
        file='testing/test_table.tex',
        addnotes=['Here is a little note'],
        digits=2,
        endog_names=['Custom','Header','Please'],
        varlabels={'const':'Constant','displacement':'Disp','mpg':'MPG'}
        )
```

Pystout takes the following inputs:

Inputs:
    models:         You need to provide a list of models to print.
                    Currenty must be fitted from statsmodels.OLS().fit()
                    
    file:           This is the file name (including path) to write to

    exogvars:       If none, pull all exogenous variable names.
                    These will be ordered in order of model (the constant will be put last).
                    If ordered list, then only pull these variables from each model, if exist.

    endog_names:    False generates numbered columns, True generates columns
                    based on the exog_names in the models, passing a list makes
                    custom column names.

    varlabels:      Dictionary, or NoneType -- Custom labels for variables in table.
                    Works for exog/endog variables.

    stars:          Either False/None or a dictionary like: {.1:'+',.05:'*',.01:'**'}.

    digits:         Number of digits to round all items to (default=2).

    modstat:        You can add a custom options from sm (F-stat, R-squared, Adjusted R-Squared)
                    Should be a dictionary of {'Name':'statsmodel statistic'}.
                    Currently only accepts: fvalue,rsquared,rsquared_adj,nobs
    
    addnotes:       Add notes to the bottom of the table
                    (input is a list; each new element is a new line of comment).

    mgroups:        A dictionary that defines both the groups and what is in it.
                    For example, mgroups={'Group 1':1,'Group 2':[2,5],'':[6,8]}. 
                    The keys are the group header (must be strings), and values are a list
                    (corresponding to the min and max) or integer that defines the regression 
                    columns of group. You must specify a complete set of groups though 
                    you can define one as blank (as shown) this will cause that section 
                    to not have a header or a line underneath it.
