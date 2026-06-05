\# Employees Talent Analytics



!\[Project Status](https://img.shields.io/badge/status-active-success.svg)

!\[Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)

!\[License](https://img.shields.io/badge/license-MIT-green.svg)



\## 📊 Project Overview



A production-grade Python library for analyzing employee performance, succession 

planning, and talent development across an organization's regional offices (Dhahran, Jeddah, 

Riyadh). Designed to support data-driven HR decisions aligned with Vision 2030 

workforce development goals.



\## 🎯 Business Problem



HR leadership needs a systematic, data-driven approach to:

\- Identify high performers ready for promotion to Vision 2030 mega-project roles

\- Detect declining talent before flight risk becomes critical

\- Optimize training investment by measuring ROI per employee

\- Build a reliable succession pipeline for critical technical positions



Manual reviews across 3 offices create inconsistency and missed signals. 

This system standardizes performance evaluation at scale.



\## 🗂️ Dataset



| File | Records | Description |

|------|---------|-------------|

| `employees.csv` | 30 employees | Profile, office, department, seniority |

| `project\_assignments.csv` | 120 assignments | Project hours, completion rates per employee |

| `performance\_reviews.csv` | 90 reviews | Quarterly ratings across 3 periods |

| `training\_history.csv` | 80 records | Certifications and training completion |

| `salary\_history.csv` | 45 records | Compensation changes and promotion history |



\*\*Scope:\*\* 3 offices × 3 departments 



\## 🔧 Installation



```bash

\# Clone repository

git clone https://github.com/ShooqH/employees-talent-analytics.git

cd employees-talent-analytics



\# Create conda environment

conda create -n employees-analytics python=3.9

conda activate  Employees-talent-analytics



\# Install dependencies

pip install -r requirements.txt

```



\## 🗂️ Project Structure

employees-talent-analytics/

│

├── data/

│   ├── raw/                        # Original source files

│   └── processed/                  # Cleaned, analysis-ready data

│

├── src/

│   ├── init.py

│   ├── data\_loader.py              # ETL and data ingestion

│   ├── validators.py               # Data quality checks

│   ├── performance\_calculator.py   # Core performance metrics

│   ├── talent\_scorer.py            # Composite talent scoring

│   ├── succession\_analyzer.py      # Succession pipeline logic

│   ├── api\_client.py               # External API integration

│   ├── report\_generator.py         # Automated PDF reporting

│   └── utils.py                    # Shared utilities

│

├── tests/

│   ├── init.py

│   ├── test\_data\_loader.py

│   ├── test\_calculators.py

│   └── test\_api\_client.py

│

├── cli/

│   └── hr\_analytics.py         # Command-line interface

│

├── notebooks/

│   ├── 01\_exploratory\_analysis.ipynb

│   └── 02\_model\_validation.ipynb

│

├── .gitignore

├── config.yaml                     # Project configuration

├── requirements.txt

├── README.md

└── setup.py

\## 📈 Key Features



\- \*\*Performance Analytics\*\* — Identify top performers and declining talent using 

&#x20; quarterly review trends

\- \*\*Succession Planning\*\* — Map ready-now successors for critical roles across 

&#x20; all 3 offices

\- \*\*Training ROI\*\* — Measure return on certification and training investment 

&#x20; per employee

\- \*\*Flight Risk Detection\*\* — Flag retention risks before they escalate to 

&#x20; resignation



\## 🧪 Testing



```bash

pytest tests/ -v --cov=src

```



\## ⚙️ Configuration



All thresholds and business rules are managed in `config.yaml`.  

Key assumptions are marked explicitly — validate against HR policy before 

production deployment.



\## 🚀 Quick Start



\*(Will be completed in Day 13 — CLI tool)\*



\## 📄 License



MIT License



\## 👤 Author



Shooq Homoud

http://linkedin.com/in/shooq-alwuthaynani

Shooq.otibii@gmail.com





