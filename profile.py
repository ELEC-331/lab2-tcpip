"""This is a basic profile with two hosts connected by a router.
Instructions:
Wait for the profile instance to start, then log in to each node by clicking on it in the topology and choosing the `shell` menu item. 
"""


# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal object,
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Node juno
node_juno = request.XenVM('juno')
node_juno.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD'
node_juno.addService(pg.Execute('/bin/sh','wget -O - https://raw.githubusercontent.com/ELEC-331/tcp-ip-essentials/main/scripts/no-offload.sh | bash'))
iface0 = node_juno.addInterface('interface-1', pg.IPv4Address('10.0.1.100','255.255.255.0'))
node_juno.exclusive = False
node_juno.routable_control_ip = True # required for VNC
node_juno.startVNC()

# Node europa
node_europa = request.XenVM('europa')
node_europa.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD'
node_europa.addService(pg.Execute('/bin/sh','wget -O - https://raw.githubusercontent.com/ELEC-331/tcp-ip-essentials/main/scripts/no-offload.sh | bash'))
iface1 = node_europa.addInterface('interface-3', pg.IPv4Address('10.0.2.100','255.255.255.0'))
node_europa.exclusive = False
node_europa.routable_control_ip = True # required for VNC
node_europa.startVNC()

# Node router
node_router = request.XenVM('router')
node_router.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD'
node_router.addService(pg.Execute('/bin/sh','wget -O - https://raw.githubusercontent.com/ELEC-331/tcp-ip-essentials/main/scripts/no-offload.sh | bash'))
iface2 = node_router.addInterface('interface-0', pg.IPv4Address('10.0.1.10','255.255.255.0'))
iface3 = node_router.addInterface('interface-2', pg.IPv4Address('10.0.2.10','255.255.255.0'))
node_router.exclusive = False
node_router.routable_control_ip = True # required for VNC
node_router.startVNC()

# Link link-0
link_0 = request.Link('link-0')
link_0.addInterface(iface2)
link_0.addInterface(iface0)

# Link link-1
link_1 = request.Link('link-1')
link_1.addInterface(iface3)
link_1.addInterface(iface1)


# Print the generated rspec
pc.printRequestRSpec(request)

