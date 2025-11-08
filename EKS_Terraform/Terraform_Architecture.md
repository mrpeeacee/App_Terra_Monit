root/ (root module)
│
├── main.tf          # Calls modules
├── variables.tf     # Defines project/region/etc.
├── outputs.tf       # Aggregates results
│
├── modules/
│   ├── vpc/         # 1st child module
│   │   ├── main.tf       # creates VPC/subnets/IGW
│   │   ├── variables.tf  # expects CIDR, etc.
│   │   └── outputs.tf    # exports vpc_id, subnet_ids
│   │
│   └── eks/         # 2nd child module
│       ├── main.tf       # creates EKS cluster/nodegroup
│       ├── variables.tf  # expects vpc_id, subnet_ids
│       └── outputs.tf    # exports cluster endpoint, etc.
│
└── backend/         # optional backend setup
    ├── main.tf
    ├── outputs.tf
    └── terraform.tfstate / lock files (state mgmt)
