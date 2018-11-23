# LanhuNo1
蓝虎团队第一个运维项目

------------------------------------------------
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

-----------------------------------------
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

------------------------
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

