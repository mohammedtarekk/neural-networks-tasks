import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import itertools
from sklearn.metrics import plot_confusion_matrix

def signum(W, X):
    v = np.dot(W, X)
    if v > 0:
        return 1
    elif v < 0:
        return -1

    return 0

def draw_classification_line(W, X, Y):

    b = W[0, 0]
    X1 = max(X)
    y1 = (- X1 * W[0, 1] - b) / W[0, 2]

    X2 = min(X)
    y2 = (- X2 * W[0, 1] - b) / W[0, 2]

    y_values = [y1, y2]
    x_values = [X1, X2]

    plt.figure("Data visualization")
    plt.scatter(X[0:30], Y[0:30])
    plt.scatter(X[30:], Y[30:])
    plt.plot(x_values, y_values)
    plt.show()


def MSE(y_pred,y_train):
    sum = 0
    for i in range(len(y_pred)):
        diff = y_train[i] - y_pred[i]
        sum += (diff*diff)
    return sum/y_pred.shape[0]



def train(x_train, y_train, isBiased, learning_rate, epochsNum, MSE_Threshold):

    # 1- add bias vector and create random weight vector w
    x_train = np.c_[np.ones((x_train.shape[0], 1)), x_train]
    y_train = np.expand_dims(y_train, axis=1)
    W = np.random.rand(1, x_train.shape[1])


    # 2- iterate on training data
    y_pred = np.empty(y_train.shape)

    # Iterate number of epochs
    for epoc in range(epochsNum):
        # for each sample calculate the signum
        # and update W if needed--
        for i in range(x_train.shape[0]):
            if not isBiased:
                W[:, 0] = 0
            X = x_train[i]   # X vector of each sample
            target = y_train[i]  # Y value for each sample

            y_pred[i] = np.dot(W, X)  # calculate y predict

            # calculate the loss and update W
            if target != y_pred[i]:
                loss = target - y_pred[i]
                W = W + learning_rate * loss * X
        if (MSE(y_pred,y_train)<MSE_Threshold):
            break


    accuracy = 0.0
    for y in range(len(y_pred)):
        X = x_train[y]
        y_pred[y] = signum(W, X)
        if(y_pred[y] == y_train[y]):
            accuracy+=1
    accuracy = accuracy/len(y_pred)
    print("======== Training Accuracy: ", end=' ')
    print("{:.0%}".format(accuracy))

    # # Drawing the classification line
    draw_classification_line(W, x_train[:, 1], x_train[:, 2])
    return W


def test(x_test, y_test, W,labels):
    x_test = np.c_[np.ones((x_test.shape[0], 1)), x_test]
    y_test = np.expand_dims(y_test, axis=1)
    NumOfMiss = 0
    predicted = np.empty(y_test.shape)
    for i in range(len(x_test)):
        X = x_test[i]
        predicted[i] = signum(W, X)
        if predicted[i] != y_test[i]:
            NumOfMiss += 1
    Accuracy = 100 - ((NumOfMiss / len(x_test)) * 100)
    print("======== Testing Accuracy is : ", Accuracy, "%")
    #draw_classification_line(W, x_test[:, 1], x_test[:, 2])
    evaluate(y_test, predicted,labels)


def evaluate(y_test, y_pred,labels):
    # It should return the accuracy and show the confusion matrix
    #labels = ['class 1', 'class 2']
    #labels=[firstClassCB.get(),secondClassCB.get()]
    confusion_mat = confusion_matrix(y_test, y_pred)
    plot_confusion_matrix(confusion_mat, classes=labels)


def plot_confusion_matrix(cm, classes):
    plt.figure(figsize = (7,7))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=90)
    plt.yticks(tick_marks, classes)
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    print(cm)
    plt.show()
    ConAccuracy = ((cm[0][0]+cm[1][1])/(cm[0][0]+cm[0][1]+cm[1][0]+cm[1][1]))*100
    print("The Accuracy from Confusion Matrix is : ",ConAccuracy , "%" )



