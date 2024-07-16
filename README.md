# Encrypt RDS Instances

This script encrypts Amazon RDS instances that are not already encrypted. It performs the following steps for each specified RDS instance:
1. Creates a snapshot of the instance.
2. Copies the snapshot with encryption using a specified KMS key.
3. Restores the encrypted snapshot to a new RDS instance.
## Prerequisites
* AWS CLI configured with necessary permissions.
* Python 3 Installed
* boto3 library installed. You can install it using [pip](https://pip.pypa.io/en/stable/).

```bash
pip install boto3
```

## Usage
1. Clone the repository to your local machine
```bash
git clone <https://github.com/mriccobene-git/RDS-Encryption-Hardening.git>
cd <your-repository-directory>
```
2. Run the script using python
```bash
python3 rdsencrypt.py
```
You will be prompted to enter the following details:

* RDS instance IDs (comma-separated)
* AWS region
* KMS key ID
* DB subnet group name


# Script Explanation
The script contains the following key components
1. Importing required libraries
```python
import boto3
import time
```
2. Defining the encrypt_rds_instances Function

This function takes four parameters: instance_ids, region_name, kms_key_id, and db_subnet_group_name.

* Describes the DB instance to check if it is already encrypted.
* If not encrypted, creates a snapshot of the instance.
* Copies the snapshot with encryption.
* Restores the encrypted snapshot to a new instance.

3. Main Execution Block

This block prompts the user for input and calls the encrypt_rds_instances function with the provided inputs.
```python
if __name__ == "__main__":
    instance_ids = input("Enter the RDS instance IDs (comma-separated): ").split(',')
    region_name = input("Enter the AWS region: ")
    kms_key_id = input("Enter the KMS key ID: ")
    db_subnet_group_name = input("Enter the DB subnet group name: ")

    instance_ids = [id.strip() for id in instance_ids]
    encrypt_rds_instances(instance_ids, region_name, kms_key_id, db_subnet_group_name)
```


# Notes
* Ensure that the provided RDS instance IDs, AWS region, KMS key ID, and DB subnet group name are correct.
* The script uses AWS waiters to wait for the completion of snapshot creation, snapshot copy, and instance restoration processes.
* Any errors during the encryption process will be caught and printed to the console.


## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


