import pandas as pd
import datetime
import sys

from .common import ga_report_view_css as css
from .common import res_url_formatter, highlight_results

# -------------------------------------------------------------------------------------------
#                                  create_analysis_view
# -------------------------------------------------------------------------------------------


def create_analysis_view(evaldata, tableid="garesults"):

    evaldata["req"] = evaldata["req"].map(lambda x: x.replace("SR_C30_SRS_Safe-", ""))
    evaldata["tc"] = evaldata["tc"].map(lambda x: x.replace("-DriveBrake-S", ""))

    evaldata.rename(
        {
            "session": "Execution Log",
            "req": "Requirement",
            "tc": "Log Source <br>(Active Test Case)",
            "ga": "Passive Test Case",
        },
        axis=1,
        inplace=True,
    )

    if len(set(evaldata["Execution Log"].values)) > 1:
        evaldata = evaldata.set_index(
            [
                "Requirement",
                "Passive Test Case",
                "Log Source <br>(Active Test Case)",
                "Execution Log",
            ]
        )
    else:
        evaldata = evaldata.set_index(
            ["Requirement", "Passive Test Case", "Log Source <br>(Active Test Case)"]
        )

    # evaldata = evaldata.set_index(['req','ga','tc'])

    tbl = evaldata.unstack("Log Source <br>(Active Test Case)")["res"]
    # tbl = evaldata.unstack('Passive Test Case')['res']
    tbl = tbl.applymap(res_url_formatter)

    style_tbl = tbl.style.applymap(highlight_results)
    style_tbl.set_uuid("garesults")

    return style_tbl, tbl


# -------------------------------------------------------------------------------------------
#                                  create_view_menu
# -------------------------------------------------------------------------------------------


def create_view_menu(evaldata, outputdir):
    view_menu = """ <table class="nicetable">
        <tr style="text-align:center;" >
            <td ><h3> Execution Logs </h3></td>
            <td ><h3> # Fails </h3></td>
        </tr>\n          
    """
    for sname, grp in evaldata.groupby("session"):
        fails = len(grp[grp["ga_res"].map(lambda x: "F" in x)]["ga_res"])

        fname = outputdir + f"/ANALYSIS_view-{sname}.html".replace(" ", "_").replace(
            ":", "-"
        )
        view_menu += f'    <tr><td><a href={fname[1:]}> {sname}</a></td> <td style="color:red"> {fails} </td></tr>\n'

    view_menu = view_menu + "</table>\n"

    return view_menu


# -------------------------------------------------------------------------------------------
#                                  update_all_analysis_views
# -------------------------------------------------------------------------------------------


def update_all_analysis_views(results, outputdir):
    for sname, grp in results.groupby("session"):

        tbl, raw = create_analysis_view(evaldata=grp, tableid="garesults")
        tbl = tbl.to_html(escape=False)

        pandas_css, ga_table = tbl.split("</style>")

        # Mark out the Active Test Cases That Has Failed..
        fail_css = ""
        fail_template = ".nicetable .col_heading.colX {background-color: red;}"
        fails = grp[grp.tc_res != "Passed"]
        # For test we include  Tcs
        # fails = grp[grp['Log Source <br>(Active Test Case)'] == "TC-011"]
        for f in set(fails["Log Source <br>(Active Test Case)"]):
            fail_css += fail_template.replace("X", str(raw.columns.get_loc(f)))

        page_style = f"{pandas_css} {css} {fail_css} </style>"

        page_main_table = f"""
            <table><tr>
                     <td style="vertical-align: top;">{create_view_menu(results,outputdir)}</td>
                     <td>{ga_table}</td>
                     <tr><td colspan="2" style="text-align:right;"> View created: {datetime.datetime.now()}<td></tr>
            </table>
            """
        page = '<meta http-equiv="refresh" content="1">' + page_style + page_main_table

        page = page.replace('id="T_garesults"', 'class="nicetable"')

        fname = outputdir + f"/ANALYSIS_view-{sname}.html".replace(" ", "_").replace(
            ":", "-"
        )
        with open(fname, "w") as f:
            f.write(page)
        print("Overview Created: ", fname)
