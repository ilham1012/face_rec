
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
    
def axes2fig(axes, figsize=(16,12)):
    fig = plt.figure(figsize=figsize)
    
    try:
        h, w = axes.shape
        for i in range(h):
            for j in range(w):
                fig._axstack.add(fig._make_key(axes[i, j]), axes[i, j])

    except AttributeError:
        fig._axstack.add(fig._make_key(axes), axes)

    return fig


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues,
                          plt=None):
    """
    This function prints and plots the confusion matrix.
    """     
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, ax = ax)
    # labels, title and ticks
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels') 
    ax.set_title(title)
    print(classes)
    ax.xaxis.set_ticklabels(classes)
    ax.yaxis.set_ticklabels(classes)
    fig.tight_layout()
    return ax