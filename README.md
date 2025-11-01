# chiz.work.gd-gateway 🚀

![Status](https://img.shields.io/badge/status-in%20development-yellow)

 ## ⚙️ Quick start 

### Install in dev with stack

for use with local installed [Docker-infra-stack](https://github.com/AndreyChiz/Docker-Infra-Stack.git)
 ```sh
git clone git@github.com:AndreyChiz/chiz.work.gd-gateway.git
./scripts/pipeline_run_dev.sh

```
### Install dev just own
```sh
docker compose -f compose.dev.yml up --buils -d
```

*in this case the database will be installed between service*

### Use in CICD

1. Change env.HOST="chiz.work.gd" in jenkinsfile to env.HOST="<YOUR_HOST_DNS>"
2. Create job in jenkins ui and set triggers like in standart flow