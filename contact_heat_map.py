'''
Created May 1, 2021

@author nick pietras

program creating a contact map 
and contact heap map of given
sequences from files
'''

from bokeh.plotting import figure, output_file, show
from bokeh.models import LinearColorMapper
from bokeh.models import ColumnDataSource
from urllib.request import urlopen
from collections import defaultdict
import math

def contact_map(source, output = None, threshold = 8, model = 1, chain = 'A'):
    '''
    creates a binary contact map of a given model and chain of a pdb file of a sequence
    '''    
    def points_to_plot(pointsList):
        '''
        returns the list of points to plot for contact map
        '''
        points = []
        for i in range(len(pointsList)):
            for j in range(len(pointsList)):
                if distance(pointsList[i], pointsList[j]) < threshold:
                    points.append((i, j))
        return points
    
    d = dataParser(source, output)[0]
    try:
        pointsList = points_from_dict(d, model, chain)
    except:
        raise RuntimeError('Error: Invalid model or chain')
    output_file(dataParser(source, output)[1])
    plot = figure(width = 400, height = 400)
    pairs = points_to_plot(pointsList)
    x,y = zip(*pairs) #a bit of Python magic
    plot.x(x,y,size = 1, color = 'black',alpha = 0.5)
    plot.xgrid.visible = False
    plot.ygrid.visible = False
    show(plot)      



def contact_heat_map(source, output = None, model = 1, chain = 'A'):
    '''
    creates a contact heat map of a given model and chain of a pdb file of a sequence
    '''
    def toCDS(pointsList):
        '''
        returns column data source of all points and their respective z values for contact heat map
        '''
        sideLen = len(pointsList)
        df = {'x' : [i // sideLen for i in range(sideLen ** 2)],
              'y' : [j % sideLen for j in range(sideLen ** 2)]}
        df['z'] = []
        for x in range(len(pointsList)):
            for y in range(len(pointsList)):
                df['z'].append(distance(pointsList[x], pointsList[y]))        
        return ColumnDataSource(df)
        
    
    d = dataParser(source, output)[0]
    try:
        pointsList = points_from_dict(d, model, chain)
    except:
        raise RuntimeError('Error: Invalid model or chain')
    df = toCDS(pointsList)
    
    
    output_file(dataParser(source, output)[1])
    colors = 'Inferno256'
    mapper = LinearColorMapper(palette=colors,
                               low=min(df.data['z']),
                               high=max(df.data['z']))
    p = figure(height=400, width=400)
    p.rect(x = 'x', y = 'y', width = 1, height = 1,
           source = df,
           fill_color = {'field' : 'z', 'transform' : mapper},
           line_color = None)
    show(p)
    
    
    
    
    



def points_from_dict(d, model, chain):
    '''
    returns list of x-y-z values given the dictionary, model, and chain
    '''
    return [index for index in d[model][chain]]
    


def distance(point1, point2):
    '''
    returns distance between two points
    '''
    return math.sqrt(sum((p-q)**2 for p,q in zip(point1, point2)))

def dataParser(source, output):
    '''
    returns the created dictionary of x-y-z values from the pdb file,
    and also returns the name of the file to save as
    '''
    def get_centers(data):
        '''
        returns dictionary containing x-y-z values
        '''
        centers = defaultdict(lambda : defaultdict(list))
        model = 1
        for line in data:
            if line.startswith('ENDMDL'):
                model += 1
            if line.startswith('ATOM'):
                if line[12:16].strip() == 'CA':
                    chain = line[21]
                    index = int(line[22:26])
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    centers[model][chain].append((x, y, z))
        return centers
    
    try:
        if source.endswith('.pdb'):
            with open(source, 'r') as f:
                data = f.read()
        else:
            with urlopen('https://files.rcsb.org/view/' + source.upper() + '.pdb') as f:
                data = f.read().decode('utf-8')
        data = data.split('\n')
        d = get_centers(data)
        
    except:
        raise FileNotFoundError('Error: No such file ' + source)
    
    try:
        if output == None:
            output_file = source + '.html'
        else:
            output_file = source
    except:
        raise RuntimeError('Error: Invalid save-file name')
    return [d, output_file]

contact_map('2HUI')
contact_heat_map('2HUI')
