import sys
import ns.applications
import ns.core
import ns.internet
import ns.network
import ns.point_to_point
import ns.flow_monitor

# Enable this line to have random number being generated between runs.

#ns.core.RngSeedManager.SetSeed(int(time.time() * 1000 % (2**31-1)))

cmd = ns.core.CommandLine()

# Default values
cmd.latency = 1
cmd.rate = 500000
cmd.on_off_rate = 300000
cmd.AddValue ("rate", "P2P data rate in bps")
cmd.AddValue ("latency", "P2P link Latency in miliseconds")
cmd.AddValue ("on_off_rate", "OnOffApplication data sending rate")
cmd.Parse(sys.argv)


#######################################################################################
# CREATE NODES

nodes = ns.network.NodeContainer()
nodes.Create(6)


#######################################################################################
# CONNECT NODES WITH POINT-TO-POINT CHANNEL
#
# We use a helper class to create the point-to-point channels. It helps us with creating
# the necessary objects on the two connected nodes as well, including creating the
# NetDevices (of type PointToPointNetDevice), etc.

# Set the default queue length to 5 packets (used by NetDevices)
ns.core.Config.SetDefault("ns3::DropTailQueue::MaxPackets", ns.core.UintegerValue(5))


# To connect the point-to-point channels, we need to define NodeContainers for all the
# point-to-point channels.
n0n4 = ns.network.NodeContainer()
n0n4.Add(nodes.Get(0))
n0n4.Add(nodes.Get(4))

n1n4 = ns.network.NodeContainer()
n1n4.Add(nodes.Get(1))
n1n4.Add(nodes.Get(4))

n2n5 = ns.network.NodeContainer()
n2n5.Add(nodes.Get(2))
n2n5.Add(nodes.Get(5))

n3n5 = ns.network.NodeContainer()
n3n5.Add(nodes.Get(3))
n3n5.Add(nodes.Get(5))

n4n5 = ns.network.NodeContainer()
n4n5.Add(nodes.Get(4))
n4n5.Add(nodes.Get(5))

# create point-to-point helper with common attributes
pointToPoint = ns.point_to_point.PointToPointHelper()
pointToPoint.SetDeviceAttribute("Mtu", ns.core.UintegerValue(1500))
pointToPoint.SetDeviceAttribute("DataRate",
                            ns.network.DataRateValue(ns.network.DataRate(int(cmd.rate))))
pointToPoint.SetChannelAttribute("Delay",
                            ns.core.TimeValue(ns.core.MilliSeconds(int(cmd.latency))))

# install network devices for all nodes based on point-to-point links
d0d4 = pointToPoint.Install(n0n4)
d1d4 = pointToPoint.Install(n1n4)
d2d5 = pointToPoint.Install(n2n5)
d3d5 = pointToPoint.Install(n3n5)
d4d5 = pointToPoint.Install(n4n5)