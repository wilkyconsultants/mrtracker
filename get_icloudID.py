#!/usr/bin/python3
#
# simulate ksh command: defaults read MobileMeAccounts Accounts|grep AccountID|awk '{print $3}'|sed 's/"//g; s/;//g'
#
import subprocess
result = subprocess.run(["defaults", "read", "MobileMeAccounts", "Accounts"], capture_output=True, text=True)
output_lines = result.stdout.split('\n')
account_lines = [line for line in output_lines if "AccountID" in line]
account_ids = [line.split()[2] for line in account_lines]
cleaned_account_ids = [account_id.replace('"', '').replace(';', '') for account_id in account_ids]
for account_id in cleaned_account_ids:
    icloud_ID=account_id
    #print(account_id)
print("icloud ID: "+icloud_ID)
