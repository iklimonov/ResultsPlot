import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

class myLine():
    """description of class"""
    tData = []
    fData = []

    label = 'myLine'
    color = 'black'

    #linestyle = [ '-' | '--' | '-.' | ':' | 'steps']
    lineStyle = ''
    lineWidth = 1
    
    #'o', '.', ',', 'x', '+', 'v', '^', '<', '>', 's', 'd'
    marker = ''
    markerEdgeWidth = 1
    markerSize = 1
    
    markerFaceColor = 'black'
    markerEdgeColor = 'black'


    def __init__(self, tData,fData):
        self.tData = list(tData)
        self.fData = list(fData)
        if len(self.tData) != len(self.fData) :
            print("Lists have different size")

    def set_label(self, label):
        self.label = label

    def set_lineStyle(self, lineStyle):
        self.lineStyle = lineStyle
        
    def set_lineWidth(self, lineWidth):
        self.lineWidth = lineWidth

    def set_color(self, color):
        self.color = color
        
    def set_marker(self, marker):
        self.marker = marker

    def set_markerEdgeWidth(self, markerEdgeWidth):
        self.markerEdgeWidth = markerEdgeWidth

    def set_markerSize(self, markerSize):
        self.markerSize = markerSize

        
    def set_markerFaceColor(self, markerFaceColor):
        self.markerFaceColor = markerFaceColor

    def set_markerEdgeColor(self, markerEdgeColor):
        self.markerEdgeColor = markerEdgeColor    
