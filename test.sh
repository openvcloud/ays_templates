#!bin/bash
set -e

RUNTYPE=$1


echo "Starting AYS server"
js9 'j.atyourservice.server.start()'

# sleep for 30 seconds
sleep 30

# check if the server started
js9 'cli=j.clients.atyourservice.get();cli.api.ays.listRepositories()'

# validate all the schemas
echo "Validating Schemas"
for schema in $(find -name schema.capnp); do
  echo "Validating $schema"
  capnp compile -oc++ $schema
done

# running testsuite
echo "Running ays core tests"
js9"""
from ays_testrunner.template_testrunner import AYSTestRunnerFactory
backend_config = {'URL': 'se-gen-1.demo.greenitglobe.com',
                  'ACCOUNT': 'aystestrunner', 'LOCATION': '', 
                  'JWT': '***'}
runner = AYSTestRunnerFactory.get(name='non-core', test_type='non-core', config={'BACKEND_ENV': backend_config, 'BACKEND_ENV_CLEANUP': True})
runner.run()
"""