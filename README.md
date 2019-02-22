# LanhuNo1
蓝虎团队第一个运维项目

---
问题1：vagrant安装插件vagrant-vbguest遇到墙，报错如下：
‘’‘
Vagrant failed to load a configured plugin source. This can be caused
by a variety of issues including: transient connectivity issues, proxy
filtering rejecting access to a configured plugin source, or a configured
plugin source not responding correctly. Please review the error message
below to help resolve the issue:
  SSL_connect SYSCALL returned=5 errno=0 state=SSLv3/TLS write client hello (https://gems.hashicorp.com/specs.4.8.gz)
Source: https://gems.hashicorp.com/
’‘’
解决办法：
    $ gem sources --add https://gems.ruby-china.com/ --remove https://rubygems.org/
    $ gem sources -l https://gems.ruby-china.com
    $ vagrant plugin install vagrant-vbguest --plugin-clean-sources --plugin-source https://gems.ruby-china.com/

---
问题2: vagrant虚拟机不能挂载共享目录，报错如下：
‘’‘
Vagrant was unable to mount VirtualBox shared folders. This is usually
because the filesystem "vboxsf" is not available. This filesystem is
made available via the VirtualBox Guest Additions and kernel module.
Please verify that these guest additions are properly installed in the
guest. This is not a bug in Vagrant and is usually caused by a faulty
Vagrant box. For context, the command attempted was:
mount -t vboxsf -o uid=1000,gid=1000 share /share
The error output from the command was:
/sbin/mount.vboxsf: mounting failed with the error: No such device
’‘’
解决办法：
文件VagrantFile中
    config.vm.synced_folder ".", "/share"
修改为：
    config.vm.synced_folder ".", "/share",type:"nfs",nfs_udp: false

---
问题3:vagrant up时报错如下：
‘’‘
An error occurred during installation of VirtualBox Guest Additions 5.2.22. Some functionality may not work as intended.
In most cases it is OK that the "Window System drivers" installation failed.
’‘’
解决办法：https://github.com/dotless-de/vagrant-vbguest/issues/298
I have been able to workaround this by logging on with with vagrant ssh and running a
sudo yum update -y
Then once that completed I disconnected from ssh and re-ran vagrant reload --provision
The guest-additions were then showing as running OK.

---
###基本监控项(数据库/文本/接口)显示内容配置规则
    1. 显示内容：深圳指数#szzs=3000#
        预览效果：深圳指数3000
        szzs是自定义键名，其值由采集规则从数据库/文件/接口中采集并存入采集表，前端从采集表中获取
    2. 显示内容：行情数据库连接状态@DB_CONNECTION=1@
        预览效果：行情数据库连接状态+64X64圆形颜色图标表示状态               
        DB_CONNECTION为约定键名，表示数据库连接状态
        1：连接正常，绿色表示
        2：手工修改为正常状态，深绿色表示
        -1：连接异常，红色表示
        -2：采集规则错误
        0/null/或者获取不到数据：尚未采集到，灰色表示
        数据库采集时，需采集数据库连接状态
    3. 显示内容：行情接口状态@URL_CONNECTION=1@
        预览效果：行情接口状态+64X64圆形颜色图标表示状态               
        URL_CONNECTION为约定键名，表示接口状态
        1：连接正常，绿色表示
        2：手工修改为正常状态，深绿色表示
        -1：连接异常，红色表示
        -2：脚本执行异常
        0/null/或者获取不到数据：尚未采集到，灰色表示
        接口采集时，需采集接口状态
    4. 显示内容：深圳行情文件状态@FILE_EXIST=1@
        预览效果：深圳行情文件状态+64X64圆形颜色图标表示状态               
        FILE_EXIST为约定键名，表示文件是否存在
        1：文件正常存在，绿色表示
        2：手工修改为正常状态，深绿色表示
        -1：文件不存在，红色表示
        -2：脚本执行异常
        0/null/或者获取不到数据：尚未采集到，灰色表示
        文件采集时，需采集文件是否存在
    解释：##内的变量用数字或字符串展示，@@内的变量用状态图标展示
---        
###基本监控项数据库采集规则
        配置内容：select @keyA=fieldA@, @b=fieldB@ from tabA where id=1;
        解释：fieldA,fieldB为表tabA的具体字段；
            keyA,keyB为采集存储的键名，其值为单值字符串，如'1000'。
        * 基本监控项的数据必须是单行数据
---
HelloWorld=1000
###基本监控项文件和接口采集规则
        配置内容：shell脚本对文件内容进行抽提，返回形如"{keyA='valueA',keyB='valueB'}"json字符串
        如：
            从本文档中提取HelloWorld的值，可以配置:
            echo {keyA='valueA',keyB='valueB'}
###控项文件和接口采集规则
        配置内容：入参配置采用json串配置，实例如{"params1"：“xxx”，“params2”：“xxx”}
    
    
    
    
#系统介绍
随着行业客户日益庞大的软硬件系统的堆积建设，IDC机房的运维管理工作越来越复杂。为有效简化机房与各业务系统的运维管理工作，我司为行业客户落地打造了一款强大的看板系统。
看板系统基于蓝鲸智云平台开发，具有对计算机集群网络的跨云集中管理功能。看板系统与蓝鲸智云平台的配置管理平台、作业平台和标准运维形成一个有机整体，可编排满足各种客户具体业务需求的日常运维场景，系统以轮播的方式对各个岗位的运维场景进行统一展示，不同岗位的人员只轮播该岗位相关场景；同时各个运维场景在日常运维过程中可能会产生各种告警事件，告警事件在轮播场景中将会得到一目了然的展现，同时也会通过邮件、短信、微信等多种通讯方式告知相关人员。
看板系统的功能模块包括首页概览、监控项管理、场景管理、场景编排、场景轮播、配置管理和权限管理等功能模块，通过任务调度器调度采集各个业务系统的状态和数据，与自动化运维结合，不断优化、总结并固化一批自动化运维流程，以看板的形式进行统一监控管理，从而大大减轻了运维人员的日常维护工作，把运维人员从日常的琐碎事务中解放出来，以更多的精力关注业务系统的整体健康态势，出了问题能够迅速定位问题环节并予以解决，更加有效地保障了业务系统的健康运行。



    