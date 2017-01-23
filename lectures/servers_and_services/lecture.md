## Servers and services



## Objective
* Discuss the running droplets in Digital Ocean and the services that run on them.



## Summary
* Servers are hosted in Digital Ocean
  - most are in the NYC2 region, some in SGP1
* 21 servers in total
* Previously managed using Salt but now commands are ran manually



## ct1
* Gateway to other servers
  - SSH to `ct1` first before SSH to others
  - SSH port 58878
  - Only accepts SSH keys


## ct1
* Redirects requests to
  - naked `insynchq.com` domain
  - `jobs.insynchq.com`
  - `blog.insynchq.com`
  - `*.insync.io`


## ct1
* conf server
  - stores configuration that the `web` and `mailer` uses
* `source /insync/venv/conf_server_bin/activate`
  - use `conf_server`'s virtualenv
* `jt sconf load`
  - add or update conf values


## ct1
* Updates `apt` and `yum` repos
* `update_apt_repo <version number>`
  - update local copy of `apt` repo
* `update_yum_repo <version number>`
  - update local copy of `yum` repo
* `sync_repos.sh`
  - sync local `apt` and `yum` repos to S3


## ct1
* Updates and restarts web
* `update_in_web <packages ...>`
  - update listed packages for the web process
* `restart_web`
  - restart running web processes


## ct1
* Sets current Insync version for Mac and Windows



## beanstalkd
* beanstalkd
  - work queue
  - used to queue mails to be sent by the mailer and periodic mailer
* mailer
* periodic_mailer



## web servers
* web-lb02
  - web load balancer
  - web backend
* web02
  - web backend
* license01
  - /license backend
* license02
  - /license backend



## dbs
* db
  - Insync db
* db-slave02
  - Slave to the Insync db
  - Creates daily backups of the db and uploads it to the insync_db_backups S3 bucket through the `automysqlbackup` script



## redis
* Contains the redis servers



## dev
* Contains our private PyPI server
* Hosts hg.insynchq.com, our private Mercurial repo



## sentry
* Sentry server



## radar-2
* Radar server



## Drone servers
* drone
  - current Drone server
* drone-test
  - Drone server being tested for running integration tests



## mrkr-web-lb
Hosts `mrkr.io`.



## wiki
Hosts wiki.insynchq.com, the deprecated Insync wiki.



## insynchq-support
Hosts forums.insynchq.com.



## Staging servers
* staging
  - Hosts www.insynchq-test.com.
* insynchq-web-staging
  - Hosts beta.insynchq.com.



## dev02
* Hosts email.insynchq.com.
  - Not sure what this is.



## sendy
* Hosted sendy which was used by the mailer before.
* Not being used now (?)



# Possible candidates for removal/merging
* dev02
* Drone servers
  - after deployment of Travis
* wiki
* dev
* sendy
