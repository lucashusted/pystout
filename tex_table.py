def tex_table(df,file,digits=2,addnotes=[],mgroups={}):
    '''
    
    This function writes a table to file. The variable name column will just be the index of the dataframe provided. The column headers will be the column headers. The contents will be the contents of the table.
        
    Inputs:
        df: This is the table you want to print
        
        name: This is the file name (including path) to write to
        
    Options:
        
        digits: What the numbers in the table are rounded to, (default 2)
        
        addnotes: Add notes to the bottom of the table (input is a list; each new element is a new line of comment)
        
        mgroups: a dictionary that defines both the groups and what is in it. A complete specification would be an ordered dictionary from left to right of the form mgroups={'Group 1':1,'Group 2':[2,5],'':[6,8]} where the key is the group header, and values are a list (corresponding to the min and max) or numeric value are the regression(s) that encompass that group. You must specify a complete set of groups; you can have blank header names as shown, this will cause that section to not have a header or a line underneath it.
            
    '''
    ## Basic Setup
    
    # Setting up the format for the output num digits
    digform = "{:.%if}" %digits

    # If there are groupings
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
    
    
    ## Actually open it and write it
    tex = open(file, "w+")
    
    tex.write(header)
    tex.write(' & '.join([''] + df.columns.to_list())+
              '\n'.join([' \\\\','\hline','']))
    
    for ii in range(0,df.shape[0]):
        row = ' '.join([str(df.index[ii]),'& '])
        for jj in range(0,df.shape[1]):
            row += digform.format(df.iloc[ii,jj])
            if jj<df.shape[1]-1:
                row += ' & '
            else:
                row += '\n'.join([' \\\\',''])
        tex.write(row)

    tex.write(footer)
    tex.close()
    









### TESTING!
import numpy as np
import pandas as pd

df = pd.DataFrame(np.random.uniform(0,10,size=[8,6]))
df.index = ['Variable 1','','Variable 2','','Variable 3','','Variable 4','']
df.columns = ['(1)','(2)','(3)','(4)','(5)','(6)']


tex_table(df,'/Users/whiskey/Desktop/penis.tex',digits=3,mgroups={'Group 1':1,'':2,'Group 2':[3,5],'Group 3':6},addnotes=['a note','and another one'])