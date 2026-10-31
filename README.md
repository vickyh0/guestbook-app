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
