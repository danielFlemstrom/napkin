import sys
import datetime

from .overview import create_analysis_view
from .common import ga_report_view_css as css

def update_overall_analysis_view(results,outputdir):
    # Also create an overall analysis view
    tbl,raw = create_analysis_view(evaldata = results.copy(),
                               tableid="garesults")
    tbl = tbl.to_html(escape=False)
    pandas_css, ga_table = tbl.split("</style>")

    page_main_table = \
        f'''
        <table><tr>
                 <td style="vertical-align: top;"> </td>
                 <td>{ga_table}</td>
                 <tr><td colspan="2" style="text-align:right;"> View created: {datetime.datetime.now()}<td></tr>
        </table>
        '''
    # Mark out the Active Test Cases That Has Failed..
    fail_css = ""
    fail_template = '.nicetable .col_heading.colX {background-color: red;}'
    fails = results[results.tc_res != "Passed"]
    # display(fails)
    for f in set(fails['tc']):
        fail_css += fail_template.replace('X', str(raw.columns.get_loc(f)))

    page_style = f"{pandas_css} {css} {fail_css} </style>"
    page =  '<meta http-equiv="refresh" content="1">' +  page_style + page_main_table

    page = page.replace('id="T_garesults"','class="nicetable"')
    fname = outputdir + f"/ANALYSIS_overview.html".replace(" ","_").replace(":","-")
    with open( fname,"w") as f:
        f.write(page)
    print("Sessions Overview Created",fname)
