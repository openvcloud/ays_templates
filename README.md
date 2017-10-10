# ays_templates
AYS templates for OVC

To use the templates you need a docker containing a JumpScale installation that has AYS as part of the installation. Follow the docs at [bash](https://github.com/Jumpscale/bash/blob/master/README.md) repo to install bash utilities that are used for installing JumpScale.

To install AYS use the following command to prepare your keys:

`ZKeysLoad`

Then the following command to install a JumpScale installation containgi AYS:

`ZInstall_ays9`

You should have a new docker image `jumpscale/ays9` that contains the installation. To create the docker run:

`ZDockerActive -b jumpscale/ays9 -i <name of your docker>`

To use the templates in this repo, use the AYS end point `addTemplateRepo` to load the templates to be used by AYS.

This can be done by a simple API call or using AYS client. First open the js9 shell by typing `js9` in the AYS container. Then run the following:

```python
ayscl = j.clients.atyourservice.get()
ayscl.api.ays.addTemplateRepo(data={'url': '{repo_url}','branch': '{branch}'})

```
