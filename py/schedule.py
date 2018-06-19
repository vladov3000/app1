import yaml

def readConfig(cfg_file):
    with open(cfg_file, 'r') as stream:
        try:
            return (yaml.load(stream))
        except yaml.YAMLError as exc:
            logger.error('Failed to load yaml file:'+str(exc))
            raise exc

def listCourses(d):
	for subject in d:
		for course in d[subject]:
			print (subject,'-',course["name"])

def findDep(subject,course,visited,final):
	s=d[subject]
	node={}
	for i in s:
		if i["name"]==course:
			node=i
	if node=={}:
		raise Exception("Couldn't find course: "+course)

	final.append(course)
	if "depends" not in node.keys():
		return
	else:
		for i in node["depends"]:
			if i not in visited:
				findDep(subject,i,visited,final)
		visited.append(course)




d=readConfig("interlake.yml")
f=[]
v=[]
for k in d["math"]:
	if k["name"] not in v:
		v.append(k["name"])
		findDep("math",k["name"],v,f)
print(f)