#!/bin/bash
set -e
set -x

export SSHKEYNAME=id_rsa

if true; then # [ -n $TRAVIS_EVENT_TYPE ] && [ $TRAVIS_EVENT_TYPE == "cron" ]; then
    # Start ays9 container
    sudo -HE bash -c "source /opt/code/github/jumpscale/bash/zlibs.sh; ZKeysLoad; ZDockerActive -b jumpscale/ays9 -i ays9"    
    # Install capnp tools if not exist
    if [ ! `which capnp` ]; then 
        sudo -HE bash -c "ssh -tA  root@localhost -p 2222 \"cd /tmp/;curl -O https://capnproto.org/capnproto-c++-0.6.1.tar.gz;tar zxf capnproto-c++-0.6.1.tar.gz;cd capnproto-c++-0.6.1;./configure;make install\""
    fi
    # Install RQ
    sudo -HE bash -c "ssh -tA root@localhost -p 2222 \"pip install rq\""
    # Dump the environment variables as json file in a the container cfg dir
    sudo -HE bash -c "python -c 'import json, os;print(json.dumps({\"BACKEND_ENV\": dict([(key, value) for key, value in os.environ.items() if key.startswith(\"BACKEND_\")])}))' > ~/js9host/cfg/ays_testrunner.json"

    # Add ays_templates
    sudo -HE bash -c "ssh -tA  root@localhost -p 2222 \"mkdir -p /opt/code/github/openvcloud; cd /opt/code/github/openvcloud; git clone https://github.com/openvcloud/ays_templates.git\""

    # Run tests
    sudo -HE bash -c "ssh -tA  root@localhost -p 2222 \"cd /opt/code/github/openvcloud/ays_templates; /bin/bash test.sh $TRAVIS_EVENT_TYPE\""
fi
