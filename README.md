# Visual CryptograPY AWS Infrastructure

Distributed visual cryptography application hosted on AWS. All the visual cryptography functionalities are implemented using Python; more information about the visual cryptography library can be found [here](https://github.com/JeeYou02/visual_cryptograPY).

The whole infrastructure is built with terraform and updated through a Github Action triggered at each repository push.

Follows a detailed diagram of the whole infrastructure:
```mermaid
---
config:
  layout: elk
---
flowchart TB
 subgraph CI_CD["DevOps & Deployment"]
    direction TB
        Terraform["Terraform CLI"]
        GitHub["GitHub Repo"]
        GHA["GitHub Actions Runner"]
        Dev["Developer Workstation"]
  end
 subgraph Frontend["Static Web Hosting"]
        S3["S3 Bucket"]
        S3Content["index.html <br> style.css <br> script.js <br> [API URL Injected]"]
  end
 subgraph Container["Docker Container"]
        PythonCode["lambda_function.py <br> Router Logic"]
        VisualCryptography["Python VC Logic"]
        Libs["OpenCV &amp; NumPy <br> Native Libs"]
  end
 subgraph Backend["Serverless Backend"]
        APIGW["API Gateway"]
        Lambda["AWS Lambda"]
        ECR["Amazon ECR"]
        Container
  end
 subgraph AWS_Cloud["AWS Cloud (us-east-1)"]
        Frontend
        Backend
  end
    Dev -- git push --> GitHub
    Dev -- terraform apply --> Terraform
    GitHub -- Triggers --> GHA
    S3 --> S3Content
    PythonCode --- VisualCryptography
    VisualCryptography --- Libs
    User(("User / Browser")) -- "1. HTTP GET (Load Site)" --> S3
    User -- "2. HTTP POST (Image Base64)" --> APIGW
    APIGW -- "3. Proxy Request (JSON Event)" --> Lambda
    Lambda -- "4. Runs Container" --> Container
    Terraform -. Provision Infrastructure .-> S3 & APIGW & Lambda & ECR
    GHA -. Sync Frontend Files .-> S3
    GHA -. Push Docker Image .-> ECR
    GHA -. Update Image Reference .-> Lambda
    Lambda -. Pulls Image .-> ECR

     Terraform:::devops
     GitHub:::devops
     GHA:::devops
     Dev:::devops
     S3:::aws
     S3Content:::comp
     PythonCode:::comp
     VisualCryptography:::comp
     Libs:::comp
     APIGW:::aws
     Lambda:::aws
     ECR:::aws
     User:::user
    classDef user fill:#f9f,stroke:#333,stroke-width:2px,color:black
    classDef aws fill:#FF9900,stroke:#232F3E,stroke-width:2px,color:white
    classDef comp fill:#ffffff,stroke:#232F3E,stroke-width:1px,color:#232F3E
    classDef devops fill:#2496ED,stroke:#333,stroke-width:2px,color:white
    classDef docker fill:#0db7ed,stroke:#333,stroke-width:2px,color:white
    style AWS_Cloud fill:#f2f2f2,stroke:#FF9900,stroke-width:2px
    linkStyle 0 stroke-width:3px,fill:none,stroke:green
    linkStyle 1 stroke-width:3px,fill:none,stroke:green
    linkStyle 2 stroke-width:3px,fill:none,stroke:green
    linkStyle 3 stroke-width:3px,fill:none,stroke:green
```
