# Pystout
A Package To Make Publication Quality Latex Tables From Python Regression Output

This package has been tested with `statsmodels` `OLS` and `linearmodels` `OLS`, `IV2SLS` and `PanelOLS`. Current limitations are that it does not have full support for all relevant model statistics, though this will be added in future releases.

Current Issues:
1. No option to look for categorical variables (panel or time dummies) and say "Yes" or "No"
2. Currently treats "const" and "Intercept" as two separate variables if you mix and match `sm.OLS()` and `sm.OLS.from_formula()`, for example.

The normal use would be as follows (also in `testing_pystout.py`):

```
# Testing pystout
import statsmodels.api as sm
import linearmodels as ln
from pystout import pystout

dta = sm.datasets.webuse('auto')
dta.loc[:,'const'] = 1

y = dta.price

# =============================================================================
# First three models are from statsmodels
# =============================================================================
X = dta[['const','mpg','displacement']]
model1 = sm.OLS(y,X).fit()

X = dta[['const','mpg','displacement','turn']]
model2 = sm.OLS(y,X).fit()

X = dta[['displacement','const','turn']]
model3 = sm.OLS(y,X).fit()

# =============================================================================
# Next 2 are an ols and a tsls from linearmodels
# =============================================================================
X = dta[['displacement','const','turn','gear_ratio']]
model4 = ln.OLS(y,X).fit()

model5 = ln.IV2SLS(dependent=dta.price,endog=dta.mpg,
                   exog=dta.filter(['const','turn','displacement']),
                   instruments=dta.length).fit()

# =============================================================================
# Print result
# =============================================================================
pystout(models=[model1,model2,model3,model4,model5],
        file='testing/test_table.tex',
        addnotes=['Here is a little note','And another one'],
        digits=2,
        endog_names=['Custom','Header','Please','Thanks','Again'],
        varlabels={'const':'Constant','displacement':'Disp','mpg':'MPG'},
        addrows={'Test':['A','Test','Row','Here','Too']},
        mgroups={'Statsmodels':[1,3],'L OLS':4,'L TSLS':5},
        modstat={'nobs':'Obs','rsquared_adj':'Adj. R\sym{2}','fvalue':'F-stat'}
        )

```

Pystout has the following options:

    models:         A list of models to print.
                    Currenty must be fitted from statsmodels.OLS().fit()

    file:           This is the file name (including path) to write to.

    exogvars:       If none, pull all exogenous variable names.
                    These will be ordered in order of model (the constant will be put last).
                    If ordered list, then only pull these variables from each model, if exist.

    endog_names:    False generates numbered columns, True generates columns.
                    Based on the exog_names in the models, passing a list makes custom column names.

    varlabels:      Dictionary, or NoneType -- Custom labels for variables in table.
                    Works for exog/endog variables.

    stars:          Either False/None or a dictionary like: {.1:'+',.05:'*',.01:'**'}.

    digits:         Number of digits to round all items to (default=2).

    modstat:        You can add custom options from sm (F-stat, R-squared, Adjusted R-Squared)
                    Should be a dictionary of {'Name':'statsmodel statistic'}.
                    Currently only accepts: fvalue,rsquared,rsquared_adj,nobs

    addnotes:       Add notes to the bottom of the table.
                    (input is a list; each new element is a new line of comment).

    addrows:        Add a row to the bottom of the dataframe, these will be above stats.
                    Format is: {row name:[row,contents,as,list]}. (Default is an empty dictionary).
                    List must be the same dimension as models (to preserve columns)

    mgroups:        A dictionary that defines both the groups and what is in it.
                    For example, mgroups={'Group 1':1,'Group 2':[2,5],'':[6,8]}.
                    The keys are the group header (must be strings), and values are a list
                    (corresponding to the min and max) or integer that defines the regression
                    columns of group. You must specify a complete set of groups though
                    you can define one as blank (as shown) this will cause that section
                    to not have a header or a line underneath it.
