from draft_bot_app import app
from flask import Flask, redirect, render_template, url_for
import ast
import numpy as np

# from draft_bot_app.packages import cornersFromEasy, graphItMPL, graphItPlotly, imagePixels
# from draft_bot_app.packages.forms import RequestForm, RequestFormEasy, imageCompressForm

#########################################################################
########################### Demo Pages ##################################
#########################################################################

@app.route("/demo2D", methods = ('GET', 'POST'))
def demo2D():
    # Set these values all to None on the page refresh
    shape, visualize, cornerPoints, ipObject, solution, graphJSON = [None] * 6
    # Set decimals to zero for default integer-rounding
    decimals = 0
    # Set done = False if they haven't filled out form. Change if they submit form.
    done = False
    form = RequestForm()
    if form.validate_on_submit():
        # If they submitted, change done to True for rendering the page
        done = True
        decimals = form.decimals.data
        cornerPoints = ast.literal_eval(form.cornerPoints.data)
        shape = ast.literal_eval(form.shape.data)
        visualize = form.visualize.data
        ipObject = imagePixels.imagePixels(cornerPoints=cornerPoints,
            shape = shape)
        # Round array values using np.around() for text display
        # Convert back to a list to output the commas
        solution = np.around(ipObject.getGrid(), decimals = decimals).tolist()
        imagePixelsInfo = ({'cornerPoints': cornerPoints,
                              'shape': shape,
                              'visualize': visualize,
                              'solution':solution
                              })
        graphJSON = graphItPlotly.graphIt(imagePixelsInfo, dimension=2).ggjWrapper()
    return render_template('demo2D.html', form = form, graphJSON = graphJSON,
    solution = solution, visualize = visualize, done = done)