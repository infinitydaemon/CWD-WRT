 <p align="center">
 <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://cwd.systems/img/cwd-logo.png">
    <img src="https://cwd.systems/img/cwd-logo.png"  alt="CWD Systems">
  </picture>
  </p>
  <br>

### Information
Default LAN IP address is 192.168.2.1. Policy based VPN routing is disabled by default.

### Requirements

You need the following tools to compile OpenWrt, the package names vary between
distributions. A complete list with distribution specific packages is found in
the [Build System Setup](https://openwrt.org/docs/guide-developer/build-system/install-buildsystem)
documentation.

### Quikstart Guide to Build Firmware

You will need to build the firmware using branch **openwrt-21.02**, not the master branch

```
git clone https://github.com/infinitydaemon/CWD-WRT.git
cd CWD-WRT
git branch -a
git checkout openwrt-21.02
./scripts/feeds update -a
./scripts/feeds install -a 
```

Run `make menuconfig` and configure the target system & firmware packages.
For the first build, run the below commands to download tool/packages and compile:

```
make download -j8
make V=s -j1
```

It is suggested to build with single thread. You can also build with multi-thread:

`make V=s -j$(nproc)`

For the second build 
```
cd CWD-WRT
git pull
./scripts/feeds update -a
./scripts/feeds install -a
make defconfig
make download -j8
make V=s -j$(nproc)
```

### Related Repositories

The main repository uses multiple sub-repositories to manage packages of
different categories. All packages are installed via the OpenWrt package
manager called `opkg`. If you're looking to develop the web interface or port
packages to OpenWrt, please find the fitting repository below.

* [LuCI Web Interface](https://github.com/openwrt/luci): Modern and modular
  interface to control the device via a web browser.

* [OpenWrt Packages](https://github.com/openwrt/packages): Community repository
  of ported packages.

* [OpenWrt Routing](https://github.com/openwrt/routing): Packages specifically
  focused on (mesh) routing.

* [OpenWrt Video](https://github.com/openwrt/video): Packages specifically
  focused on display servers and clients (Xorg and Wayland).

### Documentation

* [Quick Start Guide](https://openwrt.org/docs/guide-quick-start/start)
* [User Guide](https://openwrt.org/docs/guide-user/start)
* [Developer Documentation](https://openwrt.org/docs/guide-developer/start)
* [Technical Reference](https://openwrt.org/docs/techref/start)

### Support Community

* [Forum](https://forum.openwrt.org): For usage, projects, discussions and hardware advise.
* [Support Chat](https://webchat.oftc.net/#openwrt): Channel `#openwrt` on **oftc.net**.

### Developer Community

* [Bug Reports](https://bugs.openwrt.org): Report bugs in OpenWrt
* [Dev Mailing List](https://lists.openwrt.org/mailman/listinfo/openwrt-devel): Send patches
* [Dev Chat](https://webchat.oftc.net/#openwrt-devel): Channel `#openwrt-devel` on **oftc.net**.

## License

OpenWrt is licensed under GPL-2.0
