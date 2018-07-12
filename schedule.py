import yaml
import argparse
import os

def readConfig(cfg_file):
    with open(cfg_file, 'r') as stream:
        try:
            return (yaml.load(stream))
        except yaml.YAMLError as exc:
            logger.error('Failed to load yaml file:'+str(exc))
            raise exc

def getCourses(d):
	l=[]
	for i in d.keys():
		l.append({"subject":i,"courses":[ii["name"] for ii in d[i]]})
	return l

def findDep(d,subject,course,visited,final):
	#print(d)
	s=d[subject]
	node={}
	for i in s:
		if i["name"]==course:
			node=i
	if node=={}:
		raise Exception("Couldn't find course: "+course)

	
	if "depends" not in node.keys():
		final.append(course)
		return
	else:
		for i in node["depends"]:
			if i not in visited:
				findDep(d,subject,i,visited,final)
		visited.append(course)
	final.append(course)

def getGraph(d):
	f=[]
	v=[]
	for s in d.keys():
		for k in d[s]:
			if k["name"] not in v:
				v.append(k["name"])
				findDep(d,s,k["name"],v,f)
	return f

def getCourse(d,course,subject):
	s=d[subject]
	c={}
	for i in s:
		if i["name"]==course:
			c=i
	if c=={}:
		raise Exception("Couldn't find course: "+course)
	return c

def getDep(d,course,subject):
	f=[]
	findDep(d,subject,course,[],f)
	t={"courses":f,"target":course,"subject":subject}
	return t


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('func', type=str, help='function to run: courses, prereqs')
	parser.add_argument("--subject",dest="subject", help="subject of course",type=str,required=False,default="")
	parser.add_argument("--course",dest="course", help="course name",type=str,required=False,default="")
	args = parser.parse_args()
	cfg=readConfig("interlake.yml")

	if args.func=='courses':
		print(getCourses(cfg))
	elif args.func=='prereqs':
		if args.course=='':
			raise Exception("Course required")
		if args.subject=='':
			raise Exception("Subject required")
		print(getDep(cfg,args.course,args.subject	))
	else:
		raise Exception("Not a valid command")

if __name__ == '__main__':
    main()
