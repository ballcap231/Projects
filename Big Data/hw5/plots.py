import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
import numpy as np
# TODO: You can use other packages if you want, e.g., Numpy, Scikit-learn, etc.


def plot_learning_curves(train_losses, valid_losses, train_accuracies, valid_accuracies):
    # TODO: Make plots for loss curves and accuracy curves.
    # TODO: You do not have to return the plots.
    # TODO: You can save plots as files by codes here or an interactive way according to your preference.
    plt.figure(figsize=(15,8))
    plt.suptitle("Losses", fontsize=15, fontweight ='bold')
    plt.plot(train_losses, label = 'Training_Losses')
    plt.plot(valid_losses, label= 'Valid_Losses')
    plt.xlabel('Epoch', fontsize=25)
    plt.ylabel('Loss', fontsize= 25)
    plt.legend()
    plt.savefig("losses_CNN.png")
    plt.close()#closing image plotting inline
    
    plt.figure(figsize=(15,8))
    plt.suptitle("Accuracies", fontsize=15, fontweight ='bold')
    plt.plot(train_accuracies, label = 'Training_Accuracies')
    plt.plot(valid_accuracies, label= 'Valid_Accuracies')
    plt.xlabel('Epoch', fontsize=25)
    plt.ylabel('Accuracies', fontsize= 25)
    plt.legend()
    plt.savefig("accuracies_CNN.png")
    plt.close()#closing image plotting inline     


def plot_confusion_matrix(results, class_names):
    # TODO: Make a confusion matrix plot.
    # TODO: You do not have to return the plots.
    # TODO: You can save plots as files by codes here or an interactive way according to your preference.
    #code citation: https://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    y_true , y_pred = zip(*results)

    cm = confusion_matrix(y_true, y_pred)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)

    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=class_names, yticklabels=class_names,
           title='Normalized confusion matrix'	,
           ylabel='True label',
           xlabel='Predicted label')
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    fmt = '.2f' 
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    plt.savefig("confusion_CNN.png")
