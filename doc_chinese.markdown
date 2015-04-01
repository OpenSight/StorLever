---
layout: page
title: 文档
---

# StorLever是什么？

StorLever是一个部署在Linux服务器上的配置、管理、监控系统，用于管理服务器上的各种网络和存储资源（功能）。它提供了一组精心设计的RESTful风格的Web可编程接口，以及一个简介的Web操作面板。

StorLever建立在Linux系统中各种成熟的命令行管理工具之上，通过脚本来调用底层命令来实现。它的主要目的是隐藏底层各种管理工具的使用细节，向用户提供一致的、简单的操作接口，从而减轻Linux服务器系统管理工作的难度。StorLever向系统管理员提供了一个非常简单的Web操作面板，一方面，减轻了系统管理员的学习难度，增强了他们的操作体验，另一方面，使得管理员可以在他的PC端轻松地管理远程存储服务器而无需到现场进行维护。

除此之外，StorLever还有一个更强大的特点，它提供了一组RESTful风格（HTTP+JSON）的API来远程管理Linux系统。基于这个功能，运行在其他主机上的第三方的服务器管理软件（例如某些中心管理系统），无论它使用什么语言开发，或者运行在什么平台（Windows? Linux? Unix?），都能够非常便捷地接管安装有StorLever的服务器。RESTful风格的API的输出结果，既便于普通人阅读理解，也便于计算机程序分析。当今任何一种程序设计语言都提供了成熟的用于处理HTTP协议和解释JSON字符串的工具库，因此针对RESTful风格的API进行开发，是一件十分容易的事情。

StorLever重点是放在对Linux系统中各种存储资源的管理，这是Linux系统管理中最困难以及细节最复杂的部分，这些资源包括块设备，LVM，软阵列，文件系统，NAS，IP-SAN等等。管理这些资源常常是系统管理员的噩梦，但却又是十分重要的工作，成功配置好这些资源通常要花费管理员一两周甚至更多的时间，但是尽管如此，却还不能确保这些存储系统是工作在最好的状态。StorLever就是应对这种情况的理想的解决方案。StorLever的积累了丰富的存储系统管理经验并输出一个简单清晰的接口，能够帮助系统管理人员迅速地对服务器的存储系统进行最佳配置。

StorLever不是一个封闭的软件，它提供众多存储管理功能的同时，也是一个可扩展的框架。任何人如果希望使用StorLever的框架管理其他资源对象，只需要单独开发一个StorLever的插件即可，而该插件是完全独立项目，无需对StorLever项目做任何的修改。

StorLever由纯Python开发，因此它很简单，容易理解，稳定可靠，部署和开发都很容易。 StorLever的设计原则是简单，可扩展，容易使用。

## 为什么需要StorLever

一般情况下，Linux的发行版本会为系统管理员提供两种方式的本地操作接口，即命令行接口和图形界面。这两种方式曾经是管理Linux系统最流行的方式。随着网络，尤其是因特网的快速发展，Linux系统常常是部署在远程的服务器（例如虚拟主机）上，上述两种本地接口无法应用于这种环境，管理员喜欢使用SSH登陆到远程的主机来管理配置它们。通过SSH方式来管理是十分灵活的，但却也是困难的，痛苦的，而且耗时的。因此，很多Web控制面板的项目就被开发出来帮助系统管理员轻松地完成配置管理工作。

随着云计算的流行普及，管理员需要同时管理越来越多的虚拟主机，所以他们需要一些中心管理平台的协助。中心管理平台通过特定的网络协议（接口）连接上百台服务器，对其进行统一的配置和监控。而针对存储子系统，这些接口都不成熟，或者太复杂，一般人都无法阅读或者难于使用。

因此，StorLever被设计出来用于解决上述的问题。我们认为简单就是最好的解决方案。RESTful风格的WebAPI凭借其简单易用，方便调试，迅速成为了目前云计算系统最流行的接口风格，所有主流的云服务，无一例外都提供RESTful风格的API。因此，StorLever选择了RESTful风格的API，向用户提供了一个最简单，且平台无关的操作方式。

有很多开源项目（例如openfiler）也有类似的想法，但它们和StorLever还是有很大的差别。

* Openfiler或者freeNAS，

> 两者都是一个独立的存储操作系统，带有完整的定制操作系统和一整套管理操作工具。而StorLever仅仅是一组管理API，用于帮助用户减轻存储资源的管理工作。它基于Linux主流发行版（主要是RHEL/CentOS）中自带的系统管理工具，这些Linux发行版以及其中的管理工具都是由一帮资深的Linux系统专家维护，并且通过多年的使用和积累，已经被验证十分稳定并且适合企业级应用。StorLever也基于一些由RHEL/CentOS维护的软件包（RPM），不过用户自由选择是否需要此管理功能。

* Ajenti

> Ajenti是另一个十分优秀的开源项目，它也是由纯python开发，主要目的是为Linux虚拟主机提供一个Web控制面板，同时，它也支持插件方式扩展功能。它是一个通用型的控制面板，包括Linux上各种管理工具，可是并不是特别针对存储管理子系统，因此很多存储资源它的管理能力十分有限。同时，更重要的，它并对其它系统提供远程调用API。

* OpenLMI

> OpenLMI是一个很StorLever十分类似的项目，而且已经包含在RHEL 7的RPM包中。它也向管理员提供了一组API接口来对Linux进行远程配置、管理、监视。但我们认为，这个项目的实现方式是不合理的，OpenLMIi是基于一种称为“WBEM”的技术来实现它的扩展性。相比于RESTful，WBEM是一种非常复杂的技术框架，最初由大型企业例如微软、康柏、思科等在90年代发起，用于支持企业级分布式计算环境。它由很多组件和协议种类组成，灵活且可靠，但对于很多人来说都会感到很难理解，很难部署，很难开发。它在网络中传输的报文也是不可直接被人们阅读的。因此我们认为用这么复杂的架构及技术实现Linux的远程管理并不合适。我们需要用更简单更有生命力的技术结构。相比于OpenLMI，StorLever是一个实现类似功能的轻量级的解决方案。

## StorLever的亮点

* 集成了Linux系统的多种存储管理技术，包括LVM，阵列，NAS/SAN等等
* 提供多种操作接口，包括RESTful风格API，Web UI，CLI（另外项目），SDK（另外项目）
* 可扩展，添加插件十分容易
* 简单，纯Python

## StorLever所管理的系统资源

存储资源，我们是指系统中的各种存储实体及相关技术，以下列出了StorLever所能够管理的Linux系统中的存储资源。

* Block device
* SCSI device
* MD Raid
* Mega Raid (LSI chip, through extension)
* LVM
* XFS
* EXT4
* NFS Client & Server
* SAMBA Server
* FTP Server
* iSCSI Initiator & Target(TGT)
* SMART

以下列出了StorLever所管理的Linux系统中的网络资源。

* Ethernet Interface
* Bond Interface
* Route Table
* DNS Config

还有下列Linux系统中的其他系统资源

* NTP
* SNMP
* User&Group
* Host
* Zabbix Agent
* Mail Agent
* HTTP

# StorLever的软件架构

StorLever项目的总体软件结构如下图所示。

![StorLever软件结构](images/arch.png)

> 上图中，黄色框内是StorLever的内部结构，StorLever是一个基于[Pyramid](http://www.pylonsproject.org/)框架的Web应用（即WSGI APP），内部有三个主要部分（层次），分别是管理器，REST API模块，和Web面板模块。在实际部署中，StorLever默认使用Waitress作为Web服务器（即WSGI Server)，系统管理员可以通过浏览器访问StorLever的Web界面，也可以直接调用它的REST API。而部署在其他主机上的中心管理系统则可以通过对应的工具库或者SDK调用StorLever的REST API，对目标系统进行远程监控管理。
若用户需要扩展StorLever的功能和接口（例如需要管理其他对象），则可以对其开发的扩展程序（Plugin），通过Python语言默认提供的程序扩展方式（setuptools的entry_points机制），对StorLever的三个主要部分进行补充。补丁后的StorLever即可以输出对应的接口和Web界面，就像是StorLever项目的原生接口一般。

> 下面分别简单描述StorLever的三个主要部分

## 管理器层

管理器层中包含很多管理器类，每一个管理器类有一个对应的单例的管理器对象，每个对象负责管理Linux中一个子系统，例如LVM，FTP，文件系统等等。这些管理器对象是StorLever的核心业务逻辑，位于StorLever的最底层，向上层提供面向对象的调用接口。

## REST接口层

该层负责实现RESTful风格的API接口。每一个API调用都对应该层的一个View函数，这些函数的处理逻辑大致相同，1）从客户端获取HTTP请求，2）检查客户提供的调用参数，3）调用管理器层的接口获取结果，4）将结果返回给客户端

该层调用底层的管理器层的接口，并向上层提供RESTful API。

## Web界面层

该层主要负责实现Web控制面板界面，它包含控制面板使用到各种页面逻辑，菜单项管理，页面模板，JS脚本，CSS格式，各种静态资源。它通过JS脚本在客户端调用StorLever的RESTful API来获取系统信息（或者配置系统），并在浏览器中进行显示。Web前端JS基于开源项目AngularJS框架进行开发，并支持用户注册新菜单项和外部JS脚本，实现其扩展性。
该层主要是调用REST接口层提供的API，并向管理员提供了一个简洁实用的WEB控制面板界面。


# StorLever如何使用

> 有关StorLever安装、部署、使用方面的资料，请参考源码目录中的README文档。

## 安装与部署

StorLever是一个轻量级的Web应用，目的是于减轻CentOS/RHEL服务器上各种存储资源的管理工作。它使用纯Python语言开发，基于一个出色的Python的Web应用框架[Pyramid](http://www.pylonsproject.org/)来构建自己的Web服务。同时，利用了[PasteDeploy](http://pythonpaste.org/deploy/)系统来部署它的WSGI服务器/应用的配置。

StorLever要求Python 2.6或以上的运行环境，Python 3K暂不支持

### 从源码安装

从StorLever的github主要下载并在你的Linux系统中解包StorLever的源码包。StorLever能够安装运行在CentOS/RHEL 6系统上，而其他Linux发行版，例如Fedora, Ubuntu，StorLever未做支持。

在StorLever项目源码根目录，输入以下命令即可将StorLever安装至你的系统。

    $python setup.py install

这个安装过程中，系统将会检查所有StorLever依赖的Python包并尝试从pypi下载并安装它们

### 配置

安装完成后，StorLever将会将它的paste配置文件安装到你的系统中的以下路径。

    $ /etc/storlever.ini

StorLever在启动时将会默认读入此配置文件。你能够对该文件进行编辑，从而改变StorLever的部署配置。建议保留大部分的配置项，除了服务器监听端口。StorLever配置文件中默认使用6543作为端口，可以更改此选项为你系统合适的端口号。

### 启动

在安装并配置完成后，你可以用两种方式启动StorLever的服务：

* Daemon模式

> 在上述的安装过程中，StorLever已经将它的init脚本安装到系统的合适位置（/etc/init.d），你能够利用此脚本以Daemon模式启动StorLever，输入如下命令：

    $ service storlever startup

> 这种情况下，StorLever将会读入paste配置文件（/etc/storlever.ini），它的stderr/stdout将会从定向置/dev/null

* Foreground模式

> 如果你想调试或者测试StorLever，你可能会希望以前景模式来启动StorLever服务，这样你就能够观察到StorLever在stderr/stdout中输出的调试内容。输入如下命令即可以前景模式启动StorLever。

    $ pserve [StorLever paste 配置文件]

> StorLever的paste配置文件可以使用StorLever项目根目录下的ini文件

以上步骤完成后，相信StorLever已经正在工作了，正式开始体验吧！！！

### 系统引导时启动

如果你想在系统引导的时候启动StorLever服务，你能够利用chkconfig工具来将StorLever的服务脚本加入到系统的rc.d目录中。

    $ chkconfig --add storlever

### 针对开发者

如果你是一个想要调试或者开发StorLever的开发者，你可能只是想运行一下StorLever做测试，而不想直接将StorLever安装到你的系统。如果这样，你不应该按照上述的指引安装StorLever,你可以在StorLever的项目根目录下输入如下命令：

    $ python setup.py develop

此命令将不会把StorLever安装到你系统python的site-packages目录，而仅仅是在site-packages目录建立一个链接到StorLever项目的源码目录中。而且，该过程也不会将init脚本和paste配置文件安装到你系统的/etc/目录下。

然后，你能够输入以下的命令以前景模式运行StorLever服务。

    $ pserve --reload storlever_dev.ini

该命令能够在你的代码发生变化时自动重新装载应用，而且能够输出很多有用的调试/出错信息。

## 使用

当你成功安装并在你的系统中启动了StorLever服务后，你能够通过两种方式使用StorLever。默认情况下，StorLever服务将会监听TCP 6543端口。

### 使用Web控制面板

在你本地的浏览器中输入如下如下的URL即可进行StorLever的用户登录页面。

    http://[host_ip]:[port]/

[host_ip]是运行StorLever的主机的IP地址，[port]是StorLever服务监听的端口号，默认的登陆用户名为admin,密码为123456。

### 使用RESTful API

StorLever另外一个重要特色是提供了一组RESTful风格的API，你可以用一个http工具或者浏览器来测试它们。所有API的URL都是以下面的前缀开始。

    http://[host_ip]:[port]/storlever/api/

你能够参考StorLever WIKI的API手册来获取更多信息。

# StorLever API手册

StorLever的API是RESTful风格的Web Service，参考手册在StorLever的[Wiki](https://github.com/OpenSight/StorLever/wiki/API-Reference-v1.0)中提供。


# 如何参与StorLever的开发

StorLever的最新代码托管在Github上，项目的URL是：

    https://github.com/OpenSight/StorLever

开发者能够利用Github的issue系统来向StorLever的维护人员和开发人员反馈Bugs和提出新需求

如果开发者想参与StorLever的开发，向StorLever贡献他们的代码。我们建议使用Github提供的Fork + Pull Request模式向StorLever的master分支推送你的修改。如果StorLever采纳了你的代码，我们将会把你的名称放入StorLever的作者列表中，感谢大家的参与。

# 如何开发StorLever的插件

如果你想开发一个StorLever的扩展（插件），你应该遵循和StorLever一致的习惯和代码风格。StorLever的扩展（插件）应该和StorLever保持相同的软件结构，也应该包含三个部分：管理器，REST API， Web面板三个主要部分，并基于Pyramid框架输出其Web服务。
我们将会在Wiki中提供一份How-to文档来详细解释插件开发的主题。StorLever的项目源码中也包含了一个扩展程序（megaraid）的样列供开发者参考