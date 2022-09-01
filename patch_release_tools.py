from gerrit import GerritClient
import urllib3
import subprocess
import json
import time
import sys
urllib3.disable_warnings()


argv1 = (sys.argv[1])
url_num = argv1[argv1.rfind("+"):][2:]

#parse json conifg
with open("config.json", encoding="utf-8") as f:
    data = json.loads(f.read())
    Username = data['username']
    Password = data['password']
    Project_id = data['project_id']
    Xml_path = data['xml_path']
    Gerrit_addr = data['gerrit_addr']

#Connect Gerrit Server
client = GerritClient(base_url="https://" + Gerrit_addr, username=Username, password=Password)

#Gerrit url convert to Change ID
change = client.changes.get(url_num)
change_str = str(change)[-42:-1]

cmd = "ssh -p 29418  " + Username + "@" + Gerrit_addr + " gerrit query --format JSON --current-patch-set " + change_str
output = subprocess.check_output([cmd], shell=True).decode('utf-8')
#output = output.replace("'", "\"")
commit_json = json.loads(output.split("\n")[0])

#print(commit_json)
commit_time = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(commit_json['createdOn'])) + " +0800"


commit_url = commit_json['url']
commit_revision_id = commit_json['currentPatchSet']['revision']
commit_info = commit_json['commitMessage']
commit_git_name = commit_url[commit_url.rfind(Project_id + "/"):][7:-7]
commit_git_xml =  subprocess.check_output("grep " + commit_git_name + " " + Xml_path +  " -nr" , shell=True).decode('utf-8')
commit_git_path_tmp = commit_git_xml[commit_git_xml.rfind("path"):][6:]
commit_git_path = commit_git_path_tmp[:commit_git_path_tmp.rfind("\" ")]
commit_author_name = commit_json['currentPatchSet']['author']['name']
commit_author_email_addr = commit_json['currentPatchSet']['author']['email']

print(commit_git_path)
print(commit_revision_id)
print("Author: " + commit_author_name + " <" + commit_author_email_addr + ">")
print("Data: " + commit_time)
print()
print(commit_info)

#print("-------------" + commit_revision_id + "----------------")
#print(commit_git_name)