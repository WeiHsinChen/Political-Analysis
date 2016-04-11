from __future__ import print_function
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon

class Visualization:
  def __init__(self):
    self.density = None
    self.density_scale = None

  def init_hotmap(self):
    self.density = {
      'New Jersey':  0.0,
      'Rhode Island':   0.0,
      'Massachusetts':   0.0,
      'Connecticut':    0.0,
      'Maryland':   0.0,
      'New York':    0.0,
      'Delaware':    0.0,
      'Florida':     0.0,
      'Ohio':  0.0,
      'Pennsylvania':  0.0,
      'Illinois':    0.0,
      'California':  0.0,
      'Hawaii':  0.0,
      'Virginia':    0.0,
      'Michigan':    0.0,
      'Indiana':    0.0,
      'North Carolina':  0.0,
      'Georgia':     0.0,
      'Tennessee':   0.0,
      'New Hampshire':   0.0,
      'South Carolina':  0.0,
      'Louisiana':   0.0,
      'Kentucky':   0.0,
      'Wisconsin':  0.0,
      'Washington':  0.0,
      'Alabama':     0.0,
      'Missouri':    0.0,
      'Texas':   0.0,
      'West Virginia':   0.0,
      'Vermont':     0.0,
      'Minnesota':  0.0,
      'Mississippi':   0.0,
      'Iowa':  0.0,
      'Arkansas':    0.0,
      'Oklahoma':    0.0,
      'Arizona':     0.0,
      'Colorado':    0.0,
      'Maine':  0.0,
      'Oregon':  0.0,
      'Kansas':  0.0,
      'Utah':  0.0,
      'Nebraska':    0.0,
      'Nevada':  0.0,
      'Idaho':   0.0,
      'New Mexico':  0.0,
      'South Dakota':  0.0,
      'North Dakota':  0.0,
      'Montana':     0.0,
      'Wyoming':      0.0,
      'Alaska':     0.0
    }

  def set_hotmap(self, state, value):
    if state not in self.density:
      return 
    self.density[state] = float(value)

  def ini_scale_hotmap(self, density_scale):
    self.density_scale = density_scale

  def draw_hotmap(self, title, blue=True):
    plt.figure()
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
                projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    # draw state boundaries.
    # data from U.S Census Bureau
    # http://www.census.gov/geo/www/cob/st2000.html
    shp_info = m.readshapefile('datasets/st99_d00','states',drawbounds=True)
    # population density by state from
    # http://en.wikipedia.org/wiki/List_of_U.S._states_by_population_density

    # set the range to normalize
    vmax = -float("inf")  
    vmin = float("inf") 
    for k, v in self.density.items():
      if v > vmax:
        vmax = v
      elif v < vmin:
        vmin = v

    # normalize again if vmin < 0
    # if vmin < 0:
    #   for k, v in self.density.items():
    #     self.density[k] -= vmin
    #   vmax -= vmin
    #   vmin = 0

    # choose a color for each state based on population density.
    colors={}
    statenames=[]
    if blue:
      cmap = plt.cm.Blues_r
    else:
      cmap = plt.cm.hot 

    # print(m.states_info[0].keys())
    for shapedict in m.states_info:
      statename = shapedict['NAME']
      # skip DC and Puerto Rico.
      if statename not in ['District of Columbia','Puerto Rico']:
        den = self.density[statename]
        # calling colormap with value between 0 and 1 returns
        # rgba value.  Invert color range (hot colors are high
        # population), take sqrt root to spread out colors more.
        colors[statename] = list(cmap(1.-np.sqrt((den-vmin)/(vmax-vmin)))[:3])
      statenames.append(statename)
    # cycle through state names, color each one.
    ax = plt.gca() # get current axes instance
    for nshape,seg in enumerate(m.states):
      # skip DC and Puerto Rico.
      if statenames[nshape] not in ['District of Columbia','Puerto Rico']:
        color = rgb2hex(colors[statenames[nshape]]) 
        poly = Polygon(seg,facecolor=color,edgecolor=color)
        ax.add_patch(poly)
    # draw meridians and parallels.
    m.drawparallels(np.arange(25,65,20),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-120,-40,20),labels=[0,0,0,1])
    plt.title(title)
    plt.draw()

  def draw_candmap_scale(self, title):
    plt.figure()
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
                projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    # draw state boundaries.
    # data from U.S Census Bureau
    # http://www.census.gov/geo/www/cob/st2000.html
    shp_info = m.readshapefile('datasets/st99_d00','states',drawbounds=True)
    # choose a color for each state based on population density.
    colors={}
    statenames=[]
    cmap = plt.cm.seismic
    norm = mpl.colors.Normalize(vmin=0, vmax=1)
    msm = cm.ScalarMappable(norm=norm, cmap=cmap)
    candidate1 = None
    candidate2 = None
    # print(m.states_info[0].keys())
    for shapedict in m.states_info:
      statename = shapedict['NAME']
      statenames.append(statename)
      # skip DC and Puerto Rico.
      if statename not in ['District of Columbia','Puerto Rico']:
        if statename not in self.density_scale:
          colors[statename] = list(msm.to_rgba(0.5)[:3])
          continue
        den = self.density_scale[statename]

        cand1 = None
        cand2 = None
        score1 = None
        score2 = None
        for c, s in den.items():
          if cand1:
            cand2 = c
            score2 = s
          else:
            cand1 = c
            score1 = s   

        if not candidate1:
          candidate1 = cand1

        if not candidate2:
          candidate2 = cand2

        if not cand1:
          colors[statename] = list(msm.to_rgba(0)[:3])          
          continue
        elif not cand2:
          colors[statename] = list(msm.to_rgba(1)[:3])          
          continue

        delta = 0
        if (score1 < 0) and (score2 < 0):
            score1, score2 = score2, score1
            score1 = -score1
            score2 = -score2
        if (score1 < 0) or (score2 < 0):
            delta = -min(score1, score2)
            
        normalized_cand1 = float(score1 + delta)
        normalized_cand2 = float(score2 + delta)

        fraction_cand1 = normalized_cand1 / (normalized_cand1 + normalized_cand2)
        fraction_cand2 = 1 - fraction_cand1
        colors[statename] = list(msm.to_rgba(fraction_cand1)[:3])
    # cycle through state names, color each one.
    ax = plt.gca() # get current axes instance
    for nshape,seg in enumerate(m.states):
      # skip DC and Puerto Rico.
      if statenames[nshape] not in ['District of Columbia','Puerto Rico']:
        color = rgb2hex(colors[statenames[nshape]]) 
        poly = Polygon(seg,facecolor=color,edgecolor=color)
        ax.add_patch(poly)
    # draw meridians and parallels.
    m.drawparallels(np.arange(25,65,20),labels=[1,0,0,0])
    m.drawmeridians(np.arange(-120,-40,20),labels=[0,0,0,1])
    plt.title(title)
    if candidate1:
      red_patch = mpatches.Patch(color='r', label=candidate1)
    if candidate2:
      blue_patch = mpatches.Patch(color='b', label=candidate2)
    plt.legend(handles=[blue_patch, red_patch])
    plt.draw()

  def draw_domain_histogram(self, sum_domain):
    x_axis = ['Education', 'Law and political science', 'Social Topics', 'Philosophy', 'Science and technology', 'Medicine and health', 'Business and finance']
    abbre = ['Edu', 'Law', 'Soc', 'Rel', 'Sci', 'Med', 'Fin']
  
    for can, dic in sum_domain.items():
      tmp = []
      for d in abbre:
        if d in dic:
          tmp.append(dic[d])
        else:
          tmp.append(0)
      plt.figure()
      plt.bar(range(len(tmp)), tmp, align='center')
      plt.xticks(range(len(tmp)), x_axis, size='small')
      plt.title(can)
      plt.draw()


# Test
density = {
  'New Jersey':  438.00,
  'Rhode Island':   387.35,
  'Massachusetts':   312.68,
  'Connecticut':    271.40,
  'Maryland':   209.23,
  'New York':    155.18,
  'Delaware':    154.87,
  'Florida':     114.43,
  'Ohio':  107.05,
  'Pennsylvania':  105.80,
  'Illinois':    86.27,
  'California':  83.85,
  'Hawaii':  72.83,
  'Virginia':    69.03,
  'Michigan':    67.55,
  'Indiana':    65.46,
  'North Carolina':  63.80,
  'Georgia':     54.59,
  'Tennessee':   53.29,
  'New Hampshire':   53.20,
  'South Carolina':  51.45,
  'Louisiana':   39.61,
  'Kentucky':   39.28,
  'Wisconsin':  38.13,
  'Washington':  34.20,
  'Alabama':     33.84,
  'Missouri':    31.36,
  'Texas':   30.75,
  'West Virginia':   29.00,
  'Vermont':     25.41,
  'Minnesota':  23.86,
  'Mississippi':   23.42,
  'Iowa':  20.22,
  'Arkansas':    19.82,
  'Oklahoma':    19.40,
  'Arizona':     17.43,
  'Colorado':    16.01,
  'Maine':  15.95,
  'Oregon':  13.76,
  'Kansas':  12.69,
  'Utah':  10.50,
  'Nebraska':    8.60,
  'Nevada':  7.03,
  'Idaho':   6.04,
  'New Mexico':  5.79,
  'South Dakota':  3.84,
  'North Dakota':  3.59,
  'Montana':     2.39,
  'Wyoming':      1.96,
  'Alaska':     0.42
}

# tmp = Visualization()
# tmp.init_hotmap()
# for k, v in density.items():
#   tmp.set_hotmap(k, v)
# tmp.draw_hotmap('politics prediction')