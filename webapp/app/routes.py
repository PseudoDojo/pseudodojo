from app import app
from flask import render_template, jsonify, request
from flask_cors import cross_origin

from .forms import FormatForm

import tempfile
import requests
import warnings

from abipy.ppcodes.oncv_parser import OncvParser
from abipy.tools.plotting import mpl_to_ply

@app.route('/')
@app.route('/index')
def index():
    form = FormatForm()

    return render_template('index.html', form=form)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contribute')
def contribute():
    return render_template('contribute.html')

@app.route('/direct_table_test')
def direct_table_test():
    return render_template('direct_table_test.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/paperlist')
def paperlist():
    return render_template('paperlist.html')

@app.route('/papers')
def papers():
    return render_template('papers.html')

@app.route('/abinintsitepage')
def abinintsitepage():
    return render_template('abinintsitepage.html')


@app.route("/process_outfile", methods=["POST"])
def process_outfile():
    fname = request.form["fname"]
    
    headers = {'Authorization': f'token {app.config["GITHUB_TOKEN"]}'}

    out_file = requests.get(fname, headers=headers).text
    site_title = fname.split("/")[-1]

    return render_template("inout_files.html", file=out_file, site_title=site_title)


@app.route("/process_html", methods=["POST"])
def process_html():
    fname = request.form["fname"]
    site_title = fname.split("/")[-1][:-4]
    
    headers = {'Authorization': f'token {app.config["GITHUB_TOKEN"]}'}

    in_file = requests.get(fname.replace(".out", ".in"), headers=headers).text
    out_file = requests.get(fname, headers=headers)
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.out') as tmpfile:
        # Write the content to the temporary file
        tmpfile.write(out_file.text)
        tmpfile_path = tmpfile.name
    
    onc_parser = OncvParser(tmpfile_path).scan()
    
    onc_plotter = onc_parser.get_plotter()
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        ply_to_html_kwargs = {"full_html": False,
                              "include_plotlyjs": "cdn"}
        plots = {
            "radial_wfs": mpl_to_ply(onc_plotter.plot_radial_wfs(show=False)).to_html(**ply_to_html_kwargs),
            "atan_logder": mpl_to_ply(onc_plotter.plot_atan_logders(show=False)).to_html(**ply_to_html_kwargs),
            "ecut_convergence": mpl_to_ply(onc_plotter.plot_kene_vs_ecut(show=False)).to_html(**ply_to_html_kwargs),
            "projectors": mpl_to_ply(onc_plotter.plot_projectors(show=False)).to_html(**ply_to_html_kwargs),
            "ch_densities": mpl_to_ply(onc_plotter.plot_densities(show=False)).to_html(**ply_to_html_kwargs),
            "potentials": mpl_to_ply(onc_plotter.plot_potentials(show=False)).to_html(**ply_to_html_kwargs)
        }

    return render_template("visual_repr.html", 
                        site_title=site_title, 
                        infile=in_file,
                        plots=plots)


@app.route("/api/repo-data")
@cross_origin()
def repo_data():
    return jsonify(app.config['REPO_DATA'])