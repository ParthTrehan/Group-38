# Group-38

# COMP90024 Cluster & Cloud Computing Assignment 2

We have built a simple real-time cloud project which runs on [Nectar Cloud](https://nectar.org.au/). This project uses various frameworks and technologies including:

 1. **Ansible:** Used as a configration management tool to automate cloud.
 2. **Python:** Used for tweet harvesting and profanity analysis.
 3. **Nodejs and Expressjs:** Used for Web App. 
 4. **Couchdb:** Used as a database software for storing raw tweets and analyzed results.
 5. **AURIN:** AURIN datasets is used for result validations.


Deployment and User Guide
-
**Ansible and Setup**
Our application uses ansible to automatically create instances, mount volumes, install dependencies for various softwares, configure a cluster CouchDB on all nodes and start twitter harvesters and the web application. The following steps need to be executed to setup the application after ensuring that ansible is installed in the system.``
1. Download and save `openrc.sh` file inside the `/Ansible` folder.
2. Open file `/Ansible/host_vars/nectar.yaml` and change _*COUCHDB_PASSWORD*_ variable to your preferred database password.
3. Open terminal and run `./run-nectar.sh` from `/Ansible/` folder

**Accessing individual nodes**
The IPs of different nodes and their classifications (harvester, webserver) are stored inside _`hosts`_ file inside _`/Ansible/`_ folder. To access individual nodes, the user needs to acquire the ssh key (contact repository administrator) and store it in _`/Ansible/`_ folder. Next, the following commands need to be run to enter the individual node.
4. Open terminal and enter: 

`ssh -i<ssh-key><node-IP>`

**Checking status of Harvester**
To check the status of TwitterCrawler, the following command should be run on the terminal inside harvester node: 

`ps ax | grep TwitterCrawler.py`

The output file of the TwitterCrawler can be viewed by running _`cat output.log`_ (for debugging) in _`/home/ubuntu/deploy/Twitter_Crawler/`_ folder inside harvester node

**Checking status of Webserver**
The following command should be run on the terminal inside webserver node inside _`/home/ubuntu/deploy/webapp/`_ to check the status of webserver on NodeJs: 

`pm2 list`

The webserver node is also running a periodic function which updates the result of MapReduce on _tweets_ database every 60 seconds and pushes the updated result view to the _*analyze_results*_ database in the CouchDB cluster. This is used by the webserver to display visualizations.

To check the status of this function:

 _`ps ax | grep send_updated_result.sh`_

To check output log of this function, go to _`/home/ubuntu/deploy/Data/`_: 

_`cat output.log`_ (For debugging).


Links
-
Github repository:

https://github.com/parth97/Group-38

Deployment demo:

< link to deployment video >

Website demo:

< link to webapp video >


 Team Contributions
-

**Parth Trehan**[git link] :  Front-end development/Visualization, Ansible deployment

**Kumar Utkarsh**[git link]: Ansible deployment, Architecture, Debugging and Testing

**Kushagra**[git link]:  Ansible deployment, Architecture

**Smith John Colaco**[git link]:  Architecture, CouchDB

**Rohan Kirpekar**[git link]:  Tweet Harvesting, CouchDB, MapReduce
