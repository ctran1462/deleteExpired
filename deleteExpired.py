import time
import boto3
import datetime
now = datetime.datetime.now()
#cant just typecast to str because remainder of hours/mins/secs    
ec2client = boto3.client('ec2')
response = ec2client.describe_instances()
#
def get_instance_date(fid):
    # When given an instance ID as str e.g. 'i-1234567', return the instance 'Name' from the name tag.
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(fid)
    instancename = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'projectEndDate':
            instancename = tags["Value"]
    return instancename
def delete_server(instanceId):
                        conn.terminate_instances(instance_ids=[instanceId])
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        now = datetime.datetime.now()
	# This sample print will output entire Dictionary object
        print(str(instance))
        # This will print will output the value of the Dictionary key 'InstanceId'
	print("\n")
        ForKeyName = instance.keys()
	print("\n")
	print(ForKeyName)
	#Just gives you the keys for the one instance atm, key being what is inside of the instance and value being the value of what was inside of the instance (2/20)
	#                                                                      (what the instance consists of)
	#we want the key "Tag"'s key and value
	#we will need instance id to identify the instance to the machine
	print("\n")
	inID = instance["InstanceId"]
	inExpDate = get_instance_date(inID)
	delete = ""
	inExpDate = time.mktime(time.strptime(inExpDate, "%Y-%m-%d"))
	now = now.strftime('%Y-%m-%d')
	now = time.mktime(time.strptime(now, "%Y-%m-%d"))
	print(type(now))
	print(type(inExpDate))
	print(now)
	print(inExpDate)
	print(type(inID))
	#to debug, getting error that one is a float
	if(inExpDate <= now):
		response = ec2client.terminate_instances(InstanceIds=[inID,],)
		print("it is now, instance scheduled for deletion")
	#else if (inExpDate == now + 5 days || inExpDate == now + 4 days || inExpDate == now + 3 days || inExpDate == now + 2 days || inExpDate == now + 1)
	#432000 is the datetime float format's equivalent of 5 days
	if (inExpDate <= (now + 432000)) :
		print("this needs an emailin'")
	else :
		print("Not now")
	print (now + 345600)
