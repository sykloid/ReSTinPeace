latex_document_template = '''\
\\documentclass[{font_size}]{{article}}

\\usepackage[latin1]{{inputenc}}
\\usepackage{{amsmath}}
\\usepackage{{amsfonts}}
\\usepackage{{amssymb}}
\\usepackage{{relsize}}

\\pagestyle{{empty}}

\\newsavebox{{\\formulabox}}
\\newlength{{\\formulawidth}}
\\newlength{{\\formulaheight}}
\\newlength{{\\formuladepth}}
\\setlength{{\\topskip}}{{0pt}}
\\setlength{{\\parindent}}{{0pt}}
\\setlength{{\\abovedisplayskip}}{{0pt}}
\\setlength{{\\belowdisplayskip}}{{0pt}}

\\begin{{lrbox}}{{\\formulabox}}
    $\\mathlarger{{{formula}}}$
\\end{{lrbox}}

\\settowidth{{\\formulawidth}}{{\\usebox{{\\formulabox}}}}
\\settoheight{{\\formulaheight}}{{\\usebox{{\\formulabox}}}}
\\settodepth{{\\formuladepth}}{{\\usebox{{\\formulabox}}}}

\\newwrite\\formula
\\immediate\\openout\\formula=\\jobname.depth
\\addtolength{{\\formuladepth}}{{1pt}}
\\immediate\\write\\formula{{\\the\\formuladepth}}
\\closeout\\formula

\\begin{{document}}
    \\usebox{{\\formulabox}}
\\end{{document}}
'''
