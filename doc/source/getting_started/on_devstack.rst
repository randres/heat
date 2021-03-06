..
      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

Heat and Devstack
=================
Heat is fully integrated into DevStack. This is a convenient way to try out or develop heat alongside the current development state of all the other OpenStack projects. Heat on DevStack works on both Ubuntu and Fedora.

These instructions assume you already have a working DevStack installation which can launch basic instances.

Configure DevStack to enable Heat
---------------------------------
Adding the following line to your `localrc` file will enable the heat services
::
    ENABLED_SERVICES+=,heat,h-api,h-api-cfn,h-api-cw,h-eng

It would also be useful to automatically download and register a VM image that Heat can launch.
::
    IMAGE_URLS+=",http://fedorapeople.org/groups/heat/prebuilt-jeos-images/F16-x86_64-cfntools.qcow2,http://fedorapeople.org/groups/heat/prebuilt-jeos-images/F16-i386-cfntools.qcow2"

URLs for any of [http://fedorapeople.org/groups/heat/prebuilt-jeos-images/ these prebuilt JEOS images] can be specified.

That is all the configuration that is required. When you run `./stack.sh` the Heat processes will be launched in `screen` with the labels prefixed with `h-`.

Confirming heat is responding
-----------------------------
Before any heat commands can be run, the authentication environment needs to be loaded
::
    source openrc

You can confirm that Heat is running and responding with this command
::
    heat stack-list

This should return an empty line

Preparing Nova for running stacks
---------------------------------
Enabling Heat in devstack will replace the default Nova flavors with flavours that the Heat example templates expect. You can see what those flavors are by running
::

    nova flavor-list

Heat needs to launch instances with a keypair, so we need to generate one
::

    nova keypair-add heat_key > heat_key.priv
    chmod 600 heat_key.priv

Launching a stack
-----------------
Now lets launch a stack, using an example template from the heat-templates repository::

    heat stack-create teststack -u
    https://raw.github.com/openstack/heat-templates/master/cfn/WordPress_Single_Instance.template -P "InstanceType=m1.large;DBUsername=wp;DBPassword=verybadpassword;KeyName=heat_key;LinuxDistribution=F16"

Which will respond::

    +--------------------------------------+-----------+--------------------+----------------------+
    | ID                                   | Name      | Status             | Created              |
    +--------------------------------------+-----------+--------------------+----------------------+
    | (uuid)                               | teststack | CREATE_IN_PROGRESS | (timestamp)          |
    +--------------------------------------+-----------+--------------------+----------------------+


List stacks
~~~~~~~~~~~
List the stacks in your tenant::

    heat stack-list

List stack events
~~~~~~~~~~~~~~~~~

List the events related to a particular stack::

   heat event-list teststack

Describe the wordpress stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Show detailed state of a stack::

   heat stack-show teststack

Note: After a few seconds, the stack_status should change from IN_PROGRESS to CREATE_COMPLETE.

Verify instance creation
~~~~~~~~~~~~~~~~~~~~~~~~
Because the software takes some time to install from the repository, it may be a few minutes before the Wordpress instance is in a running state.

Point a web browser at the location given by the WebsiteURL Output as shown by heat stack-show teststack::

    wget ${WebsiteURL}

Delete the instance when done
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Note: The list operation will show no running stack.::

    heat stack-delete teststack
    heat stack-list
