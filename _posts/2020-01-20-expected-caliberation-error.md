---
Title: Expected Calibration Error
---

ECE quantifies how much you can trust the class confidences your model gives. It is the difference between the predicted confidence and reality. 
## How to compute the Caliberation Error?

Computing caliberation error is simple. First run your model over a set of samples and collect all the predictions. We need to compute two things. The accuracy of the predictions and the average confidence of all the predictions. 

The absolute difference between the two is caliberation error.

```python
def compute_accuracy(predictions, targets):
    assert predictions.shape==targets.shape
    return np.mean(predictions==targets)

def compute_caliberation_error(class_confidences, gt_idxs):
    predicted_class_idxs = np.argmax(class_confidences,axis=1)
    acc = compute_accuracy(predicted_class_idxs, gt_idxs)
    conf = np.max(class_confidences,axis=1).mean()
    return np.absolute(acc-conf),acc,conf
```

## Expected Caliberation Error 

A classifier is said to be well caliberated if it has a low ECE. I came across Expected Calibration Error from a recent, aptly titled paper “[*Your classifier is secretly an energy based model and you should treat it like one*](https://arxiv.org/abs/1912.03263)”. It defines ECE as

$$ECE = \sum _{m=1}^{M} \frac{|B_m|}{n} |acc(B_m) - conf(B_m)|$$

To compute ECE of a model, we simply bins the predictions first. Then, calculate average of all the caliberation errors. 

```python
def expected_caliberation_error(class_confidences,gt_idxs, num_bins=20):
    delta = 1.0/num_bins
    predicted_confidences = np.max(class_confidences,axis=1)
    data = []
    for l in np.arange(0.0,1.0,delta):
        h = l+delta
        # bin the predictions
        idxs = np.argwhere((predicted_confidences<=h) & (predicted_confidences>l)).flatten()
        if len(idxs)==0:continue
        
        # compute caliberation error
        ce,acc,conf = compute_caliberation_error(class_confidences[idxs,:], gt_idxs[idxs])
        data.append([l,h,ce,acc,conf])
    
    # average the computed caliberation errors
    ece = np.mean([ce for _,_,ce,_,_ in data])
    return ece, data
```

For testing, I finetuned a model with resnet18 stem and computed predictions over [ImageWoof](https://github.com/fastai/imagenette) dataset. 

Before training, the model has very high ECE

```python
learner.load('stage-0');
probs, targets = learner.get_preds()
class_confidences ,gt_idxs = probs.numpy(), targets.numpy()
ece, data = expected_caliberation_error(class_confidences,gt_idxs)
```





```python
plot_figure(x,y,delta)
```


![png](/images/2020-01-20-expected-caliberation-error_files/output_11_0.png)


After training, ECE has considerably reduced. 

```python
learner.load('stage-1');
probs, targets = learner.get_preds()
class_confidences, gt_idxs = probs.numpy(), targets.numpy()
ece, data = expected_caliberation_error(class_confidences,gt_idxs)
```





```python
plot_figure(x,y,delta)
```


![png](/images/2020-01-20-expected-caliberation-error_files/output_14_0.png)

