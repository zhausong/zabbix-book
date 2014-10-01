关于Redis的监控，请参考   
http://redis.readthedocs.org/en/latest/server/info.html
###INFO [section]
以一种易于解释（parse）且易于阅读的格式，返回关于 Redis 服务器的各种信息和统计数值。    
通过给定可选的参数 section ，可以让命令只返回某一部分的信息：  
```
server : 一般 Redis 服务器信息，包含以下域：

redis_version : Redis 服务器版本
redis_git_sha1 : Git SHA1
redis_git_dirty : Git dirty flag
os : Redis 服务器的宿主操作系统
arch_bits : 架构（32 或 64 位）
multiplexing_api : Redis 所使用的事件处理机制
gcc_version : 编译 Redis 时所使用的 GCC 版本
process_id : 服务器进程的 PID
run_id : Redis 服务器的随机标识符（用于 Sentinel 和集群）
tcp_port : TCP/IP 监听端口
uptime_in_seconds : 自 Redis 服务器启动以来，经过的秒数
uptime_in_days : 自 Redis 服务器启动以来，经过的天数
lru_clock : 以分钟为单位进行自增的时钟，用于 LRU 管理
clients : 已连接客户端信息，包含以下域：

connected_clients : 已连接客户端的数量（不包括通过从属服务器连接的客户端）
client_longest_output_list : 当前连接的客户端当中，最长的输出列表
client_longest_input_buf : 当前连接的客户端当中，最大输入缓存
blocked_clients : 正在等待阻塞命令（BLPOP、BRPOP、BRPOPLPUSH）的客户端的数量
memory : 内存信息，包含以下域：

used_memory : 由 Redis 分配器分配的内存总量，以字节（byte）为单位
used_memory_human : 以人类可读的格式返回 Redis 分配的内存总量
used_memory_rss : 从操作系统的角度，返回 Redis 已分配的内存总量（俗称常驻集大小）。这个值和 top 、 ps 等命令的输出一致。
used_memory_peak : Redis 的内存消耗峰值（以字节为单位）
used_memory_peak_human : 以人类可读的格式返回 Redis 的内存消耗峰值
used_memory_lua : Lua 引擎所使用的内存大小（以字节为单位）
mem_fragmentation_ratio : used_memory_rss 和 used_memory 之间的比率
mem_allocator : 在编译时指定的， Redis 所使用的内存分配器。可以是 libc 、 jemalloc 或者 tcmalloc 。
在理想情况下， used_memory_rss 的值应该只比 used_memory 稍微高一点儿。
当 rss > used ，且两者的值相差较大时，表示存在（内部或外部的）内存碎片。
内存碎片的比率可以通过 mem_fragmentation_ratio 的值看出。
当 used > rss 时，表示 Redis 的部分内存被操作系统换出到交换空间了，在这种情况下，操作可能会产生明显的延迟。
Because Redis does not have control over how its allocations are mapped to memory pages, high used_memory_rss is often the result of a spike in memory usage.

当 Redis 释放内存时，分配器可能会，也可能不会，将内存返还给操作系统。
如果 Redis 释放了内存，却没有将内存返还给操作系统，那么 used_memory 的值可能和操作系统显示的 Redis 内存占用并不一致。
查看 used_memory_peak 的值可以验证这种情况是否发生。
persistence : RDB 和 AOF 的相关信息

stats : 一般统计信息
replication : 主/从复制信息
cpu : CPU 计算量统计信息
commandstats : Redis 命令统计信息
cluster : Redis 集群信息
keyspace : 数据库相关的统计信息

除上面给出的这些值以外，参数还可以是下面这两个：
all : 返回所有信息
default : 返回默认选择的信息
当不带参数直接调用 INFO 命令时，使用 default 作为默认参数。

不同版本的 Redis 可能对返回的一些域进行了增加或删减。
因此，一个健壮的客户端程序在对 INFO 命令的输出进行分析时，应该能够跳过不认识的域，并且妥善地处理丢失不见的域。

可用版本：
>= 1.0.0
时间复杂度：
O(1)
返回值：
```
具体请参见下面的测试代码。  
```
 redis-cli -p 6383
127.0.0.1:6383> info
# Server
redis_version:2.8.8
redis_git_sha1:00000000
redis_git_dirty:0
redis_build_id:bafd09db0ea64ad0
redis_mode:standalone
os:Linux 3.11.0-24-generic x86_64
arch_bits:64
multiplexing_api:epoll
gcc_version:4.6.3
process_id:13724
run_id:05f48727373c94eae75b2634eb6cd99ff04c5592
tcp_port:6383
uptime_in_seconds:1329486
uptime_in_days:15
hz:10
lru_clock:2881420
config_file:/etc/redis/6383.conf

# Clients
connected_clients:267
client_longest_output_list:0
client_biggest_input_buf:0
blocked_clients:0

# Memory
used_memory:2597003592
used_memory_human:2.42G
used_memory_rss:3247697920
used_memory_peak:5300846120
used_memory_peak_human:4.94G
used_memory_lua:29696
mem_fragmentation_ratio:1.25
mem_allocator:jemalloc-3.2.0

# Persistence
loading:0
rdb_changes_since_last_save:1408782845
rdb_bgsave_in_progress:0
rdb_last_save_time:1410866014
rdb_last_bgsave_status:ok
rdb_last_bgsave_time_sec:33
rdb_current_bgsave_time_sec:-1
aof_enabled:0
aof_rewrite_in_progress:0
aof_rewrite_scheduled:0
aof_last_rewrite_time_sec:-1
aof_current_rewrite_time_sec:-1
aof_last_bgrewrite_status:ok
aof_last_write_status:ok

# Stats
total_connections_received:13209166
total_commands_processed:10099828580
instantaneous_ops_per_sec:2837
rejected_connections:36242
sync_full:0
sync_partial_ok:0
sync_partial_err:0
expired_keys:16591179
evicted_keys:0
keyspace_hits:2077408344
keyspace_misses:2433838286
pubsub_channels:0
pubsub_patterns:0
latest_fork_usec:97455

# Replication
role:master
connected_slaves:0
master_repl_offset:0
repl_backlog_active:0
repl_backlog_size:1048576
repl_backlog_first_byte_offset:0
repl_backlog_histlen:0

# CPU
used_cpu_sys:88227.02
used_cpu_user:74898.65
used_cpu_sys_children:6.00
used_cpu_user_children:47.59

# Keyspace
db0:keys=594128,expires=578561,avg_ttl=74150277
db5:keys=755192,expires=144,avg_ttl=63212667
db12:keys=6,expires=0,avg_ttl=0
```
