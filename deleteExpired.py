import time
import boto3
import datetime
import boto.ses
now = datetime.datetime.now()											#cant just typecast to str because remainder of hours/mins/secs
ec2client = boto3.client('ec2')
response = ec2client.describe_instances()
AWS_ACCESS_KEY = '' #insert aws access key/secret key of IAM user 
AWS_SECRET_KEY = '' #
#
#
#
#
class Email(object):  
    def __init__(self, to, subject):
        self.to = to
        self.subject = subject
        self._html = None
        self._text = None
        self._format = 'html'

    def html(self, html):
        self._html = html

    def text(self, text):
        self._text = text

    def send(self, from_addr=None):
        body = self._html

        if isinstance(self.to, basestring):
            self.to = [self.to]
        if not from_addr:
		#change to any email address verified through AWS SES
            from_addr = 'ctran1@u.brockport.edu'
        if not self._html and not self._text:
            raise Exception('You must provide a text or html body.')
        if not self._html:
            self._format = 'text'
            body = self._text

        connection = boto.ses.connect_to_region(
            'us-east-1',
            aws_access_key_id=AWS_ACCESS_KEY, 
            aws_secret_access_key=AWS_SECRET_KEY
        )

        return connection.send_email(
            from_addr,
            self.subject,
            None,
            self.to,
            format=self._format,
            text_body=self._text,
            html_body=self._html
        )
#
#
#
#takes in an instanceId(fid) and returns an instancename(instance exp date)
def get_instance_date(fid):
    # When given an instance ID as str e.g. 'i-1234567', return the instance 'Name' from the name tag.
    ec2 = boto3.resource('ec2')
    ec2instance = ec2.Instance(fid)
    inExp = ''
    for tags in ec2instance.tags:
        if tags["Key"] == 'projectEndDate':
            inExp = tags["Value"]
    return inExp
#
#
#
#
#nested for loop to iterate instances located in reservationsi
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
	#standardizes date layout using excel datetime format(float)
	inExpDate = time.mktime(time.strptime(inExpDate, "%Y-%m-%d"))
	#make global 'now' into an str to be used in next line
	now = now.strftime('%Y-%m-%d')
	#excel datetime format(float)
	now = time.mktime(time.strptime(now, "%Y-%m-%d"))
#
#	print(type(now))
#       print(type(inExpDate))
#       print(now)
#       print(inExpDate)
#       print(type(inID))
        #to debug, getting error that one is a float
	#
	print("\n")
	#
	if(inExpDate <= now):
		response = ec2client.terminate_instances(InstanceIds=[inID])
		print("\n")
		print("Instance scheduled for deletion")
		print("\n")
	#432000 is the datetime float format's equivalent of 5 days
	elif (inExpDate <= (now + 432000)) :
		print("\n")
		#change ctran1@u.brockport.edu to email of devops team/whom ever should be informed of a near expired instance
		email = Email(to='ctran1@u.brockport.edu', subject='instance {}'.format(inID))
		email.text('This is a warning for instance {}. project is due in 5 days or less'.format(inID))
		email.send()
		print("this needs an emailin'")
		print("\n")
	else :
		print("\n")
		print("project not due soon")
		print("\n")
