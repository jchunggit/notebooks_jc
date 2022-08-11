def hex_to_rgb(hex_value):
    h = hex_value.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

cus_palette = list(map(hex_to_rgb, \
    ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33"]))

def plotscat(data, ncls,dataX):

    import seaborn as sns
    import matplotlib.pyplot as plt

    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(30,20))
    sns.scatterplot(x = data['IAT'], y= data['self'], hue=data['Labels'], style= data['edu'],
                    style_order = ['HighO', 'High', 'UnivO', 'Univ', 'GradO', 'Grad'],
                    markers = {'HighO': '.', 'High': 'o', 'UnivO': '^', 'Univ': 's',
                                'GradO': 'P', 'Grad': '*'},
                    palette=cus_palette[0:ncls], legend = False,
                    ax = ax1)
    sns.scatterplot(x = data['IAT'], y = data['HPC'], hue=data['Labels'], style= data['edu'],
                    style_order = ['HighO', 'High', 'UnivO', 'Univ', 'GradO', 'Grad'],
                    markers = {'HighO': '.', 'High': 'o', 'UnivO': '^', 'Univ': 's',
                                'GradO': 'P', 'Grad': '*'},
                    palette=cus_palette[0:ncls], legend = False,
                    ax = ax2)
    sns.scatterplot(x = data['IAT'], y = data['perf'], hue=data['Labels'], style= data['edu'],
                    style_order = ['HighO', 'High', 'UnivO', 'Univ', 'GradO', 'Grad'],
                    markers = {'HighO': '.', 'High': 'o', 'UnivO': '^', 'Univ': 's',
                                'GradO': 'P', 'Grad': '*'},
                    palette=cus_palette[0:ncls], legend = False,
                    ax = ax3)
    sns.scatterplot(x = data['self'], y = data['HPC'], hue=data['Labels'], style= data['edu'],
                    style_order = ['HighO', 'High', 'UnivO', 'Univ', 'GradO', 'Grad'],
                    markers = {'HighO': '.', 'High': 'o', 'UnivO': '^', 'Univ': 's',
                                'GradO': 'P', 'Grad': '*'},
                    palette=cus_palette[0:ncls], legend = False,
                    ax = ax4)
    sns.scatterplot(x = data['self'], y = data['HPC'], hue=data['Labels'], style= data['edu'],
                    style_order = ['HighO', 'High', 'UnivO', 'Univ', 'GradO', 'Grad'],
                    markers = {'HighO': '.', 'High': 'o', 'UnivO': '^', 'Univ': 's',
                                'GradO': 'P', 'Grad': '*'},
                    palette=cus_palette[0:ncls], legend = False,
                    ax = ax5)
    sns.scatterplot(x = data['HPC'], y = data['perf'], hue=data['Labels'], style= data['edu'],
                    style_order = ['HighO', 'High', 'UnivO', 'Univ', 'GradO', 'Grad'],
                    markers = {'HighO': '.', 'High': 'o', 'UnivO': '^', 'Univ': 's',
                                'GradO': 'P', 'Grad': '*'},
                    palette=cus_palette[0:ncls],
                    ax = ax6)

    handles, labels = ax6.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', fontsize = 'x-large',
                ncol = len(dataX.columns))
    ax6.get_legend().remove()
    
    ax1.xaxis.get_label().set_fontsize(20)
    ax2.xaxis.get_label().set_fontsize(20)
    ax3.xaxis.get_label().set_fontsize(20)
    ax4.xaxis.get_label().set_fontsize(20)
    ax5.xaxis.get_label().set_fontsize(20)
    ax6.xaxis.get_label().set_fontsize(20)
    ax1.yaxis.get_label().set_fontsize(20)
    ax2.yaxis.get_label().set_fontsize(20)
    ax3.yaxis.get_label().set_fontsize(20)
    ax4.yaxis.get_label().set_fontsize(20)
    ax5.yaxis.get_label().set_fontsize(20)
    ax6.yaxis.get_label().set_fontsize(20)
    ax1.tick_params(labelsize=15)
    ax2.tick_params(labelsize=15)
    ax3.tick_params(labelsize=15)
    ax4.tick_params(labelsize=15)
    ax5.tick_params(labelsize=15)
    ax6.tick_params(labelsize=15)
    plt.show()
