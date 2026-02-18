\# Behavioral Malware Detection using Machine Learning



\## Overview

Traditional antivirus systems rely on signature matching, which fails to detect new or obfuscated malware.  

This project implements a \*\*behavior-based malware detection system\*\* that identifies malicious software based on runtime activity rather than file signatures.



The system observes program behavior in a controlled sandbox environment and uses Machine Learning models to classify whether the activity is \*\*malicious or benign\*\*.



---



\## Key Idea

Instead of scanning the file itself, we analyze \*\*what the program does\*\*:



Malware typically:

\- Creates suspicious processes

\- Modifies registry for persistence

\- Writes hidden files

\- Injects threads into other processes

\- Loads unusual DLLs

\- Communicates over suspicious network ports



These behaviors are converted into numerical features and used to train a classifier.



---



\## Dataset

The dataset represents behavioral logs collected from applications executed inside an isolated virtual environment.



Each record corresponds to a single execution and contains aggregated behavior counts such as:



| Feature | Description |

|------|------|

| file\_create | Number of files created |

| file\_read | File read operations |

| file\_write | File write operations |

| reg\_create | Registry key creation |

| reg\_set | Registry modification |

| process\_create | Number of processes spawned |

| thread\_create | Threads created / injection attempts |

| dll\_load | DLL loading activity |

| unique\_paths | Distinct filesystem paths accessed |

| label | benign / malware |



The raw logs are stored in `sandbox\_logs/` and transformed into structured data for training.



---



\## Feature Engineering

Raw counts are transformed into behavioral indicators:



\- File activity intensity

\- Registry persistence behavior

\- Process-thread injection ratio

\- DLL abuse indicator

\- Path traversal suspicion

\- Overall activity score



This improves separability between benign and malicious behavior.



---



\## Machine Learning Models

Two classifiers are trained and evaluated:



\- Random Forest Classifier

\- Gradient Boosting Classifier



The best performing model is automatically selected and saved.



---



\## Project Structure

behaviour analysis/

│

├── dataset/

│ └── behavioral\_dataset.csv

│

├── feature\_extraction/

│ └── extract\_features.py

│

├── model/

│ ├── train\_model.py

│ ├── random\_forest.pkl

│ └── scaler.pkl

│

├── sandbox\_logs/

│ ├── sample\_malware\_log.txt

│ └── sample\_benign\_log.txt

│

├── testing/

│ └── test\_model.py

│

├── main.py

├── requirements.txt

└── README.md







---



\## Workflow

1\. Execute application inside sandbox

2\. Collect behavioral logs

3\. Convert logs into numerical features

4\. Train machine learning classifier

5\. Save trained model

6\. Predict malware on new activity logs



---



\## Installation



\### 1.  Repository

https://github.com/Abhay-22042005/behaviour-analysis

cd malware-behavior-analysis





\### 2. Install Dependencies

pip install -r requirements.txt







---



\## Training the Model

python main.py





This will:

\- Load dataset

\- Extract behavioral features

\- Train ML models

\- Save trained classifier



Saved files:

model/random\_forest.pkl

model/scaler.pkl







---



\## Testing Malware Detection

Run prediction on behavior log:



python testing/test\_model.py







Output:

MALWARE DETECTED



or

BENIGN FILE





---



\## Applications

\- Endpoint security systems

\- Zero-day malware detection

\- Incident response automation

\- Behavioral intrusion detection



---



\## Limitations

\- Requires execution environment (sandbox)

\- Does not perform static binary analysis

\- Accuracy depends on behavioral diversity



---



\## Future Improvements

\- Deep learning sequence models (LSTM)

\- Real-time monitoring agent

\- Network traffic feature integration

\- Automatic feature extraction from Sysmon logs



---



\## Author

Cybersecurity Machine Learning Project  

Behavior-based Malware Detection System

