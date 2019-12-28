# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 14:02:30 2018

@author: vic
"""

"""
compute the mean and stddev of 100 data sets and plot mean vs stddev.
When you click on one of the mu, sigma points, plot the raw data from
the dataset that generated the mean and stddev
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches

import md_common     as md_api
import time

class ClipInfo():
    def __init__(self, end_idx, num_bars):
        self.end_idx  = end_idx
        self.num_bars = num_bars
        self.repeats  = 0
        
class SubFigureMemo():
     def __init__(self, mem_fig, mem_collection, mem_snipinfo, mem_clips, mem_subtitle, mem_vct_ax):
         self.mem_fig      = mem_fig
         self.mem_collection = mem_collection
         self.mem_snipinfo   = mem_snipinfo
         self.mem_clips    = mem_clips
         self.mem_subtitle = mem_subtitle
         self.mem_vct_ax   = mem_vct_ax

figs_cache = {}  
       
chart_bar_num = 31
max_clips = 6
         
def build_clips(collection, assignments, dataidx):
    clips = []
    
    clip_info = ClipInfo(dataidx, chart_bar_num)
    clips.append(clip_info)
    assignment1 = assignments[dataidx]
    preclip_idx = 0
    if norepeat:
        preidx = dataidx
        for x in range(dataidx+1, len(assignments)):
            if(assignments[x] == assignment1):
                if preidx != x - 1:
                    if(len(clips) == max_clips): # need loop more
                        break
                    clip_info = ClipInfo(x, chart_bar_num)
                    clips.append(clip_info)
                    preclip_idx += 1
                else:
                    clips[preclip_idx].repeats += 1
                preidx = x
    else:
        for x in range(dataidx+1, len(assignments)):
            if(assignments[x] == assignment1):
                clip_info = ClipInfo(x, chart_bar_num)
                clips.append(clip_info)
                if(len(clips) == max_clips):
                    break
    cluster_id = assignment1
    cluster_id_cnt = 0
    for y in assignments:
        if y == cluster_id:
            cluster_id_cnt += 1
    subtitle = "Cluster(%d) Members(%d)"%(cluster_id, cluster_id_cnt)
    
    return clips, subtitle

def nxt_clips(collection, assignments, dataidx, assignment1):
    clips = []
    
    preclip_idx = -1
    if norepeat:
        preidx = dataidx
        for x in range(dataidx+1, len(assignments)):
            if(assignments[x] == assignment1):
                if(preclip_idx == -1):
                    clip_info = ClipInfo(x, chart_bar_num)
                    clips.append(clip_info)
                    preclip_idx = 0
                elif preidx != x - 1:
                    if(len(clips) == max_clips): # need loop more
                        break
                    clip_info = ClipInfo(x, chart_bar_num)
                    clips.append(clip_info)
                    preclip_idx += 1
                else:
                    clips[preclip_idx].repeats += 1
                preidx = x
    else:
        for x in range(dataidx+1, len(assignments)):
            if(assignments[x] == assignment1):
                clip_info = ClipInfo(x, chart_bar_num)
                clips.append(clip_info)
                if(len(clips) == max_clips):
                    break
    cluster_id = assignment1
    cluster_id_cnt = 0
    for y in assignments:
        if y == cluster_id:
            cluster_id_cnt += 1
    subtitle = "Cluster(%d) Members(%d)"%(cluster_id, cluster_id_cnt)
    
    return clips, subtitle

def pre_clips(collection, assignments, dataidx, assignment1):
    clips = []
    
    preclip_idx = -1
    if norepeat:
        preidx = dataidx
        for x in range(0, len(assignments)):
            if(x >= dataidx):
                break
            if(assignments[x] == assignment1):
                if(preclip_idx == -1):
                    clip_info = ClipInfo(x, chart_bar_num)
                    clips.append(clip_info)
                    preclip_idx = 0
                elif preidx != x - 1:
                    if(len(clips) == max_clips): # need loop more
                        break
                    clip_info = ClipInfo(x, chart_bar_num)
                    clips.append(clip_info)
                    preclip_idx += 1
                else:
                    clips[preclip_idx].repeats += 1
                preidx = x
    else:
        for x in range(0, len(assignments)):
            if(x >= dataidx):
                break
            if(assignments[x] == assignment1):
                clip_info = ClipInfo(x, chart_bar_num)
                clips.append(clip_info)
                if(len(clips) == max_clips):
                    break
            
    cluster_id = assignment1
    cluster_id_cnt = 0
    for y in assignments:
        if y == cluster_id:
            cluster_id_cnt += 1
    subtitle = "Cluster(%d) Members(%d)"%(cluster_id, cluster_id_cnt)
    if(len(clips) > max_clips):
        clips = clips[-max_clips-1:-1]
    return clips, subtitle
    
def sub_fig_on_key(event):
    fig_mem = figs_cache[event.canvas]
    #print('you pressed', event.key, event.xdata, event.ydata, " Convas", event.canvas, "Title =>", fig_mem.mem_subtitle)
    if(event.key == 'pageup' or event.key == 'pagedown'):
         pre_clip = fig_mem.mem_clips[len(fig_mem.mem_clips) - 1]
         if(event.key == 'pagedown'):
             clips, subtitle = nxt_clips(collection, assignments, pre_clip.end_idx + pre_clip.repeats , assignments[pre_clip.end_idx])
         else: 
             clips, subtitle = pre_clips(collection, assignments, pre_clip.end_idx + pre_clip.repeats , assignments[pre_clip.end_idx])
    
         if(len(clips) > 0):
             plot_k_chart(fig_mem.mem_fig, fig_mem.mem_collection,  fig_mem.mem_snipinfo, clips, subtitle)
             fig_mem.mem_fig.show()
    
         else:
             print("No clips")
    return True

def sub_fig_on_close(event):
    if(event.canvas in figs_cache):
        del figs_cache[event.canvas]
        print('Closed Sub Figure And Deleted It''s Cache')
    return True

def plot_k_chart(fig, collection, snipinfo, vct_clips, subtitle):#(ticker, beginDate, endDate=datetime.date.today()):
    global figs_cache
    num_clips = len(vct_clips)
    #quotes    = []

#    plt.cla()
#    plt.clf()
    
    #fig = plt.figure(figsize=(10,5))
    fig.set_tight_layout(False)
    
#    __color_balck__= '#000000'
#    __color_green__= '#00FFFF'
#    __color_purple__ = '#9900CC'
#    __color_golden__= '#FFD306'
    
    if(num_clips <=3 ):
        rows = num_clips
    else:
        rows = int(num_clips/2)
        if(num_clips % 2 == 1):
            rows += 1
    avg_height = 1 / rows
    gap_height = 0.1/rows
    act_height = 0.85/rows   
    
    if(fig.canvas in figs_cache):
        mem_vct_ax = figs_cache[fig.canvas].mem_vct_ax
        for ax in mem_vct_ax:
            fig.delaxes(ax)

    vct_ax = []
    for clip_idx in range(num_clips):
        clip_info =  vct_clips[clip_idx] 
        quotes_idx = []
        data_len = clip_info.num_bars
        real_idx_begin = snipinfo[1] + clip_info.end_idx + 1 - clip_info.num_bars
        real_idx_end   = snipinfo[1] + clip_info.end_idx + 1
        if(real_idx_begin < 0):
            raise ("Data Ivalid")
        title_tim = "%s"%(time.strftime("%Y-%m-%d %H:%M",time.localtime(collection.my_tim_array[real_idx_begin+clip_info.num_bars-1].Time / 1000)))
        for i in range(real_idx_begin, real_idx_end):
            quotes_idx.append("%s"%(time.strftime("%H:%M",time.localtime(collection.my_tim_array[i].Time / 1000))))


        if(rows == num_clips):
            ax1 = fig.add_axes([0.10, avg_height * (num_clips - 1 - clip_idx) + gap_height , 0.85, act_height])
        else:
            if(clip_idx < rows):
                ax1 = fig.add_axes([0.05, avg_height * (rows - 1 - clip_idx%rows) + gap_height , 0.44, act_height])
            else:
                ax1 = fig.add_axes([0.55, avg_height * (rows - 1 - clip_idx%rows) + gap_height , 0.44, act_height])
                
        #ax1.set_title("%s(%s)"%(param_date, param_interval))
        ax1.set_axisbelow(True)
        ax1.grid(True)
        ax1.set_xlim(-1, data_len+2)
        ax1.ticklabel_format(useOffset=False)
        
        #ax1.text(right, top,    title_tim, horizontalalignment='right',  verticalalignment='top', transform=ax1.transAxes)
        ax1.text(0,  0.95,      title_tim, horizontalalignment='left',   verticalalignment='top', transform=ax1.transAxes)
        if(clip_info.repeats > 0) :
            ax1.text(0.90, 0.95, "(%d)subs"%(clip_info.repeats), horizontalalignment='right',  verticalalignment='top', transform=ax1.transAxes)
   
        curve_x = []
        curve10_y = []
        curve60_y = []
        if(len(gui_line_fields) > 0):
            gui_line_vct_data = {}
            for x in gui_line_fields:
                gui_line_vct_data[x] = []
            
        for data_idx in range(real_idx_begin, real_idx_end):
            close_price = collection.my_array[data_idx].Last
            open_price =  collection.my_array[data_idx].Open
            high_price =  collection.my_array[data_idx].High
            low_price =   collection.my_array[data_idx].Low
            i = data_idx - real_idx_begin
            if close_price > open_price:
                ax1.add_patch(patches.Rectangle((i-0.2, open_price), 0.4, close_price-open_price, fill=False, color='r'))
                ax1.plot([i, i], [low_price, open_price], 'r')
                ax1.plot([i, i], [close_price, high_price], 'r')
            else:
                ax1.add_patch(patches.Rectangle((i-0.2, open_price), 0.4, close_price-open_price, color='g'))
                ax1.plot([i, i], [low_price, high_price], color='g')
                
            curve_x.append(i)
            curve10_y.append(collection.my_array[data_idx].MA10)
            curve60_y.append(collection.my_array[data_idx].MA20)
            if(len(gui_line_fields) > 0):
                for x in gui_line_fields:
                    gui_line_vct_data[x].append(eval("collection.my_array[data_idx].%s"%(x)))

        #ax1.set_title(instrument_id, fontproperties=font, fontsize=15, loc='left', color='r')
        #ax1.set_title(instrument_id, fontsize=15, loc='left', color='r')
        ax1.plot(curve_x, curve10_y, color='yellow')
        ax1.plot(curve_x, curve60_y, color='gray')
        if(len(gui_line_fields) > 0):
            for x in gui_line_fields:
                ax1.plot(curve_x, gui_line_vct_data[x])


        show_gap = 5
        xticks_cnt = int(data_len/show_gap)
        xticks_cnt += 1
        ax1.set_xticks(range(0, data_len, show_gap))
        s1 = ax1.set_xticklabels([quotes_idx[index] for index in ax1.get_xticks()])
        vct_ax.append(ax1)
        
    fig.canvas.set_window_title(subtitle)

    fig_mem = SubFigureMemo(fig, collection, snipinfo, vct_clips, subtitle, vct_ax)
    figs_cache[fig.canvas] = fig_mem
    
    fig.canvas.draw()
    

        
def onpick(event):
    if event.artist!=line: return True
    N = len(event.ind)
    if not N: return True


    figi = plt.figure()
    for subplotnum, dataidx in enumerate(event.ind):
        clips, subtitle = build_clips(collection, assignments, dataidx)
        plot_k_chart(figi, collection, snipinfo, clips, subtitle)
    figi.canvas.mpl_connect('key_release_event', sub_fig_on_key)
    figi.canvas.mpl_connect('close_event', sub_fig_on_close)
    figi.show()
    return True

def md_cluster_plot(param_collection, param_snipinfo, p_xs, p_ys, param_assignments, param_gui_line_fields, title = "Figure1"):
    global X
    global xs
    global ys
    global line
    global collection
    global assignments
    global snipinfo
    global norepeat
    global gui_line_fields
    norepeat = True
    
    
    dim = len(p_xs)
    X = np.random.rand(dim, 1000)

    xs = p_xs
    ys = p_ys
    
    collection      = param_collection
    snipinfo        = param_snipinfo
    assignments     = param_assignments
    gui_line_fields = param_gui_line_fields
    
    fig = plt.figure()
    fig.canvas.set_window_title(title)
    ax = fig.add_subplot(111)
    ax.set_title('click on point to plot time series')
    #line, = ax.plot(xs, ys, 'o', picker=5)  # 5 points tolerance
    line = ax.scatter(xs, ys, marker='o', s=30, c=assignments, picker=5)
#    print(xs)
#    print(ys)
#    print(line)
    fig.canvas.mpl_connect('pick_event', onpick)
    
    plt.show()

#test_xs = np.arange(1,11, 1)
#test_ys = np.arange(1,11, 1)
#test_xs = np.tile(test_xs, 10)
#test_ys = np.repeat(test_ys, 10) 
#assignments = np.random.randint(0,5, 100)   
#run(test_xs, test_ys, assignments)
