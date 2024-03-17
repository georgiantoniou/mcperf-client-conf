import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sys
import json
import numpy as np

def plot_stacked_bar(fig, ax, ax2, x, y, x2, y2, lab):

    # ax.bar(x[0], y[0], edgecolor='black', linewidth=1, label=lab.split(",")[0])
    prev=y[0]
    
    for i, el in enumerate(y):
        if i==0:
            ax.bar(x[i], y[i], edgecolor='black', linewidth=1, width=20000, label=lab.split(",")[i])
        else:
            ax.bar(x[i], y[i], edgecolor='black', bottom=prev, linewidth=1, width=20000, label=lab.split(",")[i])
            for j in range(len(prev)):
                prev[j] += y[i][j]

def plot_bar(fig, ax, ax2, x, y, x2, y2, lab, offset):
    
    if x and y and lab:
        for x_list in x:
            for y_list in y:
                ax.bar([ (float(i) + float(offset)) for i in x_list], y_list, edgecolor='black', width=10000, linewidth=1, label=lab)
    if x2 and y2 and lab:
        for x2_list in x2:
            for y2_list in y2:
                ax2.bar([ (float(i) + float(offset)) for i in x2_list], y2_list, edgecolor='black', width=10000, linewidth=1, label=lab)

    if x and y and not lab:
        for x_list in x:
            for y_list in y:
                ax.bar([ (float(i) + float(offset)) for i in x_list], y_list, edgecolor='black', width=10000, linewidth=1)
    if x2 and y2 and not lab:
        for x2_list in x2:
            for y2_list in y2:
                ax2.bar([ (float(i) + float(offset)) for i in x2_list], y2_list, edgecolor='black', width=10000, linewidth=1)

def plot_line(fig, ax, ax2, x, y, x2, y2, lab, colour):

    if x and y and lab:
        for x_list in x:
            for y_list in y:
                ax.plot(x_list, y_list, marker='o', label = lab, color=colour, linewidth=5)
                
    if x2 and y2 and lab:
        for x2_list in x2:
            for y2_list in y2:
                ax2.plot(x2_list, y2_list, marker='o', label = lab, color=colour, linewidth=5)
                
    if x and y and not lab:
        for x_list in x:
            for y_list in y:
                ax.plot(x_list, y_list, marker='o', color=colour, linewidth=5)
    if x2 and y2 and not lab:
        for x2_list in x2:
            for y2_list in y2:
                ax2.plot(x2_list, y2_list, marker='o', color=colour, linewidth=5)
   
def plot_data(fig, ax, ax2, x, y, x2, y2, subgraph):
    
    lab = subgraph['label']
    if subgraph['type'] == "line":
        colour = subgraph['colour']
        plot_line(fig, ax, ax2, x, y, x2, y2, lab, colour)
    elif subgraph['type'] == "bar":
        offset = subgraph['offset']
        plot_bar(fig, ax, ax2, x, y, x2, y2, lab, offset)
    elif subgraph['type'] == "stacked-bar":
        plot_stacked_bar(fig, ax, ax2, x, y, x2, y2, lab)
    

def get_data(parameters):

    data=pd.read_csv(parameters['data'])
    axis_list_data = []

    for i,metr in enumerate(parameters['metric'].split(",")):
        if metr == "qps":
            axis_list_data.append(data["qps"].unique().tolist())
        else:
            axis_list_data.append((data.loc[(data['metric'] == metr) & (data['configuration'] == parameters['conf-name']) & (data['exp_name'] == parameters['exp-name']), parameters['stats']]).values.tolist())
    
    return axis_list_data

def insert_data(subgraph, fig, ax, ax2):
    
    x = []
    y = []
    x2 = []
    y2 = []

    # get x-element data
    if subgraph['x-elements']['data'] != "":
        x = get_data(subgraph['x-elements'])
    # get y-element data
    if subgraph['y-elements']['data'] != "":
        y = get_data(subgraph['y-elements'])
    # get x2-elements data
    if subgraph['x2-elements']['data'] != "":
        x2 = get_data(subgraph['x2-elements'])
    # get y2-elements data
    if subgraph['y2-elements']['data'] != "":
        y2 = get_data(subgraph['y2-elements'])
    # plot data    
    plot_data(fig, ax, ax2, x, y, x2, y2, subgraph)

def create_graphs(input_parameters):
    for graph in input_parameters['graphs']:
        # initialize graph
        fig, ax = plt.subplots()
        ax2 = ax.twinx()
        for subgraph in graph['subgraphs']:
            insert_data(subgraph, fig, ax, ax2)

        # insert title
        if graph['title']:
            ax.set_title(graph['title'])

        # insert axis title
        if graph['y-axis-2nd-title']:
            ax2.set_ylabel(graph['y-axis-2nd-title'])
        else:
            ax2.set(yticklabels=[])
            ax2.tick_params(left=False)

        if graph['y-axis-title']:
            ax.set_ylabel(graph['y-axis-title'])

        if graph['x-axis-title']:    
            ax.set_xlabel(graph['x-axis-title'])

        # insert legend
        if "True" in graph['label']:
            h1, l1 = ax.get_legend_handles_labels()
            h2, l2 = ax2.get_legend_handles_labels()
            ax.legend(h1+h2, l1+l2, loc=2)


        # save output  
        plt.savefig(graph['output-filename'] + '.pdf', format="pdf", bbox_inches="tight", dpi=400)
        plt.savefig(graph['output-filename'] + '.png', format="png", bbox_inches="tight", dpi=400)
        plt.show()

#############################################
# Required arguments for the script to run
# 1: Configuration File
##############################################
def main(argv):

    conf_file = argv[1]
    with open(conf_file) as json_file:
        input_parameters = json.load(json_file)

    create_graphs(input_parameters)  
            
if __name__ == '__main__':
    main(sys.argv)