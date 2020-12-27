# Build ocaml bits unless rpmbuild was run with --without ocaml
# or ocamlopt is missing (the xen makefile doesn't build ocaml bits if it isn't there)
%define with_ocaml 0
%define build_ocaml 0
# Build with docs unless rpmbuild was run with --without docs
%define build_docs %{?_without_docs: 0} %{?!_without_docs: 1}
# Build without stubdom unless rpmbuild was run with --with stubdom
%define build_stubdom %{?_with_stubdom: 1} %{?!_with_stubdom: 0}
# Build without qemu-traditional unless rpmbuild was run with --with qemutrad
%define build_qemutrad %{?_with_qemutrad: 1} %{?!_with_qemutrad: 0}
# build with ovmf from edk2-ovmf unless rpmbuild was run with --without ovmf
%define build_ovmf %{?_without_ovmf: 0} %{?!_without_ovmf: 1}
# set to 0 for archs that don't use qemu or ovmf (reduces build dependencies)
%ifnarch x86_64 %{ix86}
%define build_qemutrad 0
%define build_ovmf 0
%endif
%if ! %build_qemutrad
%define build_stubdom 0
%endif
# Build with xen hypervisor unless rpmbuild was run with --without hyp
%define build_hyp %{?_without_hyp: 0} %{?!_without_hyp: 1}
# build xsm support unless rpmbuild was run with --without xsm
# or required packages are missing
%define with_xsm 0
%define build_xsm 0
# cross compile 64-bit hypervisor on ix86 unless rpmbuild was run
# with --without crosshyp
%define build_crosshyp %{?_without_crosshyp: 0} %{?!_without_crosshyp: 1}
%ifnarch %{ix86}
%define build_crosshyp 0
%else
%if ! %build_crosshyp
%define build_hyp 0
%endif
%endif
# no point in trying to build xsm on ix86 without a hypervisor
%if ! %build_hyp
%define build_xsm 0
%endif
# build an efi boot image (where supported) unless rpmbuild was run with
# --without efi
%define build_efi %{?_without_efi: 0} %{?!_without_efi: 1}
# xen only supports efi boot images on x86_64 or aarch64
# i686 builds a x86_64 hypervisor so add that as well
%ifnarch x86_64 aarch64 %{ix86}
%define build_efi 0
%endif
%if "%dist" >= ".fc20"
%define with_systemd_presets 1
%else
%define with_systemd_presets 0
%endif

%if 0%{?centos} >= 8
%define with_systemd_presets 1
%define build_docs 0
%define build_hyp 0
%define build_ovmf 0
%endif

# Workaround for https://bugzilla.redhat.com/1671883
%define _unpackaged_files_terminate_build 0

# Hypervisor ABI
%define hv_abi  4.14

%define upstream_version 4.14.0

%define qubesos_version 4.14.0-9

%define patchurl https://raw.githubusercontent.com/QubesOS/qubes-vmm-xen/v%{qubesos_version}

Summary: Xen is a virtual machine monitor
Name:    xen
Version: %(echo %{upstream_version} | sed 's/-rc.*//')
Release: 16%{?dist}
Epoch:   2002
Group:   Development/Libraries
License: GPLv2+ and LGPLv2+ and BSD
URL:     http://xen.org/
Provides: xen-gvt
Source0: https://downloads.xenproject.org/release/xen/%{version}/xen-%{upstream_version}.tar.gz
Source2: %{patchurl}/xen.logrotate
Source3: %{patchurl}/config
Source32: %{patchurl}/xen.modules-load.conf


# Out-of-tree patches.
#
# Use the following patch numbers:
# 100+:  Fedora
# 200+:  EFI workarounds
# 500+:  Security fixes
# 600+:  Upstreamable patches
# 700+:  GCC7+ fixes
# 800+:  vchan for stubdom
# 900+:  Support for Linux based stubdom
# 1000+: Qubes specific patches
# 1100+: Others

# EFI workarounds
Patch201: %{patchurl}/patch-0001-EFI-early-Add-noexit-to-inhibit-calling-ExitBootServices.patch
Patch202: %{patchurl}/patch-0002-efi-Ensure-incorrectly-typed-runtime-services-get-ma.patch
Patch203: %{patchurl}/patch-0001-Add-xen.cfg-options-for-mapbs-and-noexitboot.patch

# Backports

# Security fixes
Patch500: %{patchurl}/patch-xsa337-1.patch
Patch501: %{patchurl}/patch-xsa337-2.patch
Patch502: %{patchurl}/patch-xsa338.patch
Patch503: %{patchurl}/patch-xsa340.patch
Patch504: %{patchurl}/patch-xsa342.patch
Patch505: %{patchurl}/patch-xsa343-1.patch
Patch506: %{patchurl}/patch-xsa343-2.patch
Patch507: %{patchurl}/patch-xsa343-3.patch
Patch508: %{patchurl}/patch-xsa345-4.14-0001-x86-mm-Refactor-map_pages_to_xen-to-have-only-a-sing.patch
Patch509: %{patchurl}/patch-xsa345-4.14-0002-x86-mm-Refactor-modify_xen_mappings-to-have-one-exit.patch
Patch510: %{patchurl}/patch-xsa345-4.14-0003-x86-mm-Prevent-some-races-in-hypervisor-mapping-upda.patch
Patch511: %{patchurl}/patch-xsa346-1.patch
Patch512: %{patchurl}/patch-xsa346-2.patch
Patch513: %{patchurl}/patch-xsa347-4.14-1.patch
Patch514: %{patchurl}/patch-xsa347-4.14-2.patch
Patch515: %{patchurl}/patch-xsa347-4.14-3.patch
Patch516: %{patchurl}/patch-xsa351-x86-4.14-1.patch
Patch517: %{patchurl}/patch-xsa351-x86-4.14-2.patch
Patch518: %{patchurl}/patch-xsa355.patch
Patch519: %{patchurl}/patch-xsa115-0001-tools-xenstore-allow-removing-child-of-a-node-exceed.patch
Patch520: %{patchurl}/patch-xsa115-0002-tools-xenstore-ignore-transaction-id-for-un-watch.patch
Patch521: %{patchurl}/patch-xsa115-0003-tools-xenstore-fix-node-accounting-after-failed-node.patch
Patch522: %{patchurl}/patch-xsa115-0004-tools-xenstore-simplify-and-rename-check_event_node.patch
Patch523: %{patchurl}/patch-xsa115-0005-tools-xenstore-check-privilege-for-XS_IS_DOMAIN_INTR.patch
Patch524: %{patchurl}/patch-xsa115-0006-tools-xenstore-rework-node-removal.patch
Patch525: %{patchurl}/patch-xsa115-0007-tools-xenstore-fire-watches-only-when-removing-a-spe.patch
Patch526: %{patchurl}/patch-xsa115-0008-tools-xenstore-introduce-node_perms-structure.patch
Patch527: %{patchurl}/patch-xsa115-0009-tools-xenstore-allow-special-watches-for-privileged-.patch
Patch528: %{patchurl}/patch-xsa115-0010-tools-xenstore-avoid-watch-events-for-nodes-without-.patch
Patch529: %{patchurl}/patch-xsa325-4.14.patch


# Upstreamable patches
Patch601: %{patchurl}/patch-xen-libxl-error-write-perm.patch
#TODO: simplified script instead:
# Patch604: patch-libxl-Revert-libxl-Remove-redundant-setting-of-phyical-dev.patch
# Patch605: patch-libxl-allow-PHY-backend-for-files-allocate-loop-devi.patch
# Patch606: patch-libxl-do-not-call-default-block-script.patch
Patch607: %{patchurl}/patch-libxl-do-not-for-backend-on-PCI-remove-when-backend-.patch
Patch614: %{patchurl}/patch-0001-libxl-do-not-fail-device-removal-if-backend-domain-i.patch
Patch621: %{patchurl}/patch-libxc-fix-xc_gntshr_munmap-semantic.patch
Patch622: %{patchurl}/patch-xen-disable-efi-gettime.patch
Patch627: %{patchurl}/patch-libxl-automatically-enable-gfx_passthru-if-IGD-is-as.patch
Patch628: %{patchurl}/patch-libxl-workaround-gcc-10.2-maybe-uninitialized-warnin.patch
Patch629: %{patchurl}/patch-libxl-fix-Werror-stringop-truncation-in-libxl__prepa.patch
Patch630: %{patchurl}/patch-x86-S3-Fix-Shadow-Stack-resume-path.patch
Patch631: %{patchurl}/patch-Revert-xen-credit2-limit-the-max-number-of-CPUs-in-a.patch
Patch632: %{patchurl}/patch-x86-S3-Restore-CR4-earlier-during-resume.patch
Patch633: %{patchurl}/patch-x86-smpboot-Unconditionally-call-memguard_unguard_stack.patch
Patch634: patch-libxl-cleanup-remaining-backend-xs-dirs-after-driver.patch

# GCC8 fixes
Patch714: %{patchurl}/patch-tools-kdd-mute-spurious-gcc-warning.patch

# Support for Linux based stubdom
Patch900: %{patchurl}/patch-disable-dom0-qemu.patch

# MSI fixes
Patch950: %{patchurl}/patch-stubdom-allow-msi-enable.patch

# Qubes specific patches
Patch1001: %{patchurl}/patch-stubdom-vbd-non-dom0-backend.patch
Patch1002: %{patchurl}/patch-xen-no-downloads.patch
Patch1003: %{patchurl}/patch-xen-hotplug-external-store.patch
Patch1006: %{patchurl}/patch-xen-libxl-qubes-minimal-stubdom.patch
Patch1007: %{patchurl}/patch-xen-disable-dom0-qemu.patch
Patch1009: %{patchurl}/patch-xenconsoled-enable-logging.patch
Patch1010: %{patchurl}/patch-stubdom-linux-libxl-suspend.patch
Patch1011: %{patchurl}/patch-xen-hotplug-qubesdb-update.patch
Patch1013: %{patchurl}/patch-stubdom-linux-libxl-use-EHCI-for-providing-tablet-USB-device.patch
Patch1014: %{patchurl}/patch-allow-kernelopts-stubdom.patch
Patch1015: %{patchurl}/patch-libxl-readonly-disk-scsi.patch
Patch1016: %{patchurl}/patch-tools-xenconsole-replace-ESC-char-on-xenconsole-outp.patch
Patch1017: %{patchurl}/patch-libxl-disable-vkb-by-default.patch

Patch1020: %{patchurl}/patch-stubdom-linux-config-qubes-gui.patch
Patch1021: %{patchurl}/patch-stubdom-linux-libxl-do-not-force-qdisk-backend-for-cdrom.patch
Patch1022: %{patchurl}/patch-xen-acpi-slic-support.patch

Patch1030: %{patchurl}/patch-fix-igd-passthrough-with-linux-stubdomain.patch

# Reproducible builds
Patch1050: %{patchurl}/patch-0001-No-insert-of-the-build-timestamp-into-the-x86-xen-ef.patch
Patch1051: %{patchurl}/patch-0002-common-remove-gzip-timestamp.patch
Patch1052: %{patchurl}/patch-Define-build-dates-time-based-on-SOURCE_DATE_EPOCH.patch
Patch1053: %{patchurl}/patch-docs-rename-DATE-to-PANDOC_REL_DATE-and-allow-to-spe.patch
Patch1054: %{patchurl}/patch-docs-xen-headers-use-alphabetical-sorting-for-incont.patch
Patch1055: %{patchurl}/patch-Strip-build-path-directories-in-tools-xen-and-xen-ar.patch

# GVT-g
Patch1200: 0007-hypercall-XENMEM_get_mfn_from_pfn.patch
Patch1201: gvt-g-hvmloader.patch
Patch1202: libxl-init-gvt.patch

%if %build_qemutrad
BuildRequires: libidn-devel zlib-devel SDL-devel curl-devel
BuildRequires: libX11-devel gtk2-devel libaio-devel
# build using Fedora seabios and ipxe packages for roms
BuildRequires: seabios-bin ipxe-roms-qemu
%ifarch %{ix86} x86_64
# for the VMX "bios"
BuildRequires: dev86
%endif
%endif
# qemu-xen
BuildRequires: glib2-devel pixman-devel
BuildRequires: python%{python3_pkgversion}-devel ncurses-devel
BuildRequires: perl-interpreter perl-generators
%ifarch %{ix86} x86_64
# so that x86_64 builds pick up glibc32 correctly
BuildRequires: /usr/include/gnu/stubs-32.h
%endif
# BEGIN QUBES SPECIFIC PART
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: flex
BuildRequires: bison
# END QUBES SPECIFIC PART
BuildRequires: gettext
#BuildRequires: glibc-devel
BuildRequires: gnutls-devel
BuildRequires: openssl-devel
# For ioemu PCI passthrough
BuildRequires: pciutils-devel
# Several tools now use uuid
BuildRequires: libuuid-devel
# iasl needed to build hvmloader
BuildRequires: acpica-tools
# modern compressed kernels
BuildRequires: bzip2-devel xz-devel
# libfsimage
BuildRequires: e2fsprogs-devel
# tools now require yajl
BuildRequires: yajl-devel
# remus support now needs libnl3
BuildRequires: libnl3-devel
%if %with_xsm
# xsm policy file needs needs checkpolicy and m4
BuildRequires: checkpolicy m4
%endif
%if %build_crosshyp
# cross compiler for building 64-bit hypervisor on ix86
BuildRequires: gcc-x86_64-linux-gnu
%endif
BuildRequires: gcc
Requires: iproute
Requires: python%{python3_pkgversion}-lxml
Requires: %{name}-runtime = %{epoch}:%{version}-%{release}
# Not strictly a dependency, but kpartx is by far the most useful tool right
# now for accessing domU data from within a dom0 so bring it in when the user
# installs xen.
Requires: kpartx
ExclusiveArch: %{ix86} x86_64 armv7hl aarch64
#ExclusiveArch: %#{ix86} x86_64 ia64 noarch
%if %with_ocaml
BuildRequires: ocaml, ocaml-findlib
%endif
%if %with_systemd_presets
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
%endif
BuildRequires: systemd-devel
%ifarch armv7hl aarch64
BuildRequires: libfdt-devel
%endif
# BIOS for HVMs
%if 0%{?rhel} >= 7
BuildRequires: OVMF
%else
BuildRequires: edk2-ovmf
%endif
Requires: seabios-bin

%description
This package contains the XenD daemon and xm command line
tools, needed to manage virtual machines running under the
Xen hypervisor

# BEGIN QUBES SPECIFIC PART
%package -n python%{python3_pkgversion}-%{name}
Summary: Python3 bindings for Xen tools
Group: Development/Libraries
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: python%{python3_pkgversion}
%{?python_provide:%python_provide python%{python3_pkgversion}-xen}

%description -n python%{python3_pkgversion}-%{name}
This package contains Python3 bindings to Xen tools. Especially xen.lowlevel.xs
and xen.lowlevel.xc modules.
# END QUBES SPECIFIC PART

%package libs
Summary: Libraries for Xen tools
Group: Development/Libraries
Requires: %{name}-licenses
Provides: xen-gvt-libs
# toolstack <-> stubdomain API change
Conflicts: xen-hvm-stubdom-linux < 1.1.0

%description libs
This package contains the libraries needed to run applications
which manage Xen virtual machines.


%package runtime
Summary: Core Xen runtime environment
Group: Development/Libraries
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: /usr/bin/qemu-img
# Ensure we at least have a suitable kernel installed, though we can't
# force user to actually boot it.
Requires: %{name}-hypervisor-abi = %{hv_abi}
%if %with_systemd_presets
Requires(post): systemd
Requires(preun): systemd
%endif

%description runtime
This package contains the runtime programs and daemons which
form the core Xen userspace environment.


%package hypervisor
Summary: Libraries for Xen tools
Group: Development/Libraries
Provides: xen-hypervisor-abi = %{hv_abi}
Requires: %{name}-licenses

%description hypervisor
This package contains the Xen hypervisor


%if %build_docs
%package doc
Summary: Xen documentation
Group: Documentation
BuildArch: noarch
Requires: %{name}-licenses
# for the docs
BuildRequires: texlive-times texlive-courier texlive-helvetic texlive-ntgclass
BuildRequires: transfig texi2html ghostscript texlive-latex
BuildRequires: perl(Pod::Man) perl(Pod::Text) texinfo graphviz
# optional requires for more documentation
BuildRequires: pandoc discount
BuildRequires: discount

%description doc
This package contains the Xen documentation.
%endif


%package devel
Summary: Development libraries for Xen tools
Group: Development/Libraries
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: libuuid-devel

%description devel
This package contains what's needed to develop applications
which manage Xen virtual machines.


%package licenses
Summary: License files from Xen source
Group: Documentation

%description licenses
This package contains the license files from the source used
to build the xen packages.


%if %build_ocaml
%package ocaml
Summary: Ocaml libraries for Xen tools
Group: Development/Libraries
Requires: ocaml-runtime, %{name}-libs = %{epoch}:%{version}-%{release}

%description ocaml
This package contains libraries for ocaml tools to manage Xen
virtual machines.


%package ocaml-devel
Summary: Ocaml development libraries for Xen tools
Group: Development/Libraries
Requires: %{name}-ocaml = %{epoch}:%{version}-%{release}

%description ocaml-devel
This package contains libraries for developing ocaml tools to
manage Xen virtual machines.
%endif

# BEGIN QUBES SPECIFIC PART
%package qemu-tools
Summary: Qemu disk tools bundled with Xen
Provides: qemu-img
Conflicts: qemu-img

%description qemu-tools
This package contains symlinks to qemu tools (qemu-img, qemu-nbd)
budled with Xen, making them available for general use.

%package qubes-vm
Summary: Xen files required in Qubes VM
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Conflicts: xen
Provides: xen-qubes-vm-essentials = %{epoch}:%{version}-%{release}

%description qubes-vm
Just a few xenstore-* tools and Xen hotplug scripts needed by Qubes VMs
# END QUBES SPECIFIC PART

%prep
%autosetup -p1 -n xen-%{upstream_version}

# copy xen hypervisor .config file to change settings
cp -v %{SOURCE3} xen/.config

sed -i -e s/"max_maptrack_frames = 0"/"max_maptrack_frames = guest_config->b_info.max_maptrack_frames"/g tools/libxl/libxl_dm.c

# Fix for glibc 2.7
#FIXME sed 's:LIBS+=-lutil:LIBS+=-lutil -lrt:' -i tools/ioemu-qemu-xen/Makefile.target

%build
%if !%build_ocaml
%define ocaml_flags OCAML_TOOLS=n
%endif
%if %build_efi
%define efi_flags EFI_VENDOR=qubes
mkdir -p dist/install/boot/efi/efi/qubes
%endif
%if %build_ocaml
mkdir -p dist/install%{_libdir}/ocaml/stublibs
%endif
%define seabiosloc /usr/share/seabios/bios-256k.bin
#export XEN_VENDORVERSION="-%{release}"
export EXTRA_CFLAGS_XEN_TOOLS="$RPM_OPT_FLAGS -Wno-error=declaration-after-statement"
export EXTRA_CFLAGS_QEMU_TRADITIONAL="$RPM_OPT_FLAGS"
export EXTRA_CFLAGS_QEMU_XEN="$RPM_OPT_FLAGS"
export PYTHON="%{__python3}"
export KCONFIG_CONFIG=%{SOURCE3}
cp -f %{SOURCE3} xen/.config
export XEN_CONFIG_EXPERT=y
%if %build_hyp
%if %build_crosshyp
%define efi_flags LD_EFI=false
XEN_TARGET_ARCH=x86_64 make %{?_smp_mflags} %{?efi_flags} prefix=/usr xen CC="/usr/bin/x86_64-linux-gnu-gcc `echo $RPM_OPT_FLAGS | sed -e 's/-m32//g' -e 's/-march=i686//g' -e 's/-mtune=atom//g' -e 's/-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1//g' -e 's/-fstack-clash-protection//g' -e 's/-mcet//g' -e 's/-fcf-protection//g'`"
%else
%ifarch armv7hl
make %{?_smp_mflags} %{?efi_flags} prefix=/usr xen CC="gcc `echo $RPM_OPT_FLAGS | sed -e 's/-mfloat-abi=hard//g' -e 's/-march=armv7-a//g'`"
%else
%ifarch aarch64
make %{?_smp_mflags} %{?efi_flags} prefix=/usr xen CC="gcc $RPM_OPT_FLAGS"
%else
make %{?_smp_mflags} %{?efi_flags} prefix=/usr xen CC="gcc `echo $RPM_OPT_FLAGS | sed -e 's/-specs=\/usr\/lib\/rpm\/redhat\/redhat-annobin-cc1//g' -e 's/-fcf-protection//g'`"
%endif
%endif
%endif
%endif
%if ! %build_qemutrad
CONFIG_EXTRA="--disable-qemu-traditional"
%else
CONFIG_EXTRA=""
%endif
%if ! %build_stubdom
CONFIG_EXTRA="$CONFIG_EXTRA --disable-stubdom"
%endif
%if %build_ovmf
CONFIG_EXTRA="$CONFIG_EXTRA --with-system-ovmf=%{_libexecdir}/xen/boot/ovmf.bin"
%endif
# BEGIN QUBES SPECIFIC PART
%ifnarch armv7hl aarch64
#CONFIG_EXTRA="$CONFIG_EXTRA --with-system-ipxe=/usr/share/ipxe"
CONFIG_EXTRA="$CONFIG_EXTRA --disable-ipxe --disable-rombios"
CONFIG_EXTRA="$CONFIG_EXTRA --disable-pvshim"
%endif
CONFIG_EXTRA="$CONFIG_EXTRA --with-extra-qemuu-configure-args='--disable-spice'"
export PATH="/usr/bin:$PATH"
autoreconf
# END QUBES SPECIFIC PART
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --with-system-seabios=%{seabiosloc} \
    --with-linux-backend-modules="xen-evtchn xen-gntdev xen-gntalloc xen-blkback xen-netback xen-pciback xen-scsiback xen-acpi-processor" \
    $CONFIG_EXTRA
make %{?_smp_mflags} %{?ocaml_flags} prefix=/usr tools
%if %build_docs
make prefix=/usr docs
%endif
export RPM_OPT_FLAGS_RED=`echo $RPM_OPT_FLAGS | sed -e 's/-m64//g' -e 's/--param=ssp-buffer-size=4//g' -e's/-fstack-protector-strong//'`
%ifarch %{ix86}
export EXTRA_CFLAGS_XEN_TOOLS="$RPM_OPT_FLAGS_RED"
%endif
%if %build_stubdom
%ifnarch armv7hl aarch64
make mini-os-dir
make -C stubdom build
%endif
%ifarch x86_64
export EXTRA_CFLAGS_XEN_TOOLS="$RPM_OPT_FLAGS_RED"
XEN_TARGET_ARCH=x86_32 make -C stubdom pv-grub
%endif
%endif


%install
#export XEN_VENDORVERSION="-%{release}"
export EXTRA_CFLAGS_XEN_TOOLS="$RPM_OPT_FLAGS"
export EXTRA_CFLAGS_QEMU_TRADITIONAL="$RPM_OPT_FLAGS"
export EXTRA_CFLAGS_QEMU_XEN="$RPM_OPT_FLAGS"
export PATH="/usr/bin:$PATH"
export KCONFIG_CONFIG=%{SOURCE3}
export XEN_CONFIG_EXPERT=y
rm -rf %{buildroot}
mkdir -p %{buildroot}
cp -prlP dist/install/* %{buildroot}
%if %build_stubdom
%ifnarch armv7hl aarch64
make DESTDIR=%{buildroot} %{?ocaml_flags} prefix=/usr install-stubdom
%endif
%endif
%if %build_efi
mkdir -p %{buildroot}/boot/efi/efi/qubes
%endif
%if %build_efi
mv %{buildroot}/boot/efi/efi %{buildroot}/boot/efi/EFI
%endif
%if %build_xsm
# policy file should be in /boot/flask
mkdir %{buildroot}/boot/flask
mv %{buildroot}/boot/xenpolicy* %{buildroot}/boot/flask
%else
rm -f %{buildroot}/boot/xenpolicy*
rm -f %{buildroot}/usr/sbin/flask-*
%endif

############ debug packaging: list files ############

find %{buildroot} -print | xargs ls -ld | sed -e 's|.*%{buildroot}||' > f1.list

############ kill unwanted stuff ############

# stubdom: newlib
rm -rf %{buildroot}/usr/*-xen-elf

# hypervisor symlinks
rm -rf %{buildroot}/boot/xen-%{hv_abi}.gz
rm -rf %{buildroot}/boot/xen-4.gz
rm -rf %{buildroot}/boot/xen.gz
%if !%build_hyp
rm -rf %{buildroot}/boot
%endif

# silly doc dir fun
rm -fr %{buildroot}%{_datadir}/doc/xen
rm -rf %{buildroot}%{_datadir}/doc/qemu

# Pointless helper
rm -f %{buildroot}%{_sbindir}/xen-python-path

# qemu stuff (unused or available from upstream)
rm -rf %{buildroot}/usr/share/xen/man
rm -rf %{buildroot}/usr/share/qemu-xen/icons
rm -rf %{buildroot}/usr/share/qemu-xen/applications
# BEGIN QUBES SPECIFIC PART
ln -s ../libexec/%{name}/bin/qemu-img %{buildroot}/%{_bindir}/qemu-img
ln -s ../libexec/%{name}/bin/qemu-nbd %{buildroot}/%{_bindir}/qemu-nbd
# END QUBES SPECIFIC PART
for file in bios.bin openbios-sparc32 openbios-sparc64 ppc_rom.bin \
         pxe-e1000.bin pxe-ne2k_pci.bin pxe-pcnet.bin pxe-rtl8139.bin \
         vgabios.bin vgabios-cirrus.bin video.x openbios-ppc bamboo.dtb
do
	rm -f %{buildroot}/%{_datadir}/xen/qemu/$file
done

# BEGIN QUBES SPECIFIC PART
rm -f %{buildroot}/usr/libexec/qemu-bridge-helper
# END QUBES SPECIFIC PART

# README's not intended for end users
rm -f %{buildroot}/%{_sysconfdir}/xen/README*

# standard gnu info files
rm -rf %{buildroot}/usr/info

# adhere to Static Library Packaging Guidelines
rm -rf %{buildroot}/%{_libdir}/*.a

%if %build_efi
# clean up extra efi files
rm -rf %{buildroot}/%{_libdir}/efi
%ifarch %{ix86}
rm -rf %{buildroot}/usr/lib64/efi
%endif
%endif

%if ! %build_ocaml
rm -rf %{buildroot}/%{_unitdir}/oxenstored.service
%endif

%if %build_ovmf
#%if 0%{?rhel} >=7
#cat /usr/share/OVMF/OVMF_{VARS,CODE.secboot}.fd > %{buildroot}/usr/lib/xen/boot/ovmf.bin
#%else
cat /usr/share/OVMF/OVMF_{VARS,CODE}.fd >%{buildroot}%{_libexecdir}/xen/boot/ovmf.bin
#%endif
%endif

############ fixup files in /etc ############

# logrotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/xen

# init scripts
rm %{buildroot}%{_sysconfdir}/rc.d/init.d/xen-watchdog
rm %{buildroot}%{_sysconfdir}/rc.d/init.d/xencommons
rm %{buildroot}%{_sysconfdir}/rc.d/init.d/xendomains
rm %{buildroot}%{_sysconfdir}/rc.d/init.d/xendriverdomain
# BEGIN QUBES SPECIFIC PART
rm %{buildroot}%{_sysconfdir}/sysconfig/xendomains
cp %{SOURCE32} %{buildroot}/usr/lib/modules-load.d/xen.conf

# get rid of standard domain starting scripts
rm %{buildroot}%{_unitdir}/xen-qemu-dom0-disk-backend.service
rm %{buildroot}%{_unitdir}/xendomains.service

# unused and dangerous
rm -f %{buildroot}/%{_bindir}/pygrub
rm -rf %{buildroot}/%{python3_sitearch}/pygrub*
# END QUBES SPECIFIC PART

############ create dirs in /var ############

mkdir -p %{buildroot}%{_localstatedir}/lib/xen/images
mkdir -p %{buildroot}%{_localstatedir}/log/xen/console

############ create symlink for x86_64 for compatibility with 4.4 ############

%if "%{_libdir}" != "/usr/lib"
ln -s %{_libexecdir}/xen %{buildroot}/%{_libdir}/xen
%endif

# BEGIN QUBES SPECIFIC PART
# don't create symlink to qemu-system-i386
ln -s ../sbin/xl %{buildroot}/%{_bindir}/xl
# END QUBES SPECIFIC PART

############ debug packaging: list files ############

find %{buildroot} -print | xargs ls -ld | sed -e 's|.*%{buildroot}||' > f2.list
diff -u f1.list f2.list || true

############ assemble license files ############

mkdir licensedir
# avoid licensedir to avoid recursion, also stubdom/ioemu and dist
# which are copies of files elsewhere
find . -path licensedir -prune -o -path stubdom/ioemu -prune -o \
  -path dist -prune -o -name COPYING -o -name LICENSE | while read file; do
  mkdir -p licensedir/`dirname $file`
  install -m 644 $file licensedir/$file
done

############ all done now ############

%posttrans runtime
%systemd_post xenstored.service xenconsoled.service xen-init-dom0.service

%preun runtime
%systemd_preun xenstored.service xenconsoled.service xen-init-dom0.service

%post qubes-vm
# Unconditionally enable this service in Qubes VM
systemctl enable xendriverdomain.service >/dev/null 2>&1 || :

%preun qubes-vm
%systemd_preun xendriverdomain.service

%post libs

/sbin/ldconfig

%ldconfig_scriptlets libs

%if %build_hyp
%post hypervisor
%if %build_efi
XEN_EFI_VERSION=$(echo %{upstream_version} | sed -e 's/rc./rc/')-%{release}
EFI_DIR=$(efibootmgr -v 2>/dev/null | awk '
      /^BootCurrent:/ { current=$2; }
      /^Boot....\* / {
          if ("Boot" current "*" == $1) {
              sub(".*File\\(", "");
              sub("\\\\xen.efi\\).*", "");
              gsub("\\\\", "/");
              print;
          }
      }')
# FAT (on ESP) does not support symlinks
# override the file on purpose
if [ -n "${EFI_DIR}" -a -d "/boot/efi${EFI_DIR}" ]; then
  cp -pf /boot/efi/EFI/qubes/xen-$XEN_EFI_VERSION.efi /boot/efi${EFI_DIR}/xen.efi
else
  cp -pf /boot/efi/EFI/qubes/xen-$XEN_EFI_VERSION.efi /boot/efi/EFI/qubes/xen.efi
fi
%endif

if [ -f /boot/efi/EFI/qubes/xen.cfg ]; then
    if ! grep -q smt=off /boot/efi/EFI/qubes/xen.cfg; then
        sed -i -e 's:^options=.*:\0 smt=off:' /boot/efi/EFI/qubes/xen.cfg
    fi
    if ! grep -q gnttab_max_frames /boot/efi/EFI/qubes/xen.cfg; then
        sed -i -e 's:^options=.*:\0 gnttab_max_frames=2048 gnttab_max_maptrack_frames=4096:' /boot/efi/EFI/qubes/xen.cfg
    fi
fi

if [ -f /etc/default/grub ]; then
    if ! grep -q smt=off /etc/default/grub; then
        echo 'GRUB_CMDLINE_XEN_DEFAULT="$GRUB_CMDLINE_XEN_DEFAULT smt=off"' >> /etc/default/grub
        grub2-mkconfig -o /boot/grub2/grub.cfg
    fi
    if ! grep -q gnttab_max_frames /etc/default/grub; then
        echo 'GRUB_CMDLINE_XEN_DEFAULT="$GRUB_CMDLINE_XEN_DEFAULT gnttab_max_frames=2048 gnttab_max_maptrack_frames=4096"' >> /etc/default/grub
        grub2-mkconfig -o /boot/grub2/grub.cfg
    fi
fi

if [ $1 == 1 -a -f /sbin/grub2-mkconfig ]; then
  if [ -f /boot/grub2/grub.cfg ]; then
    /sbin/grub2-mkconfig -o /boot/grub2/grub.cfg
  fi
  if [ -f /boot/efi/EFI/qubes/grub.cfg ]; then
    /sbin/grub2-mkconfig -o /boot/efi/EFI/qubes/grub.cfg
  fi
fi

%postun hypervisor
if [ -f /sbin/grub2-mkconfig ]; then
  if [ -f /boot/grub2/grub.cfg ]; then
    /sbin/grub2-mkconfig -o /boot/grub2/grub.cfg
  fi
  if [ -f /boot/efi/EFI/qubes/grub.cfg ]; then
    /sbin/grub2-mkconfig -o /boot/efi/EFI/qubes/grub.cfg
  fi
fi
%endif

%if %build_ocaml
%post ocaml
%systemd_post oxenstored.service

%preun ocaml
%systemd_preun oxenstored.service
%endif

%posttrans libs
# reload libxl library
systemctl try-restart libvirtd.service >/dev/null 2>&1 || :

%clean
rm -rf %{buildroot}

# Base package only contains XenD/xm python stuff
#files -f xen-xm.lang
%files
#%defattr(-,root,root)
%doc COPYING README
%{_bindir}/xencons

# BEGIN QUBES SPECIFIC PART
%files -n python%{python3_pkgversion}-%{name}
%{python3_sitearch}/xen
%{python3_sitearch}/xen-*.egg-info
# END QUBES SPECIFIC PART

%files libs
#%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/xenfsimage

# All runtime stuff except for XenD/xm python stuff
%files runtime
#%defattr(-,root,root)
# Hotplug rules

%dir %attr(0700,root,root) %{_sysconfdir}/xen
%dir %attr(0700,root,root) %{_sysconfdir}/xen/scripts/
%config %attr(0700,root,root) %{_sysconfdir}/xen/scripts/*

%{_sysconfdir}/bash_completion.d/xl.sh

%{_unitdir}/proc-xen.mount
%{_unitdir}/var-lib-xenstored.mount
%{_unitdir}/xenstored.service
%{_unitdir}/xenconsoled.service
%{_unitdir}/xen-watchdog.service
# BEGIN QUBES SPECIFIC PART
%{_unitdir}/xen-init-dom0.service
%exclude %{_unitdir}/xendriverdomain.service
# END QUBES SPECIFIC PART
/usr/lib/modules-load.d/xen.conf

%config(noreplace) %{_sysconfdir}/sysconfig/xencommons
%config(noreplace) %{_sysconfdir}/xen/xl.conf
%config(noreplace) %{_sysconfdir}/xen/cpupool
%config(noreplace) %{_sysconfdir}/xen/xlexample*

# Rotate console log files
%config(noreplace) %{_sysconfdir}/logrotate.d/xen

# Programs run by other programs
%dir %{_libexecdir}/xen
%dir %{_libexecdir}/xen/bin
%attr(0700,root,root) %{_libexecdir}/xen/bin/*
# QEMU runtime files
%if %build_qemutrad
%ifnarch armv7hl aarch64
%dir %{_datadir}/xen/qemu
%dir %{_datadir}/xen/qemu/keymaps
%{_datadir}/xen/qemu/keymaps/*
%endif
%endif
# BEGIN QUBES SPECIFIC PART
%dir %{_datadir}/qemu-xen
%dir %{_datadir}/qemu-xen/qemu
%{_datadir}/qemu-xen/qemu/*
# END QUBES SPECIFIC PART

# man pages
%if %build_docs
%{_mandir}/man1/xentop.1*
%{_mandir}/man1/xentrace_format.1*
%{_mandir}/man8/xentrace.8*
%{_mandir}/man1/xl.1*
%{_mandir}/man5/xl.cfg.5*
%{_mandir}/man5/xl.conf.5*
%{_mandir}/man5/xlcpupool.cfg.5*
%{_mandir}/man1/xenstore*
%{_mandir}/man1/xenhypfs.1*
%{_mandir}/man5/xl-disk-configuration.5.gz
%{_mandir}/man7/xen-pci-device-reservations.7.gz
%{_mandir}/man7/xen-tscmode.7.gz
%{_mandir}/man7/xen-vtpm.7.gz
%{_mandir}/man7/xen-vtpmmgr.7.gz
%{_mandir}/man5/xl-network-configuration.5.gz
%{_mandir}/man7/xen-pv-channel.7.gz
%{_mandir}/man7/xl-numa-placement.7.gz
%endif

%{python3_sitearch}/xenfsimage*.so
%{python3_sitearch}/grub

# The firmware
%ifarch %{ix86} x86_64
%dir %{_libexecdir}/xen/boot
%{_libexecdir}/xen/boot/hvmloader
%if %build_ovmf
%{_libexecdir}/xen/boot/ovmf.bin
%endif
%if %build_stubdom
%{_libexecdir}/xen/boot/ioemu-stubdom.gz
%{_libexecdir}/xen/boot/xenstore-stubdom.gz
%{_libexecdir}/xen/boot/pv-grub*.gz
#%{_libexecdir}/xen/boot/vtpm-stubdom.gz
#%{_libexecdir}/xen/boot/vtpmmgr-stubdom.gz
%endif
%endif
%ghost /usr/lib/xen
# General Xen state
%dir %{_localstatedir}/lib/xen
%dir %{_localstatedir}/lib/xen/dump
%dir %{_localstatedir}/lib/xen/images
# Xenstore persistent state
%dir %{_localstatedir}/lib/xenstored
# Xenstore runtime state
%ghost %{_localstatedir}/run/xenstored

# All xenstore CLI tools
%{_bindir}/xenstore
%{_bindir}/xenstore-*
%{_bindir}/xentrace*
#%%{_bindir}/remus
# XSM
%if %build_xsm
%{_sbindir}/flask-*
%endif
# Misc stuff
%ifnarch armv7hl aarch64
%{_bindir}/xen-detect
%endif
%{_bindir}/vchan-socket-proxy
%{_bindir}/xencov_split
%ifnarch armv7hl aarch64
%{_sbindir}/gdbsx
%{_sbindir}/xen-kdd
%endif
%ifnarch armv7hl aarch64
%{_sbindir}/xen-hptool
%{_sbindir}/xen-hvmcrash
%{_sbindir}/xen-hvmctx
%endif
%{_sbindir}/xenconsoled
%{_sbindir}/xenlockprof
%{_sbindir}/xenmon
%{_sbindir}/xentop
%{_sbindir}/xentrace_setmask
%{_sbindir}/xenbaked
%{_sbindir}/xenstored
%{_sbindir}/xenpm
%{_sbindir}/xenpmd
%{_sbindir}/xenperf
%{_sbindir}/xenwatchdogd
%{_sbindir}/xl
%{_sbindir}/xen-ucode
%{_sbindir}/xenhypfs
%ifnarch armv7hl aarch64
%{_sbindir}/xen-lowmemd
%endif
%{_sbindir}/xencov
%ifnarch armv7hl aarch64
%{_sbindir}/xen-mfndump
%endif
%{_bindir}/xenalyze
%{_sbindir}/xentrace
%{_sbindir}/xentrace_setsize
%ifnarch armv7hl aarch64
%{_bindir}/xen-cpuid
%endif
%{_sbindir}/xen-livepatch
%{_sbindir}/xen-diag
# BEGIN QUBES SPECIFIC PART
%{_bindir}/xl
# END QUBES SPECIFIC PART

# Xen logfiles
%dir %attr(0700,root,root) %{_localstatedir}/log/xen
# Guest/HV console logs
%dir %attr(0700,root,root) %{_localstatedir}/log/xen/console

%files hypervisor
%if %build_hyp
%defattr(-,root,root)
%ifnarch armv7hl aarch64
/boot/xen-*.gz
/boot/xen*.config
%else
/boot/xen*
%endif
%if %build_xsm
%dir %attr(0755,root,root) /boot/flask
/boot/flask/xenpolicy*
%endif
%if %build_efi
/boot/efi/EFI/qubes/*.efi
%endif
/usr/lib/debug/xen*
%endif

%if %build_docs
%files doc
%defattr(-,root,root)
%doc docs/misc/
%doc dist/install/usr/share/doc/xen/html
%endif

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%dir %{_includedir}/xen
%{_includedir}/xen/*
%dir %{_includedir}/xenstore-compat
%{_includedir}/xenstore-compat/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files licenses
%defattr(-,root,root)
%doc licensedir/*

%if %build_ocaml
%files ocaml
%defattr(-,root,root)
%{_libdir}/ocaml/xen*
%exclude %{_libdir}/ocaml/xen*/*.a
%exclude %{_libdir}/ocaml/xen*/*.cmxa
%exclude %{_libdir}/ocaml/xen*/*.cmx
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner
%{_sbindir}/oxenstored
%config(noreplace) %{_sysconfdir}/xen/oxenstored.conf
%{_unitdir}/oxenstored.service

%files ocaml-devel
%defattr(-,root,root)
%{_libdir}/ocaml/xen*/*.a
%{_libdir}/ocaml/xen*/*.cmxa
%{_libdir}/ocaml/xen*/*.cmx
%endif

# BEGIN QUBES SPECIFIC PART
%files qemu-tools
/usr/bin/qemu-img
/usr/bin/qemu-nbd

%files qubes-vm
%{_bindir}/xenstore
%{_bindir}/xenstore-*
%{_sbindir}/xl
%{_unitdir}/xendriverdomain.service
%config(noreplace) %{_sysconfdir}/xen/xl.conf

%dir %attr(0700,root,root) %{_sysconfdir}/xen
%dir %attr(0700,root,root) %{_sysconfdir}/xen/scripts/
%config %attr(0700,root,root) %{_sysconfdir}/xen/scripts/*

# General Xen state
%dir %{_localstatedir}/lib/xen
%dir %{_localstatedir}/lib/xen/dump

# Xen logfiles
%dir %attr(0700,root,root) %{_localstatedir}/log/xen

# Python modules
%dir %{python3_sitearch}/xen
%{python3_sitearch}/xen/__init__.*
%{python3_sitearch}/xen/lowlevel
%{python3_sitearch}/xen-*.egg-info
# END QUBES SPECIFIC PART

%changelog
* Wed Sep 25 2019 Qubes OS Team <qubes-devel@groups.google.com>
- For complete changelog see: https://github.com/QubesOS/qubes-

* Wed Sep 25 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 2ba6590
- version 4.12.1-2

* Wed Sep 25 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 2d17e02
- rpm: move libvirtd restart to posttrans

* Sat Sep 07 2019 Frédéric Pierret (fepitre) <frederic.pierret@qubes-os.org> - 2d383a8
- spec: drop systemd_postun

* Sat Sep 07 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 382d5d8
- Update to 4.12.1

* Fri Sep 06 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - fa04126
- travis: add bullseye

* Fri Sep 06 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - c0f46e2
- debian: build for bullseye too

* Fri Sep 06 2019 Ivan Kardykov <kardykov@tabit.pro> - 4541840
- add patch from OpenXT to additional support in ACPI builder to apply SLIC and OEM installs

* Fri Sep 06 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - f4c636e
- Fix xs.read_watch() python binding

* Fri Aug 09 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 64b400f
- Fix -Wsign-compare warning

* Fri Jul 19 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - df7dc1f
- version 4.12.0-3

* Thu Jun 27 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 35cbeb3
- Apply fixes for framebuffer placed over 4GB

* Mon Jun 10 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 11cedc5
- version 4.12.0-2

* Mon Jun 10 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 00ed41a
- Abort the major upgrade if any VM is running

* Mon Jun 10 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - dfcb257
- Remove obsolete patches from series-vm.conf

* Mon Jun 10 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - bfc179f
- Fix xc_physinfo python wrapper

* Mon Apr 22 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - eaa5a54
- version 4.12.0-1

* Mon Apr 22 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 4fc524c
- Revert "hvm: Use our SeaBIOS build"

* Tue Mar 19 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - ed1226c
- version 4.12.0-rc6-1

* Tue Mar 19 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 6e6e19d
- rpm: fix macros

* Tue Mar 19 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - fbc63f4
- Merge remote-tracking branch 'origin/pr/53' into xen-4.12

* Tue Mar 19 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - f8e6ba9
- rpm: export the same env variable during build and install

* Sun Mar 17 2019 Frédéric Pierret (fepitre) <frederic.pierret@qubes-os.org> - 4411f70
- Fix errors on ambiguous python shebangs

* Sun Mar 17 2019 Frédéric Pierret (fepitre) <frederic.pierret@qubes-os.org> - 63d5d0d
- Fix GCC9 warnings based on Fedora upstream patch

* Thu Feb 21 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 3eacc53
- version 4.12.0-rc3-1

* Thu Feb 21 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - ce69e96
- By default forbid terminal control sequences on xl console output

* Thu Feb 21 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 893fefa
- rpm: do not load xen-acpi-processor with systemd-modules-load

* Thu Feb 21 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - b978769
- debian: load only pvops xen modules

* Thu Feb 21 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 70b2a02
- debian: fix applying patches

* Thu Feb 21 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 481c714
- rpm: add BR: python

* Thu Feb 21 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - aeb47f5
- Fix building xen.efi

* Thu Feb 21 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - baaea92
- Improve handling -rc releases

* Tue Feb 19 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 6ca9531
- travis: update for R4.1

* Tue Feb 19 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 3baed2c
- Merge remote-tracking branch 'origin/pr/51' into xen-4.12-devel

* Tue Feb 19 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 4d17c8c
- debian: fix build on stretch

* Sat Feb 16 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - fcc2b43
- debian: include native xendriverdomain.service

* Sat Feb 16 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 68d611c
- debian: update packaging based on upstream Xen 4.11 package

* Sat Feb 16 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 7d260d3
- Fix copying xen.efi

* Sat Feb 16 2019 Simon Gaiser <simon@invisiblethingslab.com> - 2b5b794
- libxl: Add support for new qubes-gui options

* Sat Feb 16 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 5eabaaa
- Few more QubesOS specific stubdomain fixes

* Sat Feb 16 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - ea78a7d
- Replace stubdomain MSI fix with the version sent upstream

* Sat Feb 16 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 61746bf
- Update to Xen 4.12-rc1

* Sat Feb 16 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - d884c3e
- Update to Xen 4.11

* Sun Jan 27 2019 Frédéric Pierret (fepitre) <frederic.pierret@qubes-os.org> - 59ec1e4
- Build Qubes Xen package only for dom0 Fedora and use upstream for VM

* Thu Jan 10 2019 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - a4a4cc7
- version 4.8.5-1

* Sat Dec 15 2018 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - f828c93
- travis: switch to xenial

* Sat Dec 15 2018 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 880d2b3
- rpm: add BR: glibc-devel

* Sat Dec 15 2018 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - fc7aeb6
- debian: fix Build-Depends - dh-python2 is not included in python2.7-minimal

* Thu Dec 13 2018 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 7ef0e88
- debian: fixes for reproducible source package

* Wed Nov 28 2018 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - a4fc800
- version 4.8.4-8

* Wed Nov 28 2018 Marek Marczykowski-Górecki <marmarek@invisiblethingslab.com> - 509f75b
- Backport AMD IOMMU driver support for IOAPIC IDs larger than 128

