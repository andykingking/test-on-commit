import requests, json, pbs, re, time

def do_check():
	pbs.Command("hg")("id", "-i", "c:\\xampp\\htdocs\\web", _out="output.txt")
	text = open("output.txt", "r").read()
	regex_result = re.compile("(?P<node>\w+)\+*").search(text)
	local_revision = regex_result.groupdict()['node']
	r = requests.get('https://bitbucket.org/api/1.0/repositories/andrewking/web/changesets/?limit=1', auth=('myusername', 'mypassword'))
	if r.status_code == 200:
		result = r.json()
		if result['changesets'][0]['node'] != local_revision:
			print "Found new revision", result['changesets'][0]['node'], "- Doing test runs..."
			pbs.Command('powershell.exe')('c:\\xampp\\htdocs\\web\\testing\\run.ps1')
			print "Done tests"
			return True
	return False

def start():
	while(True):
		do_check()
		time.sleep(5)
	
if __name__ == "__main__":
	start()
