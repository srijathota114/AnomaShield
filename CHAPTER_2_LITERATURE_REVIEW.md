# Chapter 2  
# LITERATURE REVIEW

This chapter reviews existing work related to data poisoning, anomaly detection, and the role of data cleaning in machine learning. The review is organised into four parts: data poisoning in machine learning, anomaly detection techniques in general, the specific algorithms used in the project (Isolation Forest and One-Class SVM), and the need for data cleaning before building ML models.

---

## 2.1 Data Poisoning in Machine Learning

Machine learning models learn patterns from the data they are trained on. If that data is altered or corrupted, the model can learn wrong patterns or behave in unexpected ways. Data poisoning refers to situations where an attacker or a faulty process injects bad or malicious samples into the training data so that the model’s behaviour is harmed.

Researchers have shown that even a small fraction of poisoned data can cause significant damage. For example, in classification tasks, adding a few per cent of carefully crafted poisoned samples can increase the test error rate noticeably. The attack can be targeted (e.g. causing the model to misclassify a specific input) or untargeted (e.g. generally reducing accuracy). Biggio and Roli (2018) present a broad survey of adversarial machine learning and explain how both training-time attacks (poisoning) and test-time attacks (evasion) threaten real systems. They argue that the assumption of “clean” training data often does not hold in practice, and that defences must be designed with this in mind.

In many real-world settings, poisoning may not be intentional. Data can be corrupted by sensor errors, manual entry mistakes, or bugs in data pipelines. The effect is similar: the model is trained on data that does not represent the true distribution. So whether the bad data is injected by an adversary or appears by accident, detecting and removing it before training is important. This motivates tools that can flag suspicious rows in a dataset so that users can review or drop them.

---

## 2.2 Anomaly Detection Techniques

Anomaly detection is the task of identifying data points that do not fit the “normal” pattern. Such points are often called outliers or anomalies. They may be errors, rare events, or, in the context of security, malicious samples.

Traditional methods include statistical approaches. The Z-Score method assumes that normal data is roughly normally distributed and flags points that are too many standard deviations away from the mean. It is simple and interpretable but sensitive to the normality assumption. The Interquartile Range (IQR) method uses quartiles instead of the mean and standard deviation. It defines a “normal” range using Q1, Q3, and the IQR, and flags points outside that range. IQR is more robust to skewed distributions and to the presence of some outliers in the data itself.

More advanced methods use machine learning. Distance-based methods (e.g. k-nearest neighbours) treat points that are far from their neighbours as anomalies. Density-based methods (e.g. LOF – Local Outlier Factor) compare the local density of a point with the density of its neighbours; points in sparse regions are considered anomalous. Model-based methods learn a model of “normal” data and flag points that do not fit well. Isolation Forest and One-Class SVM fall into this category and are widely used because they can handle complex, high-dimensional data without assuming a simple distribution.

Surveys such as Chandola et al. (2009) and Hodge and Austin (2004) classify anomaly detection methods and discuss their strengths and limitations. A common finding is that no single method works best for all types of data; combining several methods or using ensemble approaches often improves reliability. This idea is used in AnomaShield, where multiple detectors are run and a consensus rule is applied.

---

## 2.3 Isolation Forest and One-Class SVM

**Isolation Forest:** Liu, Ting, and Zhou (2008) introduced the Isolation Forest algorithm. Unlike many methods that try to model “normal” data, Isolation Forest focuses on isolating anomalies. The idea is that anomalous points are few and different, so they can be isolated from the rest of the data with fewer splits in a random tree. The algorithm builds an ensemble of such trees; points that are isolated quickly (short path length) get a high anomaly score.

Isolation Forest has linear time complexity and works well on large datasets. It does not assume a particular distribution and can handle high-dimensional data. The main parameter is the “contamination” (expected fraction of anomalies), which can be set based on domain knowledge or tuned. In AnomaShield, this parameter is set in an adaptive way depending on the size of the dataset (e.g. smaller contamination for smaller datasets) to avoid over-flagging.

**One-Class SVM:** Schölkopf et al. (2001) proposed the One-Class Support Vector Machine for estimating the support of a high-dimensional distribution. The algorithm learns a boundary around the “normal” data in a feature space (often using a kernel such as RBF). Points that fall outside this boundary are classified as anomalies. The parameter ν controls the fraction of training points that can lie outside the boundary (or on the wrong side of the decision surface), which is related to the expected fraction of outliers.

One-Class SVM is powerful for complex, non-linear boundaries but is more computationally expensive than tree-based methods. It is sensitive to the choice of kernel and parameters. In AnomaShield, the RBF kernel is used with gamma set to ‘scale’, and ν is chosen adaptively based on dataset size, similar to the contamination in Isolation Forest.

Both algorithms are well established and available in libraries such as scikit-learn, which makes them practical choices for a project that combines multiple detectors.

---

## 2.4 Need for Data Cleaning Before Machine Learning

The quality of training data directly affects the quality of the learned model. If the data contains errors, duplicates, or anomalous rows, the model may learn spurious patterns, overfit to noise, or perform poorly on new data. Textbooks and best practices in machine learning stress the importance of data preprocessing and cleaning before training.

Data cleaning can include handling missing values, removing duplicates, fixing inconsistent formats, and detecting or removing outliers. The last step is closely related to anomaly detection: rows that are far from the rest of the data may be mistakes or rare events that the user does not want to include in training. Removing or correcting such rows can make the dataset more representative and improve model reliability.

In practice, many teams still rely on ad hoc scripts or manual inspection. This does not scale to large datasets and may be inconsistent. Dedicated tools for data cleaning (e.g. OpenRefine) help with formatting and consistency but often do not include specialised anomaly or poison detection. Academic work on data poisoning has produced various detection and defence methods, but fewer efforts have packaged them into easy-to-use systems for practitioners. AnomaShield aims to fill this gap by providing a web-based tool that runs several detection methods and lets users download cleaned data, so that data cleaning and anomaly removal become a regular step in the ML workflow.

---

## References (Chapter 2)

1. B. Biggio and F. Roli, “Wild patterns: Ten years after the rise of adversarial machine learning,” *Pattern Recognition*, vol. 84, pp. 317–331, 2018.

2. V. Chandola, A. Banerjee, and V. Kumar, “Anomaly detection: A survey,” *ACM Computing Surveys*, vol. 41, no. 3, 2009.

3. V. Hodge and J. Austin, “A survey of outlier detection methodologies,” *Artificial Intelligence Review*, vol. 22, no. 2, pp. 85–126, 2004.

4. F. T. Liu, K. M. Ting, and Z.-H. Zhou, “Isolation Forest,” in *Proc. IEEE International Conference on Data Mining*, 2008, pp. 413–422.

5. B. Schölkopf, J. C. Platt, J. Shawe-Taylor, A. J. Smola, and R. C. Williamson, “Estimating the support of a high-dimensional distribution,” *Neural Computation*, vol. 13, no. 7, pp. 1443–1471, 2001.
