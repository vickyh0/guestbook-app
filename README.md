```mermaid
graph LR
    User[User browser] -->|HTTP :80| IGW[Internet Gateway]
    IGW --> EC2[EC2 t3.micro<br>Amazon Linux 2023]
    subgraph EC2
        Nginx[nginx :80] --> Gunicorn[gunicorn + Flask :8000]
    end
    Gunicorn -->|PostgreSQL :5432| RDS[(RDS PostgreSQL, private)]
    CW[CloudWatch alarm] -.->|Monitors| EC2
