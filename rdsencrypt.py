import boto3
import time

def encrypt_rds_instances(instance_ids, region_name, kms_key_id, db_subnet_group_name):
    rds_client = boto3.client('rds', region_name=region_name)

    for instance_id in instance_ids:
        try:
            # Describe the DB instance
            instance = rds_client.describe_db_instances(DBInstanceIdentifier=instance_id)
            storage_encrypted = instance['DBInstances'][0]['StorageEncrypted']

            if not storage_encrypted:
                # Create a snapshot of the instance
                snapshot_id = f'{instance_id}-snapshot-{int(time.time())}'
                print(f"Creating snapshot for instance {instance_id}...")
                rds_client.create_db_snapshot(
                    DBSnapshotIdentifier=snapshot_id,
                    DBInstanceIdentifier=instance_id
                )

                # Wait for the snapshot to be completed
                waiter = rds_client.get_waiter('db_snapshot_available')
                waiter.wait(DBSnapshotIdentifier=snapshot_id)
                print(f"Snapshot {snapshot_id} created successfully for instance {instance_id}")

                # Copy the snapshot with encryption
                encrypted_snapshot_id = f'{snapshot_id}-encrypted'
                print(f"Copying snapshot {snapshot_id} with encryption...")
                rds_client.copy_db_snapshot(
                    SourceDBSnapshotIdentifier=snapshot_id,
                    TargetDBSnapshotIdentifier=encrypted_snapshot_id,
                    KmsKeyId=kms_key_id,
                    CopyTags=True
                )

                # Wait for the encrypted snapshot to be completed
                waiter = rds_client.get_waiter('db_snapshot_completed')
                waiter.wait(DBSnapshotIdentifier=encrypted_snapshot_id)
                print(f"Encrypted snapshot {encrypted_snapshot_id} created successfully")

                # Restore the encrypted snapshot to a new instance
                new_instance_id = f'{instance_id}-encrypted'
                print(f"Restoring encrypted snapshot {encrypted_snapshot_id} to a new instance {new_instance_id}...")
                rds_client.restore_db_instance_from_db_snapshot(
                    DBInstanceIdentifier=new_instance_id,
                    DBSnapshotIdentifier=encrypted_snapshot_id,
                    DBSubnetGroupName=db_subnet_group_name,
                    CopyTagsToSnapshot=True
                )

                # Wait for the new instance to be available
                waiter = rds_client.get_waiter('db_instance_available')
                waiter.wait(DBInstanceIdentifier=new_instance_id)
                print(f"New encrypted instance {new_instance_id} created successfully")

            else:
                print(f"Instance {instance_id} is already encrypted.")

        except Exception as e:
            print(f"Error encrypting instance {instance_id}: {e}")

if __name__ == "__main__":
    # Prompt user for input
    parser = argparse.ArgumentParser(description="Encrypt RDS Instances")
    parser.add_argument('--instance-ids', help="Comma-separated list of RDS instance identifiers")
    parser.add_argument('--region', help="AWS region")
    parser.add_argument('--kms-key-id', help="KMS key ID")
    parser.add_argument('--db-subnet-group-name', help="DB subnet group name")
    
    args = parser.parse_args()
    
    if not args.instance_ids:
        instance_ids = input("Enter the RDS instance IDs (comma-separated): ").split(',')
    else:
        instance_ids = args.instance_ids.split(',')
    
    region_name = args.region or input("Enter the AWS region: ")
    kms_key_id = args.kms_key_id or input("Enter the KMS key ID: ")
    db_subnet_group_name = args.db_subnet_group_name or input("Enter the DB subnet group name: ")

    instance_ids = [id.strip() for id in instance_ids]

    encrypt_rds_instances(instance_ids, region_name, kms_key_id, db_subnet_group_name)
