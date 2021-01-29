
https://docs.cyclopsgroup.org/jmxterm
https://rmoff.net/2018/09/19/exploring-jmx-with-jmxterm/
```
# Launch:
wget https://github.com/jiaqi/jmxterm/releases/download/v1.0.1/jmxterm-1.0.1-uber.jar
java -jar jmxterm-1.0.1-uber.jar --url localhost:9999
Welcome to JMX terminal. Type "help" for available commands.

# list available domains
$>domains
#following domains are available
JMImplementation
com.sun.management
java.lang
java.nio
java.util.logging
kafka
kafka.cluster
kafka.controller
kafka.coordinator.group
kafka.coordinator.transaction
kafka.log
kafka.network
kafka.server
kafka.utils

# Switch to a particular domain:
$>domain kafka.network
#domain is set to kafka.network

# List the available MBeans in a the selected domain
$>beans
#domain = kafka.network:
kafka.network:error=NONE,name=ErrorsPerSec,request=LeaderAndIsr,type=RequestMetrics
kafka.network:error=NONE,name=ErrorsPerSec,request=UpdateMetadata,type=RequestMetrics
kafka.network:listener=PLAINTEXT,name=AcceptorBlockedPercent,type=Acceptor
kafka.network:name=ControlPlaneExpiredConnectionsKilledCount,type=SocketServer
kafka.network:name=TotalTimeMs,request=Produce,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=FetchFollower,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=FetchConsumer,type=RequestMetrics



bean kafka.network:name=TotalTimeMs,request=FetchFollower,type=RequestMetrics

# Switch to a particular bean of interest:
$>bean kafka.network:name=TotalTimeMs,request=Produce,type=RequestMetrics
#bean is set to kafka.network:name=TotalTimeMs,request=Produce,type=RequestMetrics



$>info
#mbean = kafka.network:name=TotalTimeMs,request=Produce,type=RequestMetrics
#class name = com.yammer.metrics.reporting.JmxReporter$Histogram
# attributes
  %0   - 50thPercentile (double, r)
  %1   - 75thPercentile (double, r)
  %2   - 95thPercentile (double, r)
  %3   - 98thPercentile (double, r)
  %4   - 999thPercentile (double, r)
  %5   - 99thPercentile (double, r)
  %6   - Count (long, r)
  %7   - Max (double, r)
  %8   - Mean (double, r)
  %9   - Min (double, r)
  %10  - StdDev (double, r)
# operations
  %0   - javax.management.ObjectName objectName()
  %1   - [D values()
#there's no notifications

# Get metric value
$>get Mean
#mbean = kafka.network:name=TotalTimeMs,request=FetchFollower,type=RequestMetrics:
Mean = 0.0
```



### Kafka network metrics
```
kafka.network:error=NONE,name=ErrorsPerSec,request=LeaderAndIsr,type=RequestMetrics
kafka.network:error=NONE,name=ErrorsPerSec,request=UpdateMetadata,type=RequestMetrics
kafka.network:listener=PLAINTEXT,name=AcceptorBlockedPercent,type=Acceptor
kafka.network:name=ControlPlaneExpiredConnectionsKilledCount,type=SocketServer
kafka.network:name=ControlPlaneNetworkProcessorAvgIdlePercent,type=SocketServer
kafka.network:name=ExpiredConnectionsKilledCount,type=SocketServer
kafka.network:name=IdlePercent,networkProcessor=0,type=Processor
kafka.network:name=IdlePercent,networkProcessor=1,type=Processor
kafka.network:name=IdlePercent,networkProcessor=2,type=Processor
kafka.network:name=LocalTimeMs,request=AddOffsetsToTxn,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=AddPartitionsToTxn,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=AlterConfigs,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=AlterPartitionReassignments,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=AlterReplicaLogDirs,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=ApiVersions,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=ControlledShutdown,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=CreateAcls,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=CreateDelegationToken,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=CreatePartitions,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=CreateTopics,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=DeleteAcls,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=DeleteGroups,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=DeleteRecords,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=DeleteTopics,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=DescribeAcls,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=DescribeConfigs,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=DescribeDelegationToken,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=DescribeGroups,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=DescribeLogDirs,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=ElectLeaders,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=EndTxn,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=ExpireDelegationToken,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=Fetch,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=FetchConsumer,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=FetchFollower,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=FindCoordinator,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=Heartbeat,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=IncrementalAlterConfigs,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=InitProducerId,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=JoinGroup,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=LeaderAndIsr,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=LeaveGroup,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=ListGroups,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=ListOffsets,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=ListPartitionReassignments,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=Metadata,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=OffsetCommit,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=OffsetDelete,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=OffsetFetch,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=OffsetForLeaderEpoch,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=Produce,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=RenewDelegationToken,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=SaslAuthenticate,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=SaslHandshake,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=StopReplica,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=SyncGroup,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=TxnOffsetCommit,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=UpdateMetadata,type=RequestMetrics
kafka.network:name=LocalTimeMs,request=WriteTxnMarkers,type=RequestMetrics
kafka.network:name=MemoryPoolAvailable,type=SocketServer
kafka.network:name=MemoryPoolUsed,type=SocketServer
kafka.network:name=MessageConversionsTimeMs,request=Fetch,type=RequestMetrics
kafka.network:name=MessageConversionsTimeMs,request=Produce,type=RequestMetrics
kafka.network:name=NetworkProcessorAvgIdlePercent,type=SocketServer
kafka.network:name=RemoteTimeMs,request=AddOffsetsToTxn,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=AddPartitionsToTxn,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=AlterConfigs,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=AlterPartitionReassignments,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=AlterReplicaLogDirs,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=ApiVersions,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=ControlledShutdown,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=CreateAcls,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=CreateDelegationToken,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=CreatePartitions,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=CreateTopics,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=DeleteAcls,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=DeleteGroups,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=DeleteRecords,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=DeleteTopics,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=DescribeAcls,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=DescribeConfigs,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=DescribeDelegationToken,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=DescribeGroups,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=DescribeLogDirs,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=ElectLeaders,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=EndTxn,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=ExpireDelegationToken,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=Fetch,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=FetchConsumer,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=FetchFollower,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=FindCoordinator,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=Heartbeat,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=IncrementalAlterConfigs,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=InitProducerId,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=JoinGroup,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=LeaderAndIsr,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=LeaveGroup,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=ListGroups,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=ListOffsets,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=ListPartitionReassignments,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=Metadata,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=OffsetCommit,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=OffsetDelete,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=OffsetFetch,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=OffsetForLeaderEpoch,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=Produce,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=RenewDelegationToken,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=SaslAuthenticate,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=SaslHandshake,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=StopReplica,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=SyncGroup,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=TxnOffsetCommit,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=UpdateMetadata,type=RequestMetrics
kafka.network:name=RemoteTimeMs,request=WriteTxnMarkers,type=RequestMetrics
kafka.network:name=RequestBytes,request=AddOffsetsToTxn,type=RequestMetrics
kafka.network:name=RequestBytes,request=AddPartitionsToTxn,type=RequestMetrics
kafka.network:name=RequestBytes,request=AlterConfigs,type=RequestMetrics
kafka.network:name=RequestBytes,request=AlterPartitionReassignments,type=RequestMetrics
kafka.network:name=RequestBytes,request=AlterReplicaLogDirs,type=RequestMetrics
kafka.network:name=RequestBytes,request=ApiVersions,type=RequestMetrics
kafka.network:name=RequestBytes,request=ControlledShutdown,type=RequestMetrics
kafka.network:name=RequestBytes,request=CreateAcls,type=RequestMetrics
kafka.network:name=RequestBytes,request=CreateDelegationToken,type=RequestMetrics
kafka.network:name=RequestBytes,request=CreatePartitions,type=RequestMetrics
kafka.network:name=RequestBytes,request=CreateTopics,type=RequestMetrics
kafka.network:name=RequestBytes,request=DeleteAcls,type=RequestMetrics
kafka.network:name=RequestBytes,request=DeleteGroups,type=RequestMetrics
kafka.network:name=RequestBytes,request=DeleteRecords,type=RequestMetrics
kafka.network:name=RequestBytes,request=DeleteTopics,type=RequestMetrics
kafka.network:name=RequestBytes,request=DescribeAcls,type=RequestMetrics
kafka.network:name=RequestBytes,request=DescribeConfigs,type=RequestMetrics
kafka.network:name=RequestBytes,request=DescribeDelegationToken,type=RequestMetrics
kafka.network:name=RequestBytes,request=DescribeGroups,type=RequestMetrics
kafka.network:name=RequestBytes,request=DescribeLogDirs,type=RequestMetrics
kafka.network:name=RequestBytes,request=ElectLeaders,type=RequestMetrics
kafka.network:name=RequestBytes,request=EndTxn,type=RequestMetrics
kafka.network:name=RequestBytes,request=ExpireDelegationToken,type=RequestMetrics
kafka.network:name=RequestBytes,request=Fetch,type=RequestMetrics
kafka.network:name=RequestBytes,request=FetchConsumer,type=RequestMetrics
kafka.network:name=RequestBytes,request=FetchFollower,type=RequestMetrics
kafka.network:name=RequestBytes,request=FindCoordinator,type=RequestMetrics
kafka.network:name=RequestBytes,request=Heartbeat,type=RequestMetrics
kafka.network:name=RequestBytes,request=IncrementalAlterConfigs,type=RequestMetrics
kafka.network:name=RequestBytes,request=InitProducerId,type=RequestMetrics
kafka.network:name=RequestBytes,request=JoinGroup,type=RequestMetrics
kafka.network:name=RequestBytes,request=LeaderAndIsr,type=RequestMetrics
kafka.network:name=RequestBytes,request=LeaveGroup,type=RequestMetrics
kafka.network:name=RequestBytes,request=ListGroups,type=RequestMetrics
kafka.network:name=RequestBytes,request=ListOffsets,type=RequestMetrics
kafka.network:name=RequestBytes,request=ListPartitionReassignments,type=RequestMetrics
kafka.network:name=RequestBytes,request=Metadata,type=RequestMetrics
kafka.network:name=RequestBytes,request=OffsetCommit,type=RequestMetrics
kafka.network:name=RequestBytes,request=OffsetDelete,type=RequestMetrics
kafka.network:name=RequestBytes,request=OffsetFetch,type=RequestMetrics
kafka.network:name=RequestBytes,request=OffsetForLeaderEpoch,type=RequestMetrics
kafka.network:name=RequestBytes,request=Produce,type=RequestMetrics
kafka.network:name=RequestBytes,request=RenewDelegationToken,type=RequestMetrics
kafka.network:name=RequestBytes,request=SaslAuthenticate,type=RequestMetrics
kafka.network:name=RequestBytes,request=SaslHandshake,type=RequestMetrics
kafka.network:name=RequestBytes,request=StopReplica,type=RequestMetrics
kafka.network:name=RequestBytes,request=SyncGroup,type=RequestMetrics
kafka.network:name=RequestBytes,request=TxnOffsetCommit,type=RequestMetrics
kafka.network:name=RequestBytes,request=UpdateMetadata,type=RequestMetrics
kafka.network:name=RequestBytes,request=WriteTxnMarkers,type=RequestMetrics
kafka.network:name=RequestQueueSize,type=RequestChannel
kafka.network:name=RequestQueueTimeMs,request=AddOffsetsToTxn,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=AddPartitionsToTxn,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=AlterConfigs,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=AlterPartitionReassignments,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=AlterReplicaLogDirs,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=ApiVersions,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=ControlledShutdown,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=CreateAcls,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=CreateDelegationToken,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=CreatePartitions,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=CreateTopics,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=DeleteAcls,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=DeleteGroups,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=DeleteRecords,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=DeleteTopics,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=DescribeAcls,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=DescribeConfigs,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=DescribeDelegationToken,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=DescribeGroups,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=DescribeLogDirs,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=ElectLeaders,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=EndTxn,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=ExpireDelegationToken,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=Fetch,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=FetchConsumer,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=FetchFollower,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=FindCoordinator,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=Heartbeat,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=IncrementalAlterConfigs,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=InitProducerId,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=JoinGroup,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=LeaderAndIsr,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=LeaveGroup,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=ListGroups,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=ListOffsets,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=ListPartitionReassignments,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=Metadata,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=OffsetCommit,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=OffsetDelete,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=OffsetFetch,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=OffsetForLeaderEpoch,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=Produce,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=RenewDelegationToken,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=SaslAuthenticate,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=SaslHandshake,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=StopReplica,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=SyncGroup,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=TxnOffsetCommit,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=UpdateMetadata,type=RequestMetrics
kafka.network:name=RequestQueueTimeMs,request=WriteTxnMarkers,type=RequestMetrics
kafka.network:name=RequestsPerSec,request=LeaderAndIsr,type=RequestMetrics,version=4
kafka.network:name=RequestsPerSec,request=UpdateMetadata,type=RequestMetrics,version=6
kafka.network:name=ResponseQueueSize,processor=0,type=RequestChannel
kafka.network:name=ResponseQueueSize,processor=1,type=RequestChannel
kafka.network:name=ResponseQueueSize,processor=2,type=RequestChannel
kafka.network:name=ResponseQueueSize,type=RequestChannel
kafka.network:name=ResponseQueueTimeMs,request=AddOffsetsToTxn,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=AddPartitionsToTxn,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=AlterConfigs,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=AlterPartitionReassignments,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=AlterReplicaLogDirs,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=ApiVersions,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=ControlledShutdown,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=CreateAcls,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=CreateDelegationToken,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=CreatePartitions,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=CreateTopics,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=DeleteAcls,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=DeleteGroups,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=DeleteRecords,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=DeleteTopics,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=DescribeAcls,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=DescribeConfigs,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=DescribeDelegationToken,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=DescribeGroups,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=DescribeLogDirs,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=ElectLeaders,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=EndTxn,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=ExpireDelegationToken,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=Fetch,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=FetchConsumer,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=FetchFollower,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=FindCoordinator,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=Heartbeat,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=IncrementalAlterConfigs,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=InitProducerId,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=JoinGroup,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=LeaderAndIsr,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=LeaveGroup,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=ListGroups,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=ListOffsets,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=ListPartitionReassignments,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=Metadata,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=OffsetCommit,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=OffsetDelete,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=OffsetFetch,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=OffsetForLeaderEpoch,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=Produce,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=RenewDelegationToken,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=SaslAuthenticate,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=SaslHandshake,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=StopReplica,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=SyncGroup,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=TxnOffsetCommit,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=UpdateMetadata,type=RequestMetrics
kafka.network:name=ResponseQueueTimeMs,request=WriteTxnMarkers,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=AddOffsetsToTxn,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=AddPartitionsToTxn,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=AlterConfigs,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=AlterPartitionReassignments,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=AlterReplicaLogDirs,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=ApiVersions,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=ControlledShutdown,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=CreateAcls,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=CreateDelegationToken,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=CreatePartitions,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=CreateTopics,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=DeleteAcls,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=DeleteGroups,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=DeleteRecords,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=DeleteTopics,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=DescribeAcls,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=DescribeConfigs,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=DescribeDelegationToken,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=DescribeGroups,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=DescribeLogDirs,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=ElectLeaders,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=EndTxn,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=ExpireDelegationToken,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=Fetch,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=FetchConsumer,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=FetchFollower,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=FindCoordinator,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=Heartbeat,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=IncrementalAlterConfigs,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=InitProducerId,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=JoinGroup,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=LeaderAndIsr,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=LeaveGroup,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=ListGroups,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=ListOffsets,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=ListPartitionReassignments,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=Metadata,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=OffsetCommit,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=OffsetDelete,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=OffsetFetch,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=OffsetForLeaderEpoch,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=Produce,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=RenewDelegationToken,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=SaslAuthenticate,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=SaslHandshake,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=StopReplica,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=SyncGroup,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=TxnOffsetCommit,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=UpdateMetadata,type=RequestMetrics
kafka.network:name=ResponseSendTimeMs,request=WriteTxnMarkers,type=RequestMetrics
kafka.network:name=TemporaryMemoryBytes,request=Fetch,type=RequestMetrics
kafka.network:name=TemporaryMemoryBytes,request=Produce,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=AddOffsetsToTxn,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=AddPartitionsToTxn,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=AlterConfigs,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=AlterPartitionReassignments,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=AlterReplicaLogDirs,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=ApiVersions,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=ControlledShutdown,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=CreateAcls,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=CreateDelegationToken,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=CreatePartitions,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=CreateTopics,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=DeleteAcls,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=DeleteGroups,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=DeleteRecords,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=DeleteTopics,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=DescribeAcls,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=DescribeConfigs,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=DescribeDelegationToken,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=DescribeGroups,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=DescribeLogDirs,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=ElectLeaders,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=EndTxn,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=ExpireDelegationToken,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=Fetch,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=FetchConsumer,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=FetchFollower,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=FindCoordinator,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=Heartbeat,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=IncrementalAlterConfigs,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=InitProducerId,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=JoinGroup,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=LeaderAndIsr,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=LeaveGroup,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=ListGroups,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=ListOffsets,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=ListPartitionReassignments,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=Metadata,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=OffsetCommit,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=OffsetDelete,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=OffsetFetch,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=OffsetForLeaderEpoch,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=Produce,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=RenewDelegationToken,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=SaslAuthenticate,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=SaslHandshake,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=StopReplica,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=SyncGroup,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=TxnOffsetCommit,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=UpdateMetadata,type=RequestMetrics
kafka.network:name=ThrottleTimeMs,request=WriteTxnMarkers,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=AddOffsetsToTxn,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=AddPartitionsToTxn,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=AlterConfigs,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=AlterPartitionReassignments,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=AlterReplicaLogDirs,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=ApiVersions,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=ControlledShutdown,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=CreateAcls,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=CreateDelegationToken,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=CreatePartitions,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=CreateTopics,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=DeleteAcls,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=DeleteGroups,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=DeleteRecords,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=DeleteTopics,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=DescribeAcls,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=DescribeConfigs,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=DescribeDelegationToken,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=DescribeGroups,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=DescribeLogDirs,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=ElectLeaders,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=EndTxn,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=ExpireDelegationToken,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=Fetch,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=FetchConsumer,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=FetchFollower,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=FindCoordinator,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=Heartbeat,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=IncrementalAlterConfigs,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=InitProducerId,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=JoinGroup,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=LeaderAndIsr,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=LeaveGroup,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=ListGroups,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=ListOffsets,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=ListPartitionReassignments,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=Metadata,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=OffsetCommit,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=OffsetDelete,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=OffsetFetch,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=OffsetForLeaderEpoch,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=Produce,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=RenewDelegationToken,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=SaslAuthenticate,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=SaslHandshake,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=StopReplica,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=SyncGroup,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=TxnOffsetCommit,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=UpdateMetadata,type=RequestMetrics
kafka.network:name=TotalTimeMs,request=WriteTxnMarkers,type=RequestMetrics
```


## Install elasticsearch 
```
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-oss-7.8.0-darwin-x86_64.tar.gz
cd elasticsearch-7.8.0
bin/elasticsearch

curl localhost:9200
```

## Install Kibana
```
wget https://artifacts.elastic.co/downloads/kibana/kibana-7.8.0-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/kibana/kibana-oss-7.8.0-linux-x86_64.tar.gz
cd kibana-7.8.0-linux-x86_64/
vi config/kibana.yaml
server.host: "0.0.0.0"
```


## Install logstash 
```
wget https://artifacts.elastic.co/downloads/logstash/logstash-oss-7.8.0.tar.gz
tar xvf logstash-oss-7.8.0.tar.gz
cd logstash-7.8.0
bin/logstash-plugin install logstash-input-jmx
/home/freepsw/sw/logstash-7.8.0
```


## Run logstash to collect apache kafak jmx metrics
```

/home/freepsw/sw/logstash-7.8.0/bin/logstash  -f config
```


```conf
{
  "host" : "localhost",
  "port" : 9999,
  "alias" : "kafkabroker1",
  "queries" : [
  {
    "object_name" : "kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec",
    "attributes" : [ "OneMinuteRate" ],
    "object_alias" : "${type}.${name}"
  },
  {
    "object_name" : "kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec",
    "attributes" : [ "OneMinuteRate" ],
    "object_alias" : "${type}.${name}"
  },
  {
    "object_name" : "kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec",
    "attributes" : [ "OneMinuteRate" ],
    "object_alias" : "${type}.${name}"
  },
  {
    "object_name" : "kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions",
    "attributes" : [ "Value" ],
    "object_alias" : "${type}.${name}"
  },
  {
    "object_name" : "kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce",
    "attributes" : [ "Mean" ],
    "object_alias" : "${name}.${request}"
  },
  {
    "object_name" : "kafka.network:type=RequestMetrics,name=TotalTimeMs,request=FetchConsumer",
    "attributes" : [ "Mean" ],
    "object_alias" : "${name}.${request}"
  }
 ]
}
```