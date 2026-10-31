# Production Flask Guestbook Application

A production-ready Flask guestbook web application hosted on AWS EC2, backed by a managed AWS RDS PostgreSQL database, managed by Nginx and Gunicorn, and monitored with AWS CloudWatch alarms.


# Live Application
* **Live Web URL:** [http://77.113.211.17](http://77.113.211.17)

---

#Architecture Overview

```mermaid
graph LR
    User[User browser] -->|HTTP :80| IGW[Internet Gateway]
    IGW --> EC2[EC2 t3.micro<br>Amazon Linux 2023]
    subgraph EC2
        Nginx[nginx :80] --> Gunicorn[gunicorn + Flask :8000]
    end
    Gunicorn -->|PostgreSQL :5432| RDS[(RDS PostgreSQL, private)]
    CW[CloudWatch alarm] -.->|Monitors| EC2

🚀 How to Run Locally
Prerequisites
Python 3.9+

PostgreSQL (or SQLite for local testing)

Steps
Clone the repository:

Bash
git clone [https://github.com/](https://github.com/)<your-username>/guestbook-app.git
cd guestbook-app
Create and activate a virtual environment:

Bash
python3 -m venv venv
source venv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt
Set environment variables:

Bash
export DATABASE_URL="postgresql://<user>:<password>@localhost:5432/guestbook"
Run the Flask app:

Bash
python app.py
Access the app locally at http://127.0.0.1:5000.

☁️ Deployment Steps
Database Setup: Provisioned an AWS RDS PostgreSQL instance in a private security group and created the production guestbook database via psql.

Compute Instance: Launched an AWS EC2 t3.micro instance running Amazon Linux 2023.

Application Stack:

Deployed Flask application under /home/ec2-user/app/.

Managed background process execution using gunicorn bound to port 8000 via a systemd service (guestbook.service).

Configured Nginx as a reverse proxy listening on port 80 to route incoming traffic to Gunicorn.

🔔 Nice-to-Have Features & Monitoring
CloudWatch Alarm (StatusCheckFailed):

What: Configured an automated AWS CloudWatch alarm for EC2 system/instance status checks.

Why: Enables immediate SNS email notification if the EC2 host or OS instance encounters an outage, allowing rapid response before users report a system crash.

🔒 Security & Cost Optimization
Security:

Database access is isolated using AWS Security Groups—RDS accepts incoming PostgreSQL traffic (:5432) strictly from the EC2 instance web security group (web-sg).

Sensitive credentials and secrets are managed via environment variables and excluded from source control (.gitignore).

Cost:

Uses AWS Free Tier resources (t3.micro EC2 instance and Single-AZ db.t3.micro RDS instance) to minimize operational overhead while retaining high availability for personal projects.
