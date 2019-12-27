import numpy as np
import pandas as pd

################################################################################
### A generic function for writing tables to tex with some customization
################################################################################
def tex_table(df,file,addnotes=[],mgroups={},options=pd.DataFrame()):
    '''
This function writes a table to file. The variable name column will just be the index of the dataframe provided. The column headers will be the column headers. The contents will be the contents of the table.

Inputs:
    df: This is the table you want to print

    name: This is the file name (including path) to write to

Options:

    addnotes: Add notes to the bottom of the table (input is a list; each new element is a new line of comment)

    mgroups: a dictionary that defines both the groups and what is in it. For example, mgroups={'Group 1':1,'Group 2':[2,5],'':[6,8]}. The keys are the group header (must be strings), and values are a list (corresponding to the min and max) or integer that defines the regression columns of group. You must specify a complete set of groups though you can define one as blank (as shown) this will cause that section to not have a header or a line underneath it.

    '''
    ###########################################################################
    ### Basic Setup
    ###########################################################################
    # If there are groupings, then we iterate through them
    groupedcols = ''
    groupedlines = ''
    if mgroups:
        for key,value in mgroups.items():
            if key:
                if type(value)==int:
                    groupedcols += '& \multicolumn{1}{c}{%s} ' %key
                    groupedlines += '\cline{%s-%s}\n' %(str(value+1),str(value+1))
                elif type(value)==list:
                    groupedcols += '& \multicolumn{%i}{c}{%s} ' %(len(range(value[0],value[1]+1)),key)
                    groupedlines += '\cline{%s}\n' %('-'.join([str(i+1) for i in value]))
            else:
                if type(value)==int:
                    groupedcols += '& '
                elif type(value)==list:
                    groupedcols += '& '*len(range(value[0],value[1]+1))
        groupedcols += '\\\\'
        groupedlines = groupedlines[:-1]

    # Basic header, with symbolic command stolen from estout (of stata)
    # We do extra column spacing just in case there is grouping of variables (adds a space)
    header = '\n'.join(['{',
                        '\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\\fi}',
                        '\\begin{tabular}{@{\extracolsep{2pt}}l*{%i}{c}@{}}' %df.shape[1],
                        '\hline\hline',
                        groupedcols,
                        groupedlines,
                        ''])

    # Add footnotes (if any)
    footnotes = []
    if addnotes:
        for ii in addnotes:
            footnotes += ['\multicolumn{%i}{l}{\\footnotesize %s} \\\\' %(df.shape[1]+1,ii)]

    footer = '\n'.join(['\hline\hline']+footnotes+['\end{tabular}','}'])


    ###########################################################################
    ### Open and write it
    ###########################################################################
    tex = open(file, "w+")

    tex.write(header)
    tex.write(' & '.join([''] + df.columns.to_list())+
              '\n'.join([' \\\\','\hline','']))

    for ii in range(0,df.shape[0]):
        row = ' '.join([str(df.index[ii]),'& '])
        for jj in range(0,df.shape[1]):
            row += str(df.iloc[ii,jj])
            if jj<df.shape[1]-1:
                row += ' & '
            else:
                row += '\n'.join([' \\\\',''])
        tex.write(row)

    if options.empty==False:
        tex.write('\n\hline\n')
        for ii in range(0,options.shape[0]):
            row = ' '.join([str(options.index[ii]),'& '])
            for jj in range(0,options.shape[1]):
                row += str(options.iloc[ii,jj])
                if jj<options.shape[1]-1:
                    row += ' & '
                else:
                    row += '\n'.join([' \\\\',''])
            tex.write(row)



    tex.write(footer)
    tex.close()




################################################################################
### The output functon for statsmodels
################################################################################
def pystout(models,file,exogvars=None,endog_names=False,stars={.1:'+',.05:'*',.01:'**'},
            varlabels=None,digits=2,mgroups={},addnotes=[],
            modstat={'nobs':'N','fvalue':'F-stat','rsquared_adj':'Adj. R\sym{2}'}):
    '''
This function needs to read in the relevant statistics to populate the table.
Then it needs to feed them to some version of tex_table

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

Output:
    file:           The filename you want to write to, including path (should end with '.tex')

    '''
    # ==========================================================================
    # Helper Functions
    # ==========================================================================
    # A label helper function
    def tryrelabel(x,labeldict=varlabels):
        try:
            y = labeldict[x]
        except:
            y = x
        return y
    # puller function for model parameters
    def trygetp(x,thing):
        try:
            y = thing[x]
        except:
            y = np.nan
        return y
    def trygetcov(x,thing):
        try:
            y = thing.loc[x,x]**.5
        except:
            y = np.nan
        return y
    # A function to convert p-values to stars (see outtable custom function)
    def starget(x,stars=stars):
        y = ''
        if stars and x:
            sorted(stars,reverse=True)
            for k in stars.keys():
                if x<=k:
                    y = r'\sym{%s}' %stars[k]
        return y

    # The format of the numbers in the table
    digform = "{:.%if}" %digits

    # Define column headers (3 cases)
    cols = len(models)
    if endog_names==False:
        colnames = ['(%s)' %c for c in range(1,cols+1)]
    elif type(endog_names)==list:
        colnames = endog_names
    elif endog_names==True:
        colnames = [tryrelabel(m.model.endog_names) for m in models]

    # Get parameters to pull (2 cases)
    paramlist = []
    if not exogvars:
        for m in models:
            paramlist += m.model.exog_names.copy()

        # Get the unique values and keep them sorted in the old order
        indexes = np.unique(paramlist, return_index=True)[1]
        paramlist = [paramlist[index] for index in sorted(indexes)]

        if 'const' in paramlist:
            paramlist.append(paramlist.pop(paramlist.index('const')))
    else:
        paramlist = exogvars

    # Making the inside of the table, currently does coef + se
    data = []
    for p in paramlist:
        r = []
        for m in models:
            cell = trygetp(p,m.params)
            if not np.isnan(cell):
                r.append(digform.format(cell) + starget(trygetp(p,m.pvalues)))
            else:
                r.append('')
        data.append(r)
        r = []
        for m in models:
            cell = trygetcov(p,m.cov_params())
            if not np.isnan(cell):
                r.append(digform.format(cell))
            else:
                r.append('')
        data.append(r)

    # Rownames differ from parameters cuz we need blank rows for SE, and we can relabel them
    rownames = [tryrelabel(p) for p in paramlist.copy()]
    for ii in range(1,2*len(rownames)+1,2):
        rownames.insert(ii,'')

    df = pd.DataFrame(data,columns=colnames,index=rownames)
    
    # Do stuff if there are model statistics to pull
    if modstat:
        options = pd.DataFrame()
        for key,value in modstat.items():
            r = []
            for m in models:
                if key=='nobs':
                    cell = str(int(m.nobs))
                elif key=='fvalue':
                    cell = digform.format(m.fvalue)
                elif key=='rsquared':
                    cell = digform.format(m.rsquared)
                elif key=='rsquared_adj':
                    cell = digform.format(m.rsquared_adj)
                r.append(cell)
            options = options.append(pd.DataFrame([r],index=[value]))
    else:
        options = pd.DataFrame()

    tex_table(df=df,file=file,addnotes=addnotes,mgroups=mgroups,options=options)
