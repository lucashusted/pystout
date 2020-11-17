import numpy as np
import pandas as pd

################################################################################
### A generic function for writing tables to tex with some customization
################################################################################
def tex_table(
    df, file, addnotes=[], mgroups={}, title='', label='',tableopts='',
    options=pd.DataFrame(),footnotesize='footnotesize'):
    '''
This function writes a table to file. The variable name column will just be the index of the dataframe provided. The column headers will be the column headers. The contents will be the contents of the table.

Inputs:
    df: This is the table you want to print

    name: This is the file name (including path) to write to

Options:

    addnotes: Add notes to the bottom of the table (input is a list; each new element is a new line of comment)

    mgroups: a dictionary that defines both the groups and what is in it. For example, mgroups={'Group 1':1,'Group 2':[2,5],'':[6,8]}. The keys are the group header (must be strings), and values are a list (corresponding to the min and max) or integer that defines the regression columns of group. You must specify a complete set of groups though you can define one as blank (as shown) this will cause that section to not have a header or a line underneath it.

    title: A Latex table caption that will be shown at the top of the table.

    label: A label to be used for refering to table in Latex, e.g. use \\ref{label} to refer to the table

    '''
    ###########################################################################
    ### Basic Setup
    ###########################################################################
    spacedict = {'footnotesize':25,'scriptsize':35,'tiny':45}
    if footnotesize not in spacedict.keys():
        print('This footnote size not recognized, defaulting to footnotesize')
        footnotesize = 'footnotesize'


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

    header = '\n'.join(['{',
                        '\def\sym#1{\ifmmode^{#1}\else\(^{#1}\)\\fi}',
                        '\\begin{tabular}{@{\extracolsep{2pt}}l*{%i}{c}@{}}' %df.shape[1],
                        '\hline\hline',
                        groupedcols,
                        groupedlines,
                        ''])

    # Basic header, with symbolic command stolen from estout (of stata)
    # We do extra column spacing just in case there is grouping of variables (adds a space)

    # Add footnotes (if any)
    footnotes = ['\multicolumn{%i}{l}{\\%s %s}' %(df.shape[1]+1,footnotesize,ii) for ii in addnotes]
    if footnotes:
        footnotes = ('\\vspace{-.%iem} \\\\\n' %spacedict[footnotesize]).join(footnotes)
        footnotes = [footnotes]
    footer = '\n'.join(['\hline\hline']+footnotes+['\end{tabular}','}'])

    if title and label:
        header = '\n'.join(['\\begin{table}[%s]' %tableopts,f'\caption{{{title}}}',
                            f'\label{{{label}}}',header])
    elif title and not label:
        header = '\n'.join(['\\begin{table}[%s]' %tableopts,f'\caption{{{title}}}',header])
    elif label and not title:
        header = '\n'.join(['\\begin{table}[%s]' %tableopts,f'\label{{{label}}}',header])

    if title or label:
        footer += '\n\end{table}'


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
def pystout(models, file, exogvars=None, endog_names=False,
            stars={.1:'+',.05:'*',.01:'**'}, varlabels=None,
            digits=2, scientific_notation=False, mgroups={},
            addnotes=[], addrows={}, title='', label='',tableopts='',
            modstat={
                'nobs':'N',
                'fvalue':'F-stat',
                'rsquared_adj':'Adj. R\sym{2}',
                'fvalue_robust':'F-stat (robust)',
                'rsquared_within':'R\sym{2} (Within)'
            },
            footnotesize='footnotesize'
            ):
    '''
This function needs to read in the relevant statistics to populate the table.
Then it needs to feed them to some version of tex_table. If no label or title are specified a
tabular object is returned. Otherwise, this tabular is wrapped in a table format for the title
and label to be included.

Inputs:
    models:         A list of models to print.
                    Currently must be fitted from statsmodels.OLS().fit() or linearmodels.

    file:           This is the file name (including path) to write to.

    exogvars:       If none, pull all exogenous variable names.
                    These will be ordered in order of model (the constant will be put last).
                    If ordered list, then only pull these variables from each model, if exist.

    endog_names:    False generates numbered columns, True generates columns.
                    Based on the index in params, passing a list makes custom column names.

    varlabels:      Dictionary, or NoneType -- Custom labels for variables in table.
                    Works for exog/endog variables.

    stars:          Either False/None or a dictionary like: {.1:'+',.05:'*',.01:'**'}.

    digits:         Number of digits to round all items to (default=2).

    scientific_notation:
                    If True scientific notation will be used if value is less than 10**(-digits)

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

    footnotesize:   Currently accepts 'footnotesize' or 'scriptsize' or 'tiny'.
                    Automatically compresses vertical space between separate footnotes.

    title:          A Latex table caption that will be shown at the top of the table.

    label:          A label to be used for referring to table in Latex, e.g. use \\ref{label} to refer to the table

    tableopts:      The options declared for the table as in \begin{table}[tableopts]


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

    # puller functions for model parameters and other singletons
    def trygetp(x,thing):
        try:
            y = thing[x]
        except:
            y = np.nan
        return y

    # this pulls in variables that come in symmetric matrix
    def trygetcov(x,m):
        if m.__module__.startswith('statsmodels'):
            try:
                y = m.cov_params().loc[x,x]**.5
            except:
                y = np.nan
        elif m.__module__.startswith('linearmodels'):
            try:
                y = m.cov.loc[x,x]**.5
            except:
                y = np.nan
        return y

    # this pulls in the relevant statistics from the model
    def trygetstat(x,model):
        if x=='nobs':
            try:
                y = str(int(model.nobs))
            except:
                y = ''
        elif x=='fvalue':
            if m.__module__.startswith('statsmodels'):
                try:
                    y = format_digform(model.fvalue)
                except:
                    y = ''
            elif m.__module__.startswith('linearmodels'):
                try:
                    y = format_digform(model.f_statistic.stat)
                except:
                    y = ''
        elif x=='rsquared':
            try:
                y = format_digform(model.rsquared)
            except:
                y = ''
        elif x=='rsquared_adj':
            try:
                y = format_digform(model.rsquared_adj)
            except:
                y = ''
        elif x=='fvalue_robust':
            try:
                y = format_digform(model.f_statistic_robust.stat)
            except:
                y = ''
        elif x=='rsquared_within':
            try:
                y = format_digform(model.rsquared_within)
            except:
                y = ''
        else:
            y = 'Not Programmed'
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

    # A function that returns formatted numbers
    def format_digform(stat):
        if (stat < 10**(-digits)) and scientific_notation:
            digform = "{:.%iE}" %digits
        else:
            digform = "{:.%if}" %digits
        return digform.format(stat)


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
            paramlist += m.params.index.to_list()

        # Get the unique values and keep them sorted in the old order
        indexes = np.unique(paramlist, return_index=True)[1]
        paramlist = [paramlist[index] for index in sorted(indexes)]

        if 'const' in paramlist:
            paramlist.append(paramlist.pop(paramlist.index('const')))
        elif 'Intercept' in paramlist:
            paramlist.append(paramlist.pop(paramlist.index('Intercept')))

    else:
        paramlist = exogvars

    # Making the inside of the table, currently does coef + se
    data = []
    for p in paramlist:
        r = []
        for m in models:
            cell = trygetp(p,m.params)
            if not np.isnan(cell):
                r.append(format_digform(cell) + starget(trygetp(p,m.pvalues)))
            else:
                r.append('')
        data.append(r)
        r = []
        for m in models:
            cell = trygetcov(p,m)
            if not np.isnan(cell):
                r.append('('+format_digform(cell)+')')
            else:
                r.append('')
        data.append(r)

    # Rownames differ from parameters cuz we need blank rows for SE, and we can relabel them
    rownames = [tryrelabel(p) for p in paramlist.copy()]
    for ii in range(1,2*len(rownames)+1,2):
        rownames.insert(ii,'')
    rownames = [x.replace('_','\_') for x in rownames]

    df = pd.DataFrame(data,columns=colnames,index=rownames)

    for key,value in addrows.items():
        df = df.append(pd.DataFrame([[str(v) for v in value]],index=[key],columns=df.columns))

    # Do stuff if there are model statistics to pull
    if modstat:
        options = pd.DataFrame()
        for key,value in modstat.items():
            r = []
            for m in models:
                r.append(trygetstat(key,m))
            options = options.append(pd.DataFrame([r],index=[value]))
    else:
        options = pd.DataFrame()

    # Run the code to update the table
    tex_table(df=df,file=file,addnotes=addnotes,mgroups=mgroups,title=title,label=label,
                tableopts=tableopts,options=options,footnotesize=footnotesize)
